from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.PedidoMesaModel import PedidoMesa
from rest.schemas.PedidoMesaSchema import PedidoMesaSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('pedidomesa', __name__)
esquema = PedidoMesaSchema()


# ---------- CONSULTAR ----------
@bp.route('/getPedidosMesa', methods=['GET'])
def listar():
    registros = db.session.query(PedidoMesa).order_by(PedidoMesa.id_pedido_mesa).all()
    return jsonify([r.toDict() for r in registros])


@bp.route('/getPedidoMesa/<int:id_pedido_mesa>', methods=['GET'])
def obtener(id_pedido_mesa):
    r = db.session.get(PedidoMesa, id_pedido_mesa)
    if r is None:
        return no_encontrada('un pedido de mesa', id_pedido_mesa)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertPedidoMesa', methods=['POST'])
def insertar():
    try:
        datos = esquema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_id = datos.get('id_pedido_mesa')
    if nuevo_id is None:
        nuevo_id = siguiente_id(PedidoMesa.id_pedido_mesa)

    r = PedidoMesa(id_pedido_mesa=nuevo_id,
            Mesa_id_mesa=datos.get('Mesa_id_mesa'),
            Pedido_id_pedido=datos.get('Pedido_id_pedido'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updatePedidoMesa/<int:id_pedido_mesa>', methods=['PUT'])
def actualizar(id_pedido_mesa):
    r = db.session.get(PedidoMesa, id_pedido_mesa)
    if r is None:
        return no_encontrada('un pedido de mesa', id_pedido_mesa)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = esquema.load(request.get_json(silent=True) or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_pedido_mesa', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deletePedidoMesa/<int:id_pedido_mesa>', methods=['DELETE'])
def eliminar(id_pedido_mesa):
    r = db.session.get(PedidoMesa, id_pedido_mesa)
    if r is None:
        return no_encontrada('un pedido de mesa', id_pedido_mesa)

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'PedidoMesa {id_pedido_mesa} eliminado'})
