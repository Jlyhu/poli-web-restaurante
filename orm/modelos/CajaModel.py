# ============================================================
# CajaModel.py
# Modelo Caja, mapeado a la tabla 'Caja' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, DateTime, Float, Integer

from orm.models import Base


# ------------------------------------------------------------
# Clase: Caja
# Representa un registro de la tabla 'Caja'
#
# Atributos:
#   id_caja (int) -- Clave primaria
#   fecha_apertura (datetime)
#   fecha_cierre (datetime)
#   monto_inicial (float)
#   monto_final (float)
#   Cajero_id_cajero (int)
# ------------------------------------------------------------
class Caja(Base):
    __tablename__ = 'Caja'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_caja = Column(Integer, primary_key=True, autoincrement=False)
    fecha_apertura = Column(DateTime, nullable=True)
    fecha_cierre = Column(DateTime, nullable=True)
    monto_inicial = Column(Float, nullable=True)
    monto_final = Column(Float, nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Cajero_id_cajero = Column(Integer, nullable=False)
