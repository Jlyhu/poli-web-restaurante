from rest import db
from sqlalchemy import Column, Integer, String


class Cliente(db.Base):
    __tablename__ = 'Cliente'
    id_cliente = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(45), nullable=True)
    direccion = Column(String(45), nullable=True)
    telefono = Column(String(45), nullable=True)

    # Valores por defecto: permiten crear un Cliente sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_cliente=None, nombre=None, direccion=None, telefono=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def __repr__(self):
        return f'Cliente({self.id_cliente}, {self.nombre}, {self.direccion}, {self.telefono})'

    def __str__(self):
        return self.nombre

    def toDict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
