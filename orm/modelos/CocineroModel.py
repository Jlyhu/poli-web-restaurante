# ============================================================
# CocineroModel.py
# Modelo Cocinero, mapeado a la tabla 'Cocinero' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Cocinero
# Las llaves foráneas las valida MySQL: el registro referenciado debe existir.
# ------------------------------------------------------------
class Cocinero(Base):
    __tablename__ = 'Cocinero'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_cocinero = Column(Integer, primary_key=True, autoincrement=False)
    estacion = Column(String(45), nullable=True)
    Usuario_idUsuario = Column(Integer, nullable=False)
