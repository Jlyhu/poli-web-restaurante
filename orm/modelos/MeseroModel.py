# ============================================================
# MeseroModel.py
# Modelo Mesero, mapeado a la tabla 'Mesero' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Mesero
# Representa un registro de la tabla 'Mesero'
#
# Atributos:
#   id_mesero (int) -- Clave primaria
#   zona_asignada (str)
#   Usuario_idUsuario (int)
# ------------------------------------------------------------
class Mesero(Base):
    __tablename__ = 'Mesero'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_mesero = Column(Integer, primary_key=True, autoincrement=False)
    zona_asignada = Column(String(45), nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Usuario_idUsuario = Column(Integer, nullable=False)
