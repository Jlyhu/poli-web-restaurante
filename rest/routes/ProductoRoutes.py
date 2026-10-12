from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.ProductoModel import Producto
from rest.schemas.ProductoSchema import ProductoSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('producto', __name__)
producto_schema = ProductoSchema()


# ---------- CONSULTAR ----------
@bp.route('/getProductos', methods=['GET'])
def productos():
    misP = db.session.query(Producto).order_by(Producto.idProducto).all()
    return jsonify([p.toDict() for p in misP])


@bp.route('/getProductosDisponibles', methods=['GET'])
def productosDisponibles():
    # HU-12: solo los productos con unidades disponibles (los que un mesero puede agregar a un pedido)
    misP = db.session.query(Producto).filter(Producto.cantidad_disponible > 0).order_by(Producto.idProducto).all()
    return jsonify([p.toDict() for p in misP])


@bp.route('/getProducto/<int:idproducto>', methods=['GET'])
def producto(idproducto):
    p = db.session.get(Producto, idproducto)
    if p is None:
        return no_encontrada('un producto', idproducto)
    return jsonify(p.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertProducto', methods=['POST'])
def insertProducto():
    try:
        datos = producto_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idproducto = datos.get('idProducto')
    if idproducto is None:
        idproducto = siguiente_id(Producto.idProducto)

    p = Producto(idProducto=idproducto,
                 nombre=datos.get('nombre'),
                 descripcion=datos.get('descripcion'),
                 precio=datos.get('precio'),
                 cantidad_disponible=datos.get('cantidad_disponible', 0),
                 Categoria_id_categoria=datos.get('Categoria_id_categoria'))
    db.session.add(p)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(p.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateProducto/<int:idproducto>', methods=['PUT'])
def updateProducto(idproducto):
    p = db.session.get(Producto, idproducto)
    if p is None:
        return no_encontrada('un producto', idproducto)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = producto_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('idProducto', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(p, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(p.toDict())


# ---------- AGOTAR (HU-12) ----------
@bp.route('/agotarProducto/<int:idproducto>', methods=['PUT'])
def agotarProducto(idproducto):
    # Deja la cantidad disponible en 0: el producto deja de aparecer en /getProductosDisponibles.
    # Para volver a venderlo, se actualiza la cantidad con /updateProducto.
    p = db.session.get(Producto, idproducto)
    if p is None:
        return no_encontrada('un producto', idproducto)
    p.cantidad_disponible = 0

    error = guardar_cambios()
    if error:
        return error
    return jsonify(p.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteProducto/<int:idproducto>', methods=['DELETE'])
def deleteProducto(idproducto):
    p = db.session.get(Producto, idproducto)
    if p is None:
        return no_encontrada('un producto', idproducto)

    db.session.delete(p)

    # Si el producto ya está en algún pedido la base lo impide (409): en ese caso se marca como agotado
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Producto {idproducto} eliminado'})
