# ============================================================
# MeseroDAO.py
# Capa de acceso a datos (DAO) para la entidad Mesero, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Mesero'
# ============================================================

from orm.modelos.MeseroModel import Mesero
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: MeseroDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = MeseroDAO(session)
# ------------------------------------------------------------
class MeseroDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un mesero nuevo. El usuario (tabla Usuario) debe existir antes.
    # Retorna:
    #   Mesero -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_mesero, zona_asignada, id_usuario):
        nuevo = Mesero(
            id_mesero=id_mesero,
            zona_asignada=zona_asignada,
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
    #   Mesero | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_mesero):
        return self.db.query(Mesero).filter(Mesero.id_mesero == id_mesero).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Mesero
    # Retorna:
    #   list[Mesero] -- Lista de objetos (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Mesero).order_by(Mesero.id_mesero).all()

    # --------------------------------------------------------
    # Método: obtener_por_usuario
    # Busca el mesero que corresponde a un usuario
    # Retorna:
    #   Mesero | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_usuario(self, id_usuario):
        return self.db.query(Mesero).filter(Mesero.Usuario_idUsuario == id_usuario).first()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de un mesero existente
    # Retorna:
    #   Mesero | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, id_mesero, nueva_zona, id_usuario):
        mesero = self.obtener_por_id(id_mesero)
        if mesero:
            mesero.zona_asignada = nueva_zona
            mesero.Usuario_idUsuario = id_usuario
            self.db.commit()
        return mesero

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un mesero por su ID
    # (falla si otras tablas dependen de este registro)
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_mesero):
        mesero = self.obtener_por_id(id_mesero)
        if mesero:
            self.db.delete(mesero)
            self.db.commit()
            return True
        return False
