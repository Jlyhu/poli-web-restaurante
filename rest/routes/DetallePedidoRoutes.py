from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.DetallePedidoModel import DetallePedido
from rest.schemas.DetallePedidoSchema import DetallePedidoSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('detallepedido', __name__)
esquema = DetallePedidoSchema()


# ---------- CONSULTAR ----------
@bp.route('/getDetallesPedido', methods=['GET'])
def listar():
    registros = db.session.query(DetallePedido).order_by(DetallePedido.id_detalle_pedido).all()
    return jsonify([r.toDict() for r in registros])


@bp.route('/getDetallePedido/<int:id_detalle_pedido>', methods=['GET'])
def obtener(id_detalle_pedido):
    r = db.session.get(DetallePedido, id_detalle_pedido)
    if r is None:
        return no_encontrada('un detalle de pedido', id_detalle_pedido)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertDetallePedido', methods=['POST'])
def insertar():
    try:
        datos = esquema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_id = datos.get('id_detalle_pedido')
    if nuevo_id is None:
        nuevo_id = siguiente_id(DetallePedido.id_detalle_pedido)

    r = DetallePedido(id_detalle_pedido=nuevo_id,
            cantidad=datos.get('cantidad'),
            notas=datos.get('notas'),
            Pedido_id_pedido=datos.get('Pedido_id_pedido'),
            Producto_idProducto=datos.get('Producto_idProducto'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateDetallePedido/<int:id_detalle_pedido>', methods=['PUT'])
def actualizar(id_detalle_pedido):
    r = db.session.get(DetallePedido, id_detalle_pedido)
    if r is None:
        return no_encontrada('un detalle de pedido', id_detalle_pedido)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = esquema.load(request.get_json(silent=True) or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_detalle_pedido', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteDetallePedido/<int:id_detalle_pedido>', methods=['DELETE'])
def eliminar(id_detalle_pedido):
    r = db.session.get(DetallePedido, id_detalle_pedido)
    if r is None:
        return no_encontrada('un detalle de pedido', id_detalle_pedido)

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'DetallePedido {id_detalle_pedido} eliminado'})
