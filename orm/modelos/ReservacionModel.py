# ============================================================
# ReservacionModel.py
# Modelo Reservacion, mapeado a la tabla 'Reservacion' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, DateTime, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Reservacion
# Atributos:
#   id_reservacion     (int)       -- Clave primaria
#   fecha              (datetime)  -- Día de la reservación
#   hora               (datetime)  -- Hora de la reservación (la columna es DATETIME)
#   numero_personas    (int)       -- Cantidad de personas
#   estado             (str)       -- Estado (por ejemplo 'Pendiente')
#   Cliente_id_cliente (int)       -- id del cliente que reserva
# ------------------------------------------------------------
class Reservacion(Base):
    __tablename__ = 'Reservacion'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_reservacion  = Column(Integer, primary_key=True, autoincrement=False)
    fecha           = Column(DateTime, nullable=True)
    hora            = Column(DateTime, nullable=True)
    numero_personas = Column(Integer, nullable=True)
    estado          = Column(String(45), nullable=True)

    # Referencia a Cliente.id_cliente. La llave foránea la controla la base de datos:
    # si el cliente no existe, MySQL rechaza la reservación. Se deja como Integer simple
    # para no depender del archivo del modelo de otra tabla.
    Cliente_id_cliente = Column(Integer, nullable=False)
