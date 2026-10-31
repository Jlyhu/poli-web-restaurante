from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.CategoriaModel import Categoria
from rest.schemas.CategoriaSchema import CategoriaSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('categoria', __name__)
categoria_schema = CategoriaSchema()


# ---------- CONSULTAR ----------
@bp.route('/getCategorias', methods=['GET'])
def categorias():
    consulta = db.session.query(Categoria)

    mis = consulta.order_by(Categoria.id_categoria).all()
    return jsonify([x.toDict() for x in mis])


@bp.route('/getCategoria/<int:idcategoria>', methods=['GET'])
def categoria(idcategoria):
    x = db.session.get(Categoria, idcategoria)
    if x is None:
        return no_encontrada('una categoría', idcategoria)
    return jsonify(x.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertCategoria', methods=['POST'])
def insertCategoria():
    try:
        datos = categoria_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idcategoria = datos.get('id_categoria')
    if idcategoria is None:
        idcategoria = siguiente_id(Categoria.id_categoria)

    x = Categoria(id_categoria=idcategoria,
                  nombre=datos.get('nombre'))
    db.session.add(x)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateCategoria/<int:idcategoria>', methods=['PUT'])
def updateCategoria(idcategoria):
    x = db.session.get(Categoria, idcategoria)
    if x is None:
        return no_encontrada('una categoría', idcategoria)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = categoria_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_categoria', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(x, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteCategoria/<int:idcategoria>', methods=['DELETE'])
def deleteCategoria(idcategoria):
    x = db.session.get(Categoria, idcategoria)
    if x is None:
        return no_encontrada('una categoría', idcategoria)

    db.session.delete(x)

    # Si una categoría ya tiene registros relacionados la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Categoria {idcategoria} eliminado'})
