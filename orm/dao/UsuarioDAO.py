# ============================================================
# UsuarioDAO.py
# Capa de acceso a datos (DAO) para la entidad Usuario, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Usuario'
# ============================================================

from orm.modelos.UsuarioModel import Usuario
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: UsuarioDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = UsuarioDAO(session)
# ------------------------------------------------------------
class UsuarioDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo usuario (queda con estado 'activo')
    # Parámetros:
    #   idusuario (int/str) -- Identificador único del usuario
    #   nombre (str) -- Nombre del usuario
    #   credenciales (str) -- Contraseña o token de acceso
    # Retorna:
    #   Usuario -- El objeto recién creado y persistido
    # Ejemplo:
    #   u = dao.crear(1, "ana", "1234")
    # --------------------------------------------------------
    def crear(self, idusuario, nombre, credenciales):
        nuevo_usuario = Usuario(
            idUsuario=idusuario,
            nombre=nombre,
            credenciales=credenciales
        )
        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)  # sincroniza el objeto con los datos de la BD
        return nuevo_usuario

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca un usuario por su clave primaria
    # Parámetros:
    #   idusuario (int/str) -- Identificador único del usuario
    # Retorna:
    #   Usuario | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, idusuario):
        return self.db.query(Usuario).filter(Usuario.idUsuario == idusuario).first()

    # --------------------------------------------------------
    # Método: obtener_por_nombre
    # Busca el primer usuario que coincida con el nombre dado
    # Parámetros:
    #   nombre (str) -- Nombre del usuario a buscar
    # Retorna:
    #   Usuario | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_nombre(self, nombre):
        return self.db.query(Usuario).filter(Usuario.nombre == nombre).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Usuario
    # Parámetros: ninguno
    # Retorna:
    #   list[Usuario] -- Lista de objetos Usuario (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Usuario).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica el nombre y las credenciales de un usuario existente
    # Parámetros:
    #   idusuario (int/str) -- Identificador único del usuario a actualizar
    #   nuevo_nombre (str) -- Nuevo nombre para el usuario
    #   nuevas_credenciales (str) -- Nuevas credenciales para el usuario
    # Retorna:
    #   Usuario | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, idusuario, nuevo_nombre, nuevas_credenciales):
        usuario = self.obtener_por_id(idusuario)
        if usuario:
            usuario.nombre       = nuevo_nombre
            usuario.credenciales = nuevas_credenciales
            self.db.commit()
        return usuario

    # --------------------------------------------------------
    # Método: desactivar  (HU-13)
    # Cambia el estado a 'inactivo' SIN borrar el usuario, para
    # conservar su información y todo lo que haya registrado
    # Parámetros:
    #   idusuario (int/str) -- Identificador único del usuario a desactivar
    # Retorna:
    #   Usuario | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def desactivar(self, idusuario):
        usuario = self.obtener_por_id(idusuario)
        if usuario:
            usuario.estado = 'inactivo'
            self.db.commit()
        return usuario

    # --------------------------------------------------------
    # Método: activar  (HU-13)
    # Cambia el estado a 'activo'
    # Parámetros:
    #   idusuario (int/str) -- Identificador único del usuario a activar
    # Retorna:
    #   Usuario | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def activar(self, idusuario):
        usuario = self.obtener_por_id(idusuario)
        if usuario:
            usuario.estado = 'activo'
            self.db.commit()
        return usuario

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un usuario de la base de datos por su ID
    # (falla si otras tablas dependen de él: en ese caso, desactivarlo)
    # Parámetros:
    #   idusuario (int/str) -- Identificador único del usuario a eliminar
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, idusuario):
        usuario = self.obtener_por_id(idusuario)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False
