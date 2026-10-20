# ============================================================
# CajeroModel.py
# Modelo Cajero, mapeado a la tabla 'Cajero' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer

from orm.models import Base


# ------------------------------------------------------------
# Clase: Cajero
# Representa un registro de la tabla 'Cajero'
#
# Atributos:
#   id_cajero (int) -- Clave primaria
#   Usuario_idUsuario (int)
# ------------------------------------------------------------
class Cajero(Base):
    __tablename__ = 'Cajero'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_cajero = Column(Integer, primary_key=True, autoincrement=False)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Usuario_idUsuario = Column(Integer, nullable=False)
