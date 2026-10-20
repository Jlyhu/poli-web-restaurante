# ============================================================
# CajeroDAO.py
# Capa de acceso a datos (DAO) para la entidad Cajero, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Cajero'
# ============================================================

from orm.modelos.CajeroModel import Cajero
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: CajeroDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = CajeroDAO(session)
# ------------------------------------------------------------
class CajeroDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un cajero nuevo. El usuario (tabla Usuario) debe existir antes.
    # Retorna:
    #   Cajero -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_cajero, id_usuario):
        nuevo = Cajero(
            id_cajero=id_cajero,
            Usuario_idUsuario=id_usuario,
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria
    # Retorna:
    #   Cajero | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_cajero):
        return self.db.query(Cajero).filter(Cajero.id_cajero == id_cajero).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Cajero
    # Retorna:
    #   list[Cajero] -- Lista de objetos (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Cajero).order_by(Cajero.id_cajero).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de un cajero existente
    # Retorna:
    #   Cajero | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, id_cajero, id_usuario):
        cajero = self.obtener_por_id(id_cajero)
        if cajero:
            cajero.Usuario_idUsuario = id_usuario
            self.db.commit()
        return cajero

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un cajero por su ID
    # (falla si otras tablas dependen de este registro)
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_cajero):
        cajero = self.obtener_por_id(id_cajero)
        if cajero:
            self.db.delete(cajero)
            self.db.commit()
            return True
        return False
