from rest import db
from sqlalchemy import Column, Integer, String, Float, DateTime


class Pago(db.Base):
    __tablename__ = 'Pago'
    id_pago = Column(Integer, primary_key=True, autoincrement=False)
    monto = Column(Float, nullable=True)
    metodo_pago = Column(String(45), nullable=True)
    fecha_pago = Column(DateTime, nullable=True)
    Pedido_id_pedido = Column(Integer, nullable=False)
    Caja_id_caja = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear un Pago sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_pago=None, monto=None, metodo_pago=None, fecha_pago=None, Pedido_id_pedido=None, Caja_id_caja=None):
        self.id_pago = id_pago
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago
        self.Pedido_id_pedido = Pedido_id_pedido
        self.Caja_id_caja = Caja_id_caja

    def __repr__(self):
        return f'Pago({self.id_pago}, {self.monto}, {self.metodo_pago}, {self.fecha_pago}, {self.Pedido_id_pedido}, {self.Caja_id_caja})'

    def __str__(self):
        return f'Pago {self.id_pago}'

    def toDict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if d['fecha_pago'] is not None:
            d['fecha_pago'] = d['fecha_pago'].isoformat()
        return d
