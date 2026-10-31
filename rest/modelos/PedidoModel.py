from rest import db
from sqlalchemy import Column, DateTime, Integer, String


class Pedido(db.Base):
    __tablename__ = 'Pedido'
    id_pedido = Column(Integer, primary_key=True, autoincrement=False)
    estado = Column(String(45), nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
    fecha_ultima_actualizacion = Column(DateTime, nullable=True)
    tipo_pedido = Column(String(45), nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Mesero_id_mesero = Column(Integer, nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Repartidor_id_repartidor = Column(Integer, nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Cliente_id_cliente = Column(Integer, nullable=True)

    # Valores por defecto: permiten crear un Pedido sin id
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_pedido=None, estado=None, fecha_creacion=None, fecha_ultima_actualizacion=None, tipo_pedido=None, Mesero_id_mesero=None, Repartidor_id_repartidor=None, Cliente_id_cliente=None):
        self.id_pedido = id_pedido
        self.estado = estado
        self.fecha_creacion = fecha_creacion
        self.fecha_ultima_actualizacion = fecha_ultima_actualizacion
        self.tipo_pedido = tipo_pedido
        self.Mesero_id_mesero = Mesero_id_mesero
        self.Repartidor_id_repartidor = Repartidor_id_repartidor
        self.Cliente_id_cliente = Cliente_id_cliente

    def __repr__(self):
        return f'Pedido({self.id_pedido}, {self.estado}, {self.fecha_creacion}, {self.fecha_ultima_actualizacion}, {self.tipo_pedido}, {self.Mesero_id_mesero}, {self.Repartidor_id_repartidor}, {self.Cliente_id_cliente})'

    def __str__(self):
        return str(self.id_pedido)

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Las fechas se devuelven como AAAA-MM-DD HH:MM:SS
    def toDict(self):
        return {'id_pedido': self.id_pedido,
                'estado': self.estado,
                'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None,
                'fecha_ultima_actualizacion': self.fecha_ultima_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_ultima_actualizacion else None,
                'tipo_pedido': self.tipo_pedido,
                'Mesero_id_mesero': self.Mesero_id_mesero,
                'Repartidor_id_repartidor': self.Repartidor_id_repartidor,
                'Cliente_id_cliente': self.Cliente_id_cliente}
