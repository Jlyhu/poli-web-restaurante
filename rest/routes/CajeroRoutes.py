from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.CajeroModel import Cajero
from rest.schemas.CajeroSchema import CajeroSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('cajero', __name__)
cajero_schema = CajeroSchema()


# ---------- CONSULTAR ----------
@bp.route('/getCajeros', methods=['GET'])
def cajeros():
    consulta = db.session.query(Cajero)
    # opcional: /getCajeros?usuario=5
    idusuario = request.args.get('usuario', type=int)
    if idusuario is not None:
        consulta = consulta.filter(Cajero.Usuario_idUsuario == idusuario)
    mis = consulta.order_by(Cajero.id_cajero).all()
    return jsonify([x.toDict() for x in mis])


@bp.route('/getCajero/<int:idcajero>', methods=['GET'])
def cajero(idcajero):
    x = db.session.get(Cajero, idcajero)
    if x is None:
        return no_encontrada('un cajero', idcajero)
    return jsonify(x.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertCajero', methods=['POST'])
def insertCajero():
    try:
        datos = cajero_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idcajero = datos.get('id_cajero')
    if idcajero is None:
        idcajero = siguiente_id(Cajero.id_cajero)

    x = Cajero(id_cajero=idcajero,
               Usuario_idUsuario=datos.get('Usuario_idUsuario'))
    db.session.add(x)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateCajero/<int:idcajero>', methods=['PUT'])
def updateCajero(idcajero):
    x = db.session.get(Cajero, idcajero)
    if x is None:
        return no_encontrada('un cajero', idcajero)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = cajero_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_cajero', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(x, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteCajero/<int:idcajero>', methods=['DELETE'])
def deleteCajero(idcajero):
    x = db.session.get(Cajero, idcajero)
    if x is None:
        return no_encontrada('un cajero', idcajero)

    db.session.delete(x)

    # Si un cajero ya tiene registros relacionados la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Cajero {idcajero} eliminado'})
