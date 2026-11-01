from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError                        # CAMBIO: para mostrar la causa real de error al guardar el rol

from rest import db
from rest.modelos.UsuarioModel import Usuario
from rest.modelos.MeseroModel import Mesero                       # CAMBIO: Agrega el modelo Mesero para poder crear la fila de rol
from rest.modelos.RepartidorModel import Repartidor               # CAMBIO: Agrega el modelo Repartidor para poder crear la fila de rol
from rest.modelos.CocineroModel import Cocinero                   # CAMBIO: Agrega el modelo Cocinero para poder crear la fila de rol
from rest.modelos.CajeroModel import Cajero                       # CAMBIO: Agrega el modelo Cajero para poder crear la fila de rol
from rest.modelos.AdministradorModel import Administrador         # CAMBIO: Agrega el modelo Administrador para poder crear la fila de rol
from rest.schemas.UsuarioSchema import UsuarioSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('usuario', __name__)
usuario_schema = UsuarioSchema()


# ---------- CAMBIO: apoyo para los roles ----------
# rol -> (clase, columna del id, columna del dato extra o None si no tiene)
ROLES = {
    'Mesero':        (Mesero,        'id_mesero',        'zona_asignada'),
    'Repartidor':    (Repartidor,    'id_repartidor',    'placa_vehiculo'),
    'Cocinero':      (Cocinero,      'id_cocinero',      'estacion'),
    'Cajero':        (Cajero,        'id_cajero',        None),
    'Administrador': (Administrador, 'id_administrador', None),
}


def _fila_rol(idusuario):
    """Busca en qué tabla de rol está el usuario. Devuelve (rol, fila) o (None, None)."""
    for rol, (clase, _, _) in ROLES.items():
        fila = db.session.query(clase).filter(clase.Usuario_idUsuario == idusuario).first()
        if fila is not None:
            return rol, fila
    return None, None


def _roles_por_usuario():
    """Lee las 5 tablas de rol una sola vez: {idUsuario: (rol, dato)}."""
    mapa = {}
    for rol, (clase, _, col_dato) in ROLES.items():
        for fila in db.session.query(clase).all():
            mapa[fila.Usuario_idUsuario] = (rol, getattr(fila, col_dato) if col_dato else None)
    return mapa


def _crear_fila_rol(idusuario, rol, dato):
    """Crea la fila del rol (el id se asigna con siguiente_id, como en las demás tablas)."""
    clase, col_id, col_dato = ROLES[rol]
    campos = {col_id: siguiente_id(getattr(clase, col_id)),
            'Usuario_idUsuario': idusuario}
    if col_dato:
        campos[col_dato] = dato or None
    db.session.add(clase(**campos))
    db.session.flush()


def _error_rol(e):                                                # CAMBIO: recibe el error
    # CAMBIO: muestra la causa real que reportó la base de datos
    detalle = str(getattr(e, 'orig', None) or e)
    return jsonify({'error': f'No se pudo guardar el rol: {detalle}'}), 409


# ---------- CONSULTAR ----------
@bp.route('/getUsuarios', methods=['GET'])
def usuarios():
    # opcional: /getUsuarios?estado=inactivo
    consulta = db.session.query(Usuario)
    estado = request.args.get('estado')
    if estado:
        consulta = consulta.filter(Usuario.estado == estado)
    misU = consulta.order_by(Usuario.idUsuario).all()

    # NUEVO: a cada usuario se le agregan rol y datoRol (None si no tiene fila de rol)
    roles = _roles_por_usuario()
    resultado = []
    for u in misU:
        d = u.toDict()
        d['rol'], d['datoRol'] = roles.get(u.idUsuario, (None, None))
        resultado.append(d)
    return jsonify(resultado)


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

    # NUEVO: si llegó un rol, se crea también su fila (en la misma transacción)
    rol = datos.get('rol')
    if rol:
        try:
            db.session.flush()   # el usuario debe existir antes que su fila de rol
            _crear_fila_rol(idusuario, rol, datos.get('datoRol'))
        except SQLAlchemyError as e:                              # CAMBIO
            db.session.rollback()
            return _error_rol(e)                                  # CAMBIO

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

    # NUEVO: rol y datoRol no son columnas de Usuario, se sacan antes del for
    rol_nuevo = datos.pop('rol', None)
    hay_dato = 'datoRol' in datos
    dato = datos.pop('datoRol', None)

    for campo, valor in datos.items():
        setattr(u, campo, valor)

    # NUEVO: si llegó un rol, se crea, se actualiza o se cambia su fila
    if rol_nuevo:
        try:
            rol_actual, fila = _fila_rol(idusuario)
            if rol_nuevo == rol_actual:
                col_dato = ROLES[rol_nuevo][2]
                if col_dato and hay_dato:
                    setattr(fila, col_dato, dato or None)
            else:
                # cambió de rol (o no tenía): se borra la fila anterior y se crea la nueva
                if fila is not None:
                    db.session.delete(fila)
                    db.session.flush()
                _crear_fila_rol(idusuario, rol_nuevo, dato)
        except SQLAlchemyError as e:                              # CAMBIO
            db.session.rollback()
            return _error_rol(e)                                  # CAMBIO

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

    # NUEVO: primero se borra la fila del rol (si tiene), por la llave foránea
    _, fila = _fila_rol(idusuario)
    if fila is not None:
        try:
            db.session.delete(fila)
            db.session.flush()
        except SQLAlchemyError as e:                              # CAMBIO
            db.session.rollback()
            return _error_rol(e)                                  # CAMBIO

    db.session.delete(u)

    # Si el usuario ya tiene registros relacionados (por ejemplo, es mesero) la base lo
    # impide (409): en ese caso se desactiva en vez de eliminarlo
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Usuario {idusuario} eliminado'})

# ---------- INICIAR SESIÓN ----------
@bp.route('/loginUsuario', methods=['POST'])
def loginUsuario():
    datos = request.get_json()
    
    if not datos:
        return jsonify({"error": "No se enviaron datos"}), 400

    # Estas claves ('nombre' y 'contrasena') deben ser las mismas que envías desde el fetch en JavaScript
    nombre_usuario = datos.get('nombre') 
    contrasena_ingresada = datos.get('credenciales')

    if not nombre_usuario or not contrasena_ingresada:
        return jsonify({"error": "Faltan credenciales"}), 400

    try:
        # Busca al usuario en la base de datos por su nombre
        u = db.session.query(Usuario).filter(Usuario.nombre == nombre_usuario).first()
        
        # Verifica si existe y si las credenciales coinciden
        if u and u.credenciales == contrasena_ingresada:
            
            # Obtiene el diccionario del usuario (toDict oculta la contraseña automáticamente)
            datos_usuario = u.toDict()
            
            # Opcional: Agregar el rol al usuario que inicia sesión (usando tu función existente)
            rol_actual, _ = _fila_rol(u.idUsuario)
            datos_usuario['rol'] = rol_actual
            
            return jsonify({
                "mensaje": "Inicio de sesión exitoso", 
                "usuario": datos_usuario 
            }), 200
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
            
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500