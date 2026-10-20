from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.CajaModel import Caja
from rest.schemas.CajaSchema import CajaSchema, CerrarCajaSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('caja', __name__)
caja_schema = CajaSchema()


# ---------- CONSULTAR ----------
@bp.route('/getCajas', methods=['GET'])
def cajas():
    consulta = db.session.query(Caja)
    # opcional: /getCajas?cajero=3
    idcajero = request.args.get('cajero', type=int)
    if idcajero is not None:
        consulta = consulta.filter(Caja.Cajero_id_cajero == idcajero)
    mis = consulta.order_by(Caja.id_caja).all()
    return jsonify([x.toDict() for x in mis])


@bp.route('/getCaja/<int:idcaja>', methods=['GET'])
def caja(idcaja):
    x = db.session.get(Caja, idcaja)
    if x is None:
        return no_encontrada('una caja', idcaja)
    return jsonify(x.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertCaja', methods=['POST'])
def insertCaja():
    try:
        datos = caja_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idcaja = datos.get('id_caja')
    if idcaja is None:
        idcaja = siguiente_id(Caja.id_caja)

    x = Caja(id_caja=idcaja,
             fecha_apertura=datetime.now(),
             monto_inicial=datos.get('monto_inicial'),
             Cajero_id_cajero=datos.get('Cajero_id_cajero'))
    db.session.add(x)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateCaja/<int:idcaja>', methods=['PUT'])
def updateCaja(idcaja):
    x = db.session.get(Caja, idcaja)
    if x is None:
        return no_encontrada('una caja', idcaja)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = caja_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_caja', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(x, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- CERRAR ----------
@bp.route('/cerrarCaja/<int:idcaja>', methods=['PUT'])
def cerrarCaja(idcaja):
    # Guarda el monto final y la fecha de cierre (ahora). Una caja cerrada no se vuelve a cerrar.
    x = db.session.get(Caja, idcaja)
    if x is None:
        return no_encontrada('una caja', idcaja)
    if x.fecha_cierre is not None:
        return jsonify({'error': f'La caja {idcaja} ya está cerrada'}), 409

    try:
        datos = CerrarCajaSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    x.monto_final = datos['monto_final']
    x.fecha_cierre = datetime.now()

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteCaja/<int:idcaja>', methods=['DELETE'])
def deleteCaja(idcaja):
    x = db.session.get(Caja, idcaja)
    if x is None:
        return no_encontrada('una caja', idcaja)

    db.session.delete(x)

    # Si una caja ya tiene registros relacionados la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Caja {idcaja} eliminado'})
