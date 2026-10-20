from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.AdministradorModel import Administrador
from rest.schemas.AdministradorSchema import AdministradorSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('administrador', __name__)
esquema = AdministradorSchema()


# ---------- CONSULTAR ----------
@bp.route('/getAdministradores', methods=['GET'])
def listar():
    registros = db.session.query(Administrador).order_by(Administrador.id_administrador).all()
    return jsonify([r.toDict() for r in registros])


@bp.route('/getAdministrador/<int:id_administrador>', methods=['GET'])
def obtener(id_administrador):
    r = db.session.get(Administrador, id_administrador)
    if r is None:
        return no_encontrada('un administrador', id_administrador)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertAdministrador', methods=['POST'])
def insertar():
    try:
        datos = esquema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_id = datos.get('id_administrador')
    if nuevo_id is None:
        nuevo_id = siguiente_id(Administrador.id_administrador)

    r = Administrador(id_administrador=nuevo_id,
            Usuario_idUsuario=datos.get('Usuario_idUsuario'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateAdministrador/<int:id_administrador>', methods=['PUT'])
def actualizar(id_administrador):
    r = db.session.get(Administrador, id_administrador)
    if r is None:
        return no_encontrada('un administrador', id_administrador)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = esquema.load(request.get_json(silent=True) or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_administrador', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteAdministrador/<int:id_administrador>', methods=['DELETE'])
def eliminar(id_administrador):
    r = db.session.get(Administrador, id_administrador)
    if r is None:
        return no_encontrada('un administrador', id_administrador)

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Administrador {id_administrador} eliminado'})
