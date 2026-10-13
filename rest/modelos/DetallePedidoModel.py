from rest import db
from sqlalchemy import Column, Integer, String, ForeignKey


class DetallePedido(db.Base):
    __tablename__ = 'DetallePedido'
    id_detalle_pedido = Column(Integer, primary_key=True, autoincrement=False)
    cantidad = Column(Integer, nullable=True)
    notas = Column(String(120), nullable=True)
    Pedido_id_pedido = Column(Integer, ForeignKey("Pedido.id_pedido"), nullable=False)
    Producto_idProducto = Column(Integer, ForeignKey("Producto.idProducto"), nullable=False)

    # Valores por defecto: permiten crear un DetallePedido sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_detalle_pedido=None, cantidad=None, notas=None, Pedido_id_pedido=None, Producto_idProducto=None):
        self.id_detalle_pedido = id_detalle_pedido
        self.cantidad = cantidad
        self.notas = notas
        self.Pedido_id_pedido = Pedido_id_pedido
        self.Producto_idProducto = Producto_idProducto

    def __repr__(self):
        return f'DetallePedido({self.id_detalle_pedido}, {self.cantidad}, {self.notas}, {self.Pedido_id_pedido}, {self.Producto_idProducto})'

    def __str__(self):
        return f'DetallePedido {self.id_detalle_pedido}'

    def toDict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # JSON no representa datetime directamente; ISO 8601 mantiene un formato estable.
        for clave, valor in d.items():
            if hasattr(valor, 'isoformat'):
                d[clave] = valor.isoformat()
        return d
