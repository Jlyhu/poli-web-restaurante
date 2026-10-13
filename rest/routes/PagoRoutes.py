from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from datetime import datetime

from rest import db
from rest.modelos.PagoModel import Pago
from rest.schemas.PagoSchema import PagoSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('pago', __name__)
esquema = PagoSchema()


# ---------- CONSULTAR ----------
@bp.route('/getPagos', methods=['GET'])
def listar():
    registros = db.session.query(Pago).order_by(Pago.id_pago).all()
    return jsonify([r.toDict() for r in registros])


@bp.route('/getPago/<int:id_pago>', methods=['GET'])
def obtener(id_pago):
    r = db.session.get(Pago, id_pago)
    if r is None:
        return no_encontrada('un pago', id_pago)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertPago', methods=['POST'])
def insertar():
    try:
        datos = esquema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_id = datos.get('id_pago')
    if nuevo_id is None:
        nuevo_id = siguiente_id(Pago.id_pago)

    r = Pago(id_pago=nuevo_id,
            monto=datos.get('monto'),
            metodo_pago=datos.get('metodo_pago'),
            fecha_pago=datos.get('fecha_pago') or datetime.now(),
            Pedido_id_pedido=datos.get('Pedido_id_pedido'),
            Caja_id_caja=datos.get('Caja_id_caja'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updatePago/<int:id_pago>', methods=['PUT'])
def actualizar(id_pago):
    r = db.session.get(Pago, id_pago)
    if r is None:
        return no_encontrada('un pago', id_pago)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = esquema.load(request.get_json(silent=True) or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_pago', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deletePago/<int:id_pago>', methods=['DELETE'])
def eliminar(id_pago):
    r = db.session.get(Pago, id_pago)
    if r is None:
        return no_encontrada('un pago', id_pago)

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Pago {id_pago} eliminado'})
