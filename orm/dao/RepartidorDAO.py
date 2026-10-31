# ============================================================
# RepartidorDAO.py
# Capa de acceso a datos (DAO) para la entidad Repartidor, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Repartidor'
# ============================================================

from orm.modelos.RepartidorModel import Repartidor
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: RepartidorDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = RepartidorDAO(session)
# ------------------------------------------------------------
class RepartidorDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un repartidor nuevo. El usuario (tabla Usuario) debe existir antes.
    # Retorna:
    #   Repartidor -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_repartidor, placa_vehiculo, id_usuario):
        nuevo = Repartidor(
            id_repartidor=id_repartidor,
            placa_vehiculo=placa_vehiculo,
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
    #   Repartidor | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_repartidor):
        return self.db.query(Repartidor).filter(Repartidor.id_repartidor == id_repartidor).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Repartidor
    # Retorna:
    #   list[Repartidor] -- Lista de objetos (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Repartidor).order_by(Repartidor.id_repartidor).all()

    # --------------------------------------------------------
    # Método: obtener_por_usuario
    # Busca el repartidor que corresponde a un usuario
    # Retorna:
    #   Repartidor | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_usuario(self, id_usuario):
        return self.db.query(Repartidor).filter(Repartidor.Usuario_idUsuario == id_usuario).first()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de un repartidor existente
    # Retorna:
    #   Repartidor | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, id_repartidor, nueva_placa, id_usuario):
        repartidor = self.obtener_por_id(id_repartidor)
        if repartidor:
            repartidor.placa_vehiculo = nueva_placa
            repartidor.Usuario_idUsuario = id_usuario
            self.db.commit()
        return repartidor

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un repartidor por su ID
    # (falla si otras tablas dependen de este registro)
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_repartidor):
        repartidor = self.obtener_por_id(id_repartidor)
        if repartidor:
            self.db.delete(repartidor)
            self.db.commit()
            return True
        return False
