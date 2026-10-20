from rest import db
from sqlalchemy import Column, Integer, String


class Mesa(db.Base):
    __tablename__ = 'Mesa'
    id_mesa = Column(Integer, primary_key=True, autoincrement=False)
    numero = Column(Integer, nullable=True)
    estado = Column(String(45), nullable=True)

    # Valores por defecto: permiten crear una Mesa sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_mesa=None, numero=None, estado=None):
        self.id_mesa = id_mesa
        self.numero = numero
        self.estado = estado

    def __repr__(self):
        return f'Mesa({self.id_mesa}, {self.numero}, {self.estado})'

    def __str__(self):
        return str(self.numero)

    def toDict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
