# ============================================================
# RepartidorModel.py
# Modelo Repartidor, mapeado a la tabla 'Repartidor' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Repartidor
# Representa un registro de la tabla 'Repartidor'
#
# Atributos:
#   id_repartidor (int) -- Clave primaria
#   placa_vehiculo (str)
#   Usuario_idUsuario (int)
# ------------------------------------------------------------
class Repartidor(Base):
    __tablename__ = 'Repartidor'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_repartidor = Column(Integer, primary_key=True, autoincrement=False)
    placa_vehiculo = Column(String(45), nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Usuario_idUsuario = Column(Integer, nullable=False)
