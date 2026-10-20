from rest import db
from sqlalchemy import Column, Integer


class PedidoMesa(db.Base):
    __tablename__ = 'PedidoMesa'
    id_pedido_mesa = Column(Integer, primary_key=True, autoincrement=False)
    Mesa_id_mesa = Column(Integer, nullable=False)
    Pedido_id_pedido = Column(Integer, nullable=False)

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
        return d
