# ============================================================
# ReservacionMesaModel.py
# Modelo ReservacionMesa, mapeado a la tabla 'ReservacionMesa' que YA
# existe en la base de datos (no se crea ni se modifica ninguna tabla).
# Es la tabla que asigna mesas a una reservación.
# ============================================================

from sqlalchemy import Column, Integer

from orm.models import Base


# ------------------------------------------------------------
# Clase: ReservacionMesa
# Atributos:
#   id_reservacion_mesa        (int)  -- Clave primaria
#   Mesa_id_mesa               (int)  -- id de la mesa asignada
#   Reservacion_id_reservacion (int)  -- id de la reservación
# ------------------------------------------------------------
class ReservacionMesa(Base):
    __tablename__ = 'ReservacionMesa'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_reservacion_mesa = Column(Integer, primary_key=True, autoincrement=False)

    # Referencias a Mesa y Reservacion. Las llaves foráneas las controla la base de datos:
    # si la mesa o la reservación no existen, MySQL rechaza el registro.
    Mesa_id_mesa               = Column(Integer, nullable=False)
    Reservacion_id_reservacion = Column(Integer, nullable=False)
