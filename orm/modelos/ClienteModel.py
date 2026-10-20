# ============================================================
# ClienteModel.py
# Modelo Cliente, mapeado a la tabla 'Cliente' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Cliente
# Atributos:
#   id_cliente (int)  -- Clave primaria
#   nombre     (str)  -- Nombre del cliente
#   direccion  (str)  -- Dirección
#   telefono   (str)  -- Teléfono
# ------------------------------------------------------------
class Cliente(Base):
    __tablename__ = 'Cliente'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_cliente = Column(Integer, primary_key=True, autoincrement=False)
    nombre     = Column(String(45), nullable=True)
    direccion  = Column(String(45), nullable=True)
    telefono   = Column(String(45), nullable=True)
