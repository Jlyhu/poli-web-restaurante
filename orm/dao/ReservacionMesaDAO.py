# ============================================================
# ReservacionMesaDAO.py
# Capa de acceso a datos (DAO) para la entidad ReservacionMesa, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'ReservacionMesa'
# ============================================================

from orm.modelos.ReservacionMesaModel import ReservacionMesa
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: ReservacionMesaDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = ReservacionMesaDAO(session)
# ------------------------------------------------------------
class ReservacionMesaDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # ------------------------------------------------------------
    # Método: crear
    # Asigna una mesa a una reservación. Ambas deben existir.
    # Parámetros:
    #   id_reservacion_mesa (int/str) -- Identificador único de la relación
    #   id_mesa (int/str) -- Identificador de la mesa
    #   id_reservacion (int/str) -- Identificador de la reservación
    # Retorna: 
    #   ReservacionMesa (el objeto creado)
    # Ejemplo:
    #   rm = dao.crear(id_reservacion_mesa=1, id_mesa=10, id_reservacion=5)
    # ------------------------------------------------------------
    def crear(self, id_reservacion_mesa, id_mesa, id_reservacion):
        nuevo = ReservacionMesa(
            id_reservacion_mesa=id_reservacion_mesa,
            Mesa_id_mesa=id_mesa,
            Reservacion_id_reservacion=id_reservacion
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    #--------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria. 
    # Parámetros:
    #   id_reservacion_mesa (int/str) -- Identificador único de la relación
    # Retorna: 
    #   ReservacionMesa | None
    # Ejemplo:
    #   rm = dao.obtener_por_id(1)
    #--------------------------------------------------------
    def obtener_por_id(self, id_reservacion_mesa):
        return self.db.query(ReservacionMesa).filter(
            ReservacionMesa.id_reservacion_mesa == id_reservacion_mesa).first()
    
    #--------------------------------------------------------
    # Método: obtener_por_reservacion
    # Recupera las mesas asignadas a una reservación.
    # Parámetros:
    #   id_reservacion (int/str) -- Identificador de la reservación
    # Retorna:
    #   list[ReservacionMesa] -- La lista de relaciones encontradas
    # Ejemplo:
    #   rms = dao.obtener_por_reservacion(5)
    #--------------------------------------------------------
    def obtener_por_reservacion(self, id_reservacion):
        return self.db.query(ReservacionMesa).filter(
            ReservacionMesa.Reservacion_id_reservacion == id_reservacion).all()
    
    #--------------------------------------------------------
    # Método: obtener_todos
    # Recupera todas las relaciones reservación-mesa.
    # Parámetros: ninguno
    # Retorna:
    #   list[ReservacionMesa] -- La lista de relaciones encontradas
    # Ejemplo:
    #   rms = dao.obtener_todos()
    #--------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(ReservacionMesa).all()

    #--------------------------------------------------------
    # Método: actualizar
    # Cambia la mesa o la reservación de un registro. 
    # Parámetros:
    #   id_reservacion_mesa (int/str) -- Identificador único de la relación
    #   nuevo_id_mesa (int/str) -- Nuevo identificador de la mesa
    #   nuevo_id_reservacion (int/str) -- Nuevo identificador de la reservación
    # Retorna: 
    #   ReservacionMesa | None
    # Ejemplo:
    #   rm = dao.actualizar(id_reservacion_mesa=1, nuevo_id_mesa=12, nuevo_id_reservacion=6)
    #--------------------------------------------------------
    def actualizar(self, id_reservacion_mesa, nuevo_id_mesa, nuevo_id_reservacion):
        registro = self.obtener_por_id(id_reservacion_mesa)
        if registro:
            registro.Mesa_id_mesa               = nuevo_id_mesa
            registro.Reservacion_id_reservacion = nuevo_id_reservacion
            self.db.commit()
        return registro

    #--------------------------------------------------------
    # Método: eliminar
    # Elimina un registro. 
    # Parámetros:
    #   id_reservacion_mesa (int/str) -- Identificador único de la relación
    # Retorna: 
    #   bool (True si se eliminó, False si no existía)
    # Ejemplo:
    #   exito = dao.eliminar(1)
    #--------------------------------------------------------
    def eliminar(self, id_reservacion_mesa):
        registro = self.obtener_por_id(id_reservacion_mesa)
        if registro:
            self.db.delete(registro)
            self.db.commit()
            return True
        return False
