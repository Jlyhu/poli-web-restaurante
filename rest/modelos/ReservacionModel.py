from rest import db
from sqlalchemy import Column, DateTime, Integer, String


class Reservacion(db.Base):
    __tablename__ = 'Reservacion'
    id_reservacion = Column(Integer, primary_key=True, autoincrement=False)
    fecha = Column(DateTime, nullable=True)
    hora = Column(DateTime, nullable=True)      # la columna es DATETIME: guarda fecha y hora juntas
    numero_personas = Column(Integer, nullable=True)
    estado = Column(String(45), nullable=True)

    # Referencia a Cliente.id_cliente: la llave foránea la controla la base de datos
    Cliente_id_cliente = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear una Reservacion sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_reservacion=None, fecha=None, hora=None, numero_personas=None,
                estado=None, Cliente_id_cliente=None):
        self.id_reservacion = id_reservacion
        self.fecha = fecha
        self.hora = hora
        self.numero_personas = numero_personas
        self.estado = estado
        self.Cliente_id_cliente = Cliente_id_cliente

    def __repr__(self):
        return f'Reservacion({self.id_reservacion}, {self.fecha}, {self.hora}, {self.numero_personas}, {self.estado}, {self.Cliente_id_cliente})'

    def __str__(self):
        return str(self.id_reservacion)

    # La fecha se devuelve como AAAA-MM-DD y la hora como HH:MM:SS
    def toDict(self):
        return {'id_reservacion': self.id_reservacion,
                'fecha': self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
                'hora': self.hora.strftime('%H:%M:%S') if self.hora else None,
                'numero_personas': self.numero_personas,
                'estado': self.estado,
                'Cliente_id_cliente': self.Cliente_id_cliente}
