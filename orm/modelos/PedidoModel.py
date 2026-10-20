# ============================================================
# PedidoModel.py
# Modelo Pedido, mapeado a la tabla 'Pedido' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, DateTime, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Pedido
# Representa un registro de la tabla 'Pedido'
#
# Atributos:
#   id_pedido (int) -- Clave primaria
#   estado (str)
#   fecha_creacion (datetime)
#   fecha_ultima_actualizacion (datetime)
#   tipo_pedido (str)
#   Mesero_id_mesero (int)
#   Repartidor_id_repartidor (int)
#   Cliente_id_cliente (int)
# ------------------------------------------------------------
class Pedido(Base):
    __tablename__ = 'Pedido'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_pedido = Column(Integer, primary_key=True, autoincrement=False)
    estado = Column(String(45), nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
    fecha_ultima_actualizacion = Column(DateTime, nullable=True)
    tipo_pedido = Column(String(45), nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Mesero_id_mesero = Column(Integer, nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Repartidor_id_repartidor = Column(Integer, nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos (MySQL
    # rechaza el registro si lo referenciado no existe). Se deja como Integer simple
    # para no depender del archivo del modelo de otra persona del equipo.
    Cliente_id_cliente = Column(Integer, nullable=True)
