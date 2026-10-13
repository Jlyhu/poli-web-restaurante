from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.PedidoModel import Pedido
from rest.schemas.PedidoSchema import PedidoSchema, CambiarEstadoPedidoSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('pedido', __name__)
pedido_schema = PedidoSchema()


# ---------- CONSULTAR ----------
@bp.route('/getPedidos', methods=['GET'])
def pedidos():
    consulta = db.session.query(Pedido)
    # opcionales: /getPedidos?estado=PENDIENTE   y   /getPedidos?mesero=2
    estado = request.args.get('estado')
    if estado:
        consulta = consulta.filter(Pedido.estado == estado)
    idmesero = request.args.get('mesero', type=int)
    if idmesero is not None:
        consulta = consulta.filter(Pedido.Mesero_id_mesero == idmesero)
    mis = consulta.order_by(Pedido.id_pedido).all()
    return jsonify([x.toDict() for x in mis])


@bp.route('/getPedido/<int:idpedido>', methods=['GET'])
def pedido(idpedido):
    x = db.session.get(Pedido, idpedido)
    if x is None:
        return no_encontrada('un pedido', idpedido)
    return jsonify(x.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertPedido', methods=['POST'])
def insertPedido():
    try:
        datos = pedido_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idpedido = datos.get('id_pedido')
    if idpedido is None:
        idpedido = siguiente_id(Pedido.id_pedido)

    x = Pedido(id_pedido=idpedido,
               estado='PENDIENTE',
               fecha_creacion=datetime.now(),
               fecha_ultima_actualizacion=datetime.now(),
               tipo_pedido=datos.get('tipo_pedido'),
               Mesero_id_mesero=datos.get('Mesero_id_mesero'),
               Repartidor_id_repartidor=datos.get('Repartidor_id_repartidor'),
               Cliente_id_cliente=datos.get('Cliente_id_cliente'))
    db.session.add(x)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updatePedido/<int:idpedido>', methods=['PUT'])
def updatePedido(idpedido):
    x = db.session.get(Pedido, idpedido)
    if x is None:
        return no_encontrada('un pedido', idpedido)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = pedido_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_pedido', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(x, campo, valor)
    x.fecha_ultima_actualizacion = datetime.now()

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- CAMBIAR ESTADO ----------
# Flujo del pedido: PENDIENTE -> EN PREPARACION -> LISTO -> ENTREGADO
# CANCELADO solo puede ocurrir desde PENDIENTE o EN PREPARACION (nunca si ya fue entregado)
TRANSICIONES = {
    'PENDIENTE': ['EN PREPARACION', 'CANCELADO'],
    'EN PREPARACION': ['LISTO', 'CANCELADO'],
    'LISTO': ['ENTREGADO'],
    'ENTREGADO': [],
    'CANCELADO': [],
}


@bp.route('/cambiarEstadoPedido/<int:idpedido>', methods=['PUT'])
def cambiarEstadoPedido(idpedido):
    x = db.session.get(Pedido, idpedido)
    if x is None:
        return no_encontrada('un pedido', idpedido)

    try:
        datos = CambiarEstadoPedidoSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo = datos['estado']
    permitidos = TRANSICIONES.get(x.estado, [])
    if nuevo not in permitidos:
        return jsonify({'error': f'No se puede pasar de {x.estado} a {nuevo}',
                        'estados_permitidos': permitidos}), 409

    x.estado = nuevo
    x.fecha_ultima_actualizacion = datetime.now()

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deletePedido/<int:idpedido>', methods=['DELETE'])
def deletePedido(idpedido):
    x = db.session.get(Pedido, idpedido)
    if x is None:
        return no_encontrada('un pedido', idpedido)

    db.session.delete(x)

    # Si un pedido ya tiene registros relacionados la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Pedido {idpedido} eliminado'})
