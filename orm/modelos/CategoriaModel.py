# ============================================================
# CategoriaModel.py
# Modelo Categoria, mapeado a la tabla 'Categoria' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Categoria
# Representa un registro de la tabla 'Categoria'
#
# Atributos:
#   id_categoria (int) -- Clave primaria
#   nombre (str)
# ------------------------------------------------------------
class Categoria(Base):
    __tablename__ = 'Categoria'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_categoria = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(100), nullable=True)
