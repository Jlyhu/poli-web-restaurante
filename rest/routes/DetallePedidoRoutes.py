from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.DetallePedidoModel import DetallePedido
from rest.modelos.PedidoModel import Pedido
from rest.modelos.ProductoModel import Producto
from rest.schemas.DetallePedidoSchema import DetallePedidoSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('detallepedido', __name__)
esquema = DetallePedidoSchema()


# HU-03: los productos de un pedido solo se pueden agregar, cambiar o quitar mientras esté PENDIENTE
def _pedido_no_modificable(id_pedido):
    """Devuelve una respuesta de error si el pedido no existe o ya no está PENDIENTE; si todo va bien, None."""
    pedido = db.session.get(Pedido, id_pedido)
    if pedido is None:
        return no_encontrada('un pedido', id_pedido)
    if pedido.estado != 'PENDIENTE':
        return jsonify({'error': f'El pedido {id_pedido} está {pedido.estado}: '
                                 'solo se pueden agregar, cambiar o quitar productos de un pedido PENDIENTE.'}), 409
    return None


# ---------- CONSULTAR ----------
@bp.route('/getDetallesPedido', methods=['GET'])
def listar():
    consulta = db.session.query(DetallePedido)
    # opcional: /getDetallesPedido?pedido=5  -> solo los renglones de ese pedido
    id_pedido = request.args.get('pedido', type=int)
    if id_pedido is not None:
        consulta = consulta.filter(DetallePedido.Pedido_id_pedido == id_pedido)
    registros = consulta.order_by(DetallePedido.id_detalle_pedido).all()
    return jsonify([r.toDict() for r in registros])


# HU-03 / HU-08: renglones del pedido con el nombre y el precio del producto, y el total
@bp.route('/getDetallePedidoConProducto/<int:id_pedido>', methods=['GET'])
def detalle_con_producto(id_pedido):
    if db.session.get(Pedido, id_pedido) is None:
        return no_encontrada('un pedido', id_pedido)

    filas = (db.session.query(DetallePedido, Producto)
             .select_from(DetallePedido)
             .join(Producto, Producto.idProducto == DetallePedido.Producto_idProducto)
             .filter(DetallePedido.Pedido_id_pedido == id_pedido)
             .order_by(DetallePedido.id_detalle_pedido).all())

    renglones, total = [], 0
    for d, prod in filas:
        precio = prod.precio or 0
        subtotal = precio * (d.cantidad or 0)
        total += subtotal
        renglones.append({**d.toDict(),
                          'producto_nombre': prod.nombre,
                          'precio_unitario': precio,
                          'subtotal': subtotal})
    return jsonify({'id_pedido': id_pedido, 'renglones': renglones, 'total': total})


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

    # HU-03: solo pedidos PENDIENTES
    error = _pedido_no_modificable(datos['Pedido_id_pedido'])
    if error:
        return error

    # HU-03 / HU-12: solo productos que existan y estén disponibles, y no más que las unidades que hay
    producto = db.session.get(Producto, datos['Producto_idProducto'])
    if producto is None:
        return no_encontrada('un producto', datos['Producto_idProducto'])
    if (producto.cantidad_disponible or 0) <= 0:
        return jsonify({'error': f'El producto "{producto.nombre}" está agotado.'}), 409
    if datos['cantidad'] > producto.cantidad_disponible:
        return jsonify({'error': f'Solo quedan {producto.cantidad_disponible} unidades de "{producto.nombre}".'}), 409

    notas = (datos.get('notas') or '').strip() or None

    # Si el mismo producto ya está en el pedido y sin observación distinta, se suma la cantidad
    # en vez de repetir el renglón. Con una observación distinta se crea un renglón nuevo.
    existente = (db.session.query(DetallePedido)
                 .filter(DetallePedido.Pedido_id_pedido == datos['Pedido_id_pedido'],
                         DetallePedido.Producto_idProducto == datos['Producto_idProducto'])
                 .all())
    for e in existente:
        if (e.notas or None) == notas:
            if e.cantidad + datos['cantidad'] > producto.cantidad_disponible:
                return jsonify({'error': f'Solo quedan {producto.cantidad_disponible} unidades de "{producto.nombre}".'}), 409
            e.cantidad += datos['cantidad']
            error = guardar_cambios()
            if error:
                return error
            return jsonify(e.toDict()), 200

    nuevo_id = datos.get('id_detalle_pedido')
    if nuevo_id is None:
        nuevo_id = siguiente_id(DetallePedido.id_detalle_pedido)

    r = DetallePedido(id_detalle_pedido=nuevo_id,
            cantidad=datos.get('cantidad'),
            notas=notas,
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
    datos.pop('Pedido_id_pedido', None)    # un renglón no se pasa a otro pedido
    error = _pedido_no_modificable(r.Pedido_id_pedido)
    if error:
        return error
    if 'notas' in datos:
        datos['notas'] = (datos['notas'] or '').strip() or None
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

    error = _pedido_no_modificable(r.Pedido_id_pedido)
    if error:
        return error

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'DetallePedido {id_detalle_pedido} eliminado'})
