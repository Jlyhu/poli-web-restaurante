# ============================================================
# PedidoMesaModel.py
# Modelo PedidoMesa, mapeado a la tabla 'PedidoMesa' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer

from orm.models import Base


# ------------------------------------------------------------
# Clase: PedidoMesa
# Las llaves foráneas las valida MySQL: el registro referenciado debe existir.
# ------------------------------------------------------------
class PedidoMesa(Base):
    __tablename__ = 'PedidoMesa'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_pedido_mesa = Column(Integer, primary_key=True, autoincrement=False)
    Mesa_id_mesa = Column(Integer, nullable=False)
    Pedido_id_pedido = Column(Integer, nullable=False)
