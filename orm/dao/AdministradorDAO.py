# ============================================================
# AdministradorDAO.py
# Capa de acceso a datos (DAO) para la entidad Administrador, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Administrador'
# ============================================================

from orm.modelos.AdministradorModel import Administrador
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: AdministradorDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = AdministradorDAO(session)
# ------------------------------------------------------------
class AdministradorDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo registro.
    # Falla si el id ya existe o si una llave foránea no existe.
    # Retorna: Administrador -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_administrador, Usuario_idUsuario):
        nuevo = Administrador(
            id_administrador=id_administrador,
            Usuario_idUsuario=Usuario_idUsuario
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Retorna: Administrador -- El objeto encontrado, o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_administrador):
        return self.db.query(Administrador).filter(Administrador.id_administrador == id_administrador).first()

    # --------------------------------------------------------
    # Método: obtener_por_usuario
    # Busca por id de usuario.
    # Retorna: list[Administrador] -- Lista de registros encontrados (puede estar vacía)
    # --------------------------------------------------------
    def obtener_por_usuario(self, valor):
        return self.db.query(Administrador).filter(Administrador.Usuario_idUsuario == valor).all()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros.
    # Retorna: list[Administrador]
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Administrador).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica un registro existente (el id no se modifica).
    # Retorna: Administrador -- El objeto actualizado, o None si no existe
    # --------------------------------------------------------
    def actualizar(self, id_administrador, Usuario_idUsuario):
        registro = self.obtener_por_id(id_administrador)
        if registro:
            registro.Usuario_idUsuario = Usuario_idUsuario
            self.db.commit()
        return registro

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un registro.
    # Falla si otros registros dependen de él (llave foránea).
    # Retorna: bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_administrador):
        registro = self.obtener_por_id(id_administrador)
        if registro:
            self.db.delete(registro)
            self.db.commit()
            return True
        return False
