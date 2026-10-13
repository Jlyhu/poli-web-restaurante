# ============================================================
# CocineroDAO.py
# Capa de acceso a datos (DAO) para la entidad Cocinero, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Cocinero'
# ============================================================

from orm.modelos.CocineroModel import Cocinero
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: CocineroDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = CocineroDAO(session)
# ------------------------------------------------------------
class CocineroDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo registro.
    # Falla si el id ya existe o si una llave foránea no existe.
    # Retorna: Cocinero -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_cocinero, estacion, Usuario_idUsuario):
        nuevo = Cocinero(
            id_cocinero=id_cocinero,
            estacion=estacion,
            Usuario_idUsuario=Usuario_idUsuario
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Retorna: Cocinero -- El objeto encontrado, o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_cocinero):
        return self.db.query(Cocinero).filter(Cocinero.id_cocinero == id_cocinero).first()

    # --------------------------------------------------------
    # Método: obtener_por_estacion
    # Busca por estación.
    # Retorna: list[Cocinero] -- Lista de registros encontrados (puede estar vacía)
    # --------------------------------------------------------
    def obtener_por_estacion(self, valor):
        return self.db.query(Cocinero).filter(Cocinero.estacion == valor).all()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros.
    # Retorna: list[Cocinero]
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Cocinero).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica un registro existente (el id no se modifica).
    # Retorna: Cocinero -- El objeto actualizado, o None si no existe
    # --------------------------------------------------------
    def actualizar(self, id_cocinero, estacion, Usuario_idUsuario):
        registro = self.obtener_por_id(id_cocinero)
        if registro:
            registro.estacion = estacion
            registro.Usuario_idUsuario = Usuario_idUsuario
            self.db.commit()
        return registro

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un registro.
    # Falla si otros registros dependen de él (llave foránea).
    # Retorna: bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_cocinero):
        registro = self.obtener_por_id(id_cocinero)
        if registro:
            self.db.delete(registro)
            self.db.commit()
            return True
        return False
