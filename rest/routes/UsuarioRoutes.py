from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.UsuarioModel import Usuario
from rest.schemas.UsuarioSchema import UsuarioSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('usuario', __name__)
usuario_schema = UsuarioSchema()

# ---------- CONSULTAR ----------
@bp.route('/getUsuarios', methods=['GET'])
def usuarios():
    # opcional: /getUsuarios?estado=inactivo
    consulta = db.session.query(Usuario)
    estado = request.args.get('estado')
    if estado:
        consulta = consulta.filter(Usuario.estado == estado)
    misU = consulta.order_by(Usuario.idUsuario).all()
    return jsonify([u.toDict() for u in misU])


@bp.route('/getUsuario/<int:idusuario>', methods=['GET'])
def usuario(idusuario):
    u = db.session.get(Usuario, idusuario)
    if u is None:
        return no_encontrada('un usuario', idusuario)
    return jsonify(u.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertUsuario', methods=['POST'])
def insertUsuario():
    try:
        datos = usuario_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idusuario = datos.get('idUsuario')
    if idusuario is None:
        idusuario = siguiente_id(Usuario.idUsuario)

    u = Usuario(idUsuario=idusuario,
                nombre=datos.get('nombre'),
                credenciales=datos.get('credenciales'))
    db.session.add(u)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(u.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateUsuario/<int:idusuario>', methods=['PUT'])
def updateUsuario(idusuario):
    u = db.session.get(Usuario, idusuario)
    if u is None:
        return no_encontrada('un usuario', idusuario)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = usuario_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('idUsuario', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(u, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(u.toDict())


# ---------- DESACTIVAR / ACTIVAR ----------
@bp.route('/desactivarUsuario/<int:idusuario>', methods=['PUT'])
def desactivarUsuario(idusuario):
    # El usuario no podrá iniciar sesión, pero no se borra: su información se conserva
    u = db.session.get(Usuario, idusuario)
    if u is None:
        return no_encontrada('un usuario', idusuario)
    u.estado = 'inactivo'

    error = guardar_cambios()
    if error:
        return error
    return jsonify(u.toDict())


@bp.route('/activarUsuario/<int:idusuario>', methods=['PUT'])
def activarUsuario(idusuario):
    u = db.session.get(Usuario, idusuario)
    if u is None:
        return no_encontrada('un usuario', idusuario)
    u.estado = 'activo'

    error = guardar_cambios()
    if error:
        return error
    return jsonify(u.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteUsuario/<int:idusuario>', methods=['DELETE'])
def deleteUsuario(idusuario):
    u = db.session.get(Usuario, idusuario)
    if u is None:
        return no_encontrada('un usuario', idusuario)

    db.session.delete(u)

    # Si el usuario ya tiene registros relacionados (por ejemplo, es mesero) la base lo
    # impide (409): en ese caso se desactiva en vez de eliminarlo
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Usuario {idusuario} eliminado'})
