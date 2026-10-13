from rest import db
from sqlalchemy import Column, Integer, ForeignKey


class PedidoMesa(db.Base):
    __tablename__ = 'PedidoMesa'
    id_pedido_mesa = Column(Integer, primary_key=True, autoincrement=False)
    Mesa_id_mesa = Column(Integer, ForeignKey("Mesa.id_mesa"), nullable=False)
    Pedido_id_pedido = Column(Integer, ForeignKey("Pedido.id_pedido"), nullable=False)

    # Valores por defecto: permiten crear un PedidoMesa sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_pedido_mesa=None, Mesa_id_mesa=None, Pedido_id_pedido=None):
        self.id_pedido_mesa = id_pedido_mesa
        self.Mesa_id_mesa = Mesa_id_mesa
        self.Pedido_id_pedido = Pedido_id_pedido

    def __repr__(self):
        return f'PedidoMesa({self.id_pedido_mesa}, {self.Mesa_id_mesa}, {self.Pedido_id_pedido})'

    def __str__(self):
        return f'PedidoMesa {self.id_pedido_mesa}'

    def toDict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # JSON no representa datetime directamente; ISO 8601 mantiene un formato estable.
        for clave, valor in d.items():
            if hasattr(valor, 'isoformat'):
                d[clave] = valor.isoformat()
        return d
