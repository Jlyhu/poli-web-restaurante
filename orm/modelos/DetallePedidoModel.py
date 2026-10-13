# ============================================================
# DetallePedidoModel.py
# Modelo DetallePedido, mapeado a la tabla 'DetallePedido' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String, ForeignKey

from orm.models import Base


# ------------------------------------------------------------
# Clase: DetallePedido
# Las llaves foráneas las valida MySQL: el registro referenciado debe existir.
# ------------------------------------------------------------
class DetallePedido(Base):
    __tablename__ = 'DetallePedido'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_detalle_pedido = Column(Integer, primary_key=True, autoincrement=False)
    cantidad = Column(Integer, nullable=True)
    notas = Column(String(120), nullable=True)
    Pedido_id_pedido = Column(Integer, ForeignKey("Pedido.id_pedido"), nullable=False)
    Producto_idProducto = Column(Integer, ForeignKey("Producto.idProducto"), nullable=False)
