from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.CocineroModel import Cocinero
from rest.schemas.CocineroSchema import CocineroSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('cocinero', __name__)
esquema = CocineroSchema()


# ---------- CONSULTAR ----------
@bp.route('/getCocineros', methods=['GET'])
def listar():
    registros = db.session.query(Cocinero).order_by(Cocinero.id_cocinero).all()
    return jsonify([r.toDict() for r in registros])


@bp.route('/getCocinero/<int:id_cocinero>', methods=['GET'])
def obtener(id_cocinero):
    r = db.session.get(Cocinero, id_cocinero)
    if r is None:
        return no_encontrada('un cocinero', id_cocinero)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertCocinero', methods=['POST'])
def insertar():
    try:
        datos = esquema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_id = datos.get('id_cocinero')
    if nuevo_id is None:
        nuevo_id = siguiente_id(Cocinero.id_cocinero)

    r = Cocinero(id_cocinero=nuevo_id,
            estacion=datos.get('estacion'),
            Usuario_idUsuario=datos.get('Usuario_idUsuario'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateCocinero/<int:id_cocinero>', methods=['PUT'])
def actualizar(id_cocinero):
    r = db.session.get(Cocinero, id_cocinero)
    if r is None:
        return no_encontrada('un cocinero', id_cocinero)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = esquema.load(request.get_json(silent=True) or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_cocinero', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteCocinero/<int:id_cocinero>', methods=['DELETE'])
def eliminar(id_cocinero):
    r = db.session.get(Cocinero, id_cocinero)
    if r is None:
        return no_encontrada('un cocinero', id_cocinero)

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Cocinero {id_cocinero} eliminado'})
