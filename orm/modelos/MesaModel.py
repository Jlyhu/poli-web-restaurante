# ============================================================
# MesaModel.py
# Modelo Mesa, mapeado a la tabla 'Mesa' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Mesa
# Atributos:
#   id_mesa (int)  -- Clave primaria
#   numero  (int)  -- Número de la mesa en el restaurante
#   estado  (str)  -- Estado de la mesa (por ejemplo 'Disponible')
# ------------------------------------------------------------
class Mesa(Base):
    __tablename__ = 'Mesa'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_mesa = Column(Integer, primary_key=True, autoincrement=False)
    numero  = Column(Integer, nullable=True)
    estado  = Column(String(45), nullable=True)
