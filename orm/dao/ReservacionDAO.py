# ============================================================
# ReservacionDAO.py
# Capa de acceso a datos (DAO) para la entidad Reservacion, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Reservacion'
# ============================================================

from orm.modelos.ReservacionModel import Reservacion
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: ReservacionDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = ReservacionDAO(session)
#
# Nota: 'fecha' y 'hora' se reciben como objetos datetime de Python
# (la consola convierte el texto escrito por el usuario).
# ------------------------------------------------------------
class ReservacionDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    #--------------------------------------------------------
    # Método: crear
    # Inserta una nueva reservación. El cliente debe existir.
    # Parámetros:
    #   id_reservacion (int/str) -- Identificador único de la reservación
    #   fecha (datetime.date)    -- Fecha de la reservación
    #   hora (datetime.time)     -- Hora de la reservación
    #   numero_personas (int)    -- Número de personas para la reservación
    #   estado (str)             -- Estado de la reservación ('pendiente', 'confirmada', 'cancelada', etc.)
    #   id_cliente (int/str) -- Identificador del cliente que realiza la reservación
    # Retorna:
    #   Reservacion -- El objeto recién creado y persistido
    # Ejemplo:
    #   r = dao.crear(id_reservacion=1, fecha=date(2024, 6, 15), hora=time(19, 30), numero_personas=4, estado='pendiente', id_cliente=123)
    #--------------------------------------------------------
    def crear(self, id_reservacion, fecha, hora, numero_personas, estado, id_cliente):
        nueva_reservacion = Reservacion(
            id_reservacion=id_reservacion,
            fecha=fecha,
            hora=hora,
            numero_personas=numero_personas,
            estado=estado,
            Cliente_id_cliente=id_cliente
        )
        self.db.add(nueva_reservacion)
        self.db.commit()
        self.db.refresh(nueva_reservacion)  # sincroniza el objeto con los datos de la BD
        return nueva_reservacion

    #--------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Parámetros:
    #   id_reservacion (int/str) -- Identificador único de la reservación
    # Retorna:  
    #   Reservacion -- El objeto encontrado, o None si no existe
    # Ejemplo:
    #   r = dao.obtener_por_id(1)
    #--------------------------------------------------------
    def obtener_por_id(self, id_reservacion):
        return self.db.query(Reservacion).filter(Reservacion.id_reservacion == id_reservacion).first()

    #--------------------------------------------------------
    # Método: obtener_por_cliente
    # Recupera todas las reservaciones de un cliente.
    # Parámetros:
    #   id_cliente (int/str) -- Identificador del cliente
    # Retorna:
    #   list[Reservacion] -- La lista de reservaciones encontradas
    # Ejemplo:
    #   r = dao.obtener_por_cliente(123)
    #--------------------------------------------------------
    def obtener_por_cliente(self, id_cliente):
        return self.db.query(Reservacion).filter(Reservacion.Cliente_id_cliente == id_cliente).all()

    #--------------------------------------------------------
    # Método: obtener_todos
    # Recupera todas las reservaciones.
    # Parámetros:
    #   None
    # Retorna:
    #   list[Reservacion] -- La lista de reservaciones encontradas
    # Ejemplo:
    #   r = dao.obtener_todos()
    #--------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Reservacion).all()

    #--------------------------------------------------------
    # Método: actualizar
    # Modifica una reservación existente.
    # Parámetros:
    #   id_reservacion (int/str) -- Identificador único de la reservación
    #   nueva_fecha (datetime.date) -- Nueva fecha de la reservación
    #   nueva_hora (datetime.time) -- Nueva hora de la reservación
    #   nuevo_numero_personas (int) -- Nuevo número de personas para la reservación
    #   nuevo_estado (str) -- Nuevo estado de la reservación ('pendiente', 'confirmada', 'cancelada', etc.)
    # Retorna:
    #   Reservacion -- El objeto actualizado, o None si no existe
    # Ejemplo:
    #   r = dao.actualizar(id_reservacion=1, nueva_fecha=date(2024, 6, 16), nueva_hora=time(20, 0), nuevo_numero_personas=5, nuevo_estado='confirmada')
    #--------------------------------------------------------   
    def actualizar(self, id_reservacion, nueva_fecha, nueva_hora, nuevo_numero_personas, nuevo_estado):
        reservacion = self.obtener_por_id(id_reservacion)
        if reservacion:
            reservacion.fecha           = nueva_fecha
            reservacion.hora            = nueva_hora
            reservacion.numero_personas = nuevo_numero_personas
            reservacion.estado          = nuevo_estado
            self.db.commit()
        return reservacion

    #--------------------------------------------------------
    # Método: eliminar  
    # Elimina una reservación.
    # Falla si la reservación ya tiene mesas asignadas (ReservacionMesa).
    # Parámetros:
    #   id_reservacion (int/str) -- Identificador único de la reservación
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # Ejemplo:
    #   exito = dao.eliminar(1)
    #--------------------------------------------------------
    def eliminar(self, id_reservacion):
        reservacion = self.obtener_por_id(id_reservacion)
        if reservacion:
            self.db.delete(reservacion)
            self.db.commit()
            return True
        return False
