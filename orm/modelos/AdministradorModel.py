# ============================================================
# AdministradorModel.py
# Modelo Administrador, mapeado a la tabla 'Administrador' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, ForeignKey

from orm.models import Base


# ------------------------------------------------------------
# Clase: Administrador
# Las llaves foráneas las valida MySQL: el registro referenciado debe existir.
# ------------------------------------------------------------
class Administrador(Base):
    __tablename__ = 'Administrador'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_administrador = Column(Integer, primary_key=True, autoincrement=False)
    Usuario_idUsuario = Column(Integer, ForeignKey("Usuario.idUsuario"), nullable=False)
