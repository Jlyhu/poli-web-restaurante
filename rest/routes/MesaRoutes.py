from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.MesaModel import Mesa
from rest.schemas.MesaSchema import MesaSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('mesa', __name__)
mesa_schema = MesaSchema()


# ---------- CONSULTAR ----------
@bp.route('/getMesas', methods=['GET'])
def mesas():
    misM = db.session.query(Mesa).order_by(Mesa.id_mesa).all()
    return jsonify([m.toDict() for m in misM])


@bp.route('/getMesa/<int:idmesa>', methods=['GET'])
def mesa(idmesa):
    m = db.session.get(Mesa, idmesa)
    if m is None:
        return no_encontrada('una mesa', idmesa)
    return jsonify(m.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertMesa', methods=['POST'])
def insertMesa():
    try:
        datos = mesa_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idmesa = datos.get('id_mesa')
    if idmesa is None:
        idmesa = siguiente_id(Mesa.id_mesa)

    m = Mesa(id_mesa=idmesa,
            numero=datos.get('numero'),
            estado=datos.get('estado', 'Disponible'))
    db.session.add(m)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(m.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateMesa/<int:idmesa>', methods=['PUT'])
def updateMesa(idmesa):
    m = db.session.get(Mesa, idmesa)
    if m is None:
        return no_encontrada('una mesa', idmesa)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = mesa_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_mesa', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(m, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(m.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteMesa/<int:idmesa>', methods=['DELETE'])
def deleteMesa(idmesa):
    m = db.session.get(Mesa, idmesa)
    if m is None:
        return no_encontrada('una mesa', idmesa)

    db.session.delete(m)

    # Si la mesa ya está en una reservación o en un pedido la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Mesa {idmesa} eliminada'})
