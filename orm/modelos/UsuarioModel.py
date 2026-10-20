# ============================================================
# UsuarioModel.py
# Modelo Usuario, mapeado a la tabla 'Usuario' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Usuario
# Representa un registro de la tabla 'Usuario'
#
# Atributos:
#   idUsuario    (int)  -- Clave primaria
#   nombre       (str)  -- Nombre de usuario
#   credenciales (str)  -- Credenciales de acceso
#   estado       (str)  -- 'activo' o 'inactivo'
#
# Ejemplo:
#   u = Usuario(idUsuario=1, nombre="Ana", credenciales="1234")
# ------------------------------------------------------------
class Usuario(Base):
    __tablename__ = 'Usuario'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    idUsuario    = Column(Integer, primary_key=True, autoincrement=False)
    nombre       = Column(String(100), nullable=True)
    credenciales = Column(String(255), nullable=True)
    estado       = Column(String(20), nullable=False, default='activo')
