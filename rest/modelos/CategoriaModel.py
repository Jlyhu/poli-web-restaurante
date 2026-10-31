from rest import db
from sqlalchemy import Column, Integer, String


class Categoria(db.Base):
    __tablename__ = 'Categoria'
    id_categoria = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(100), nullable=True)

    # Valores por defecto: permiten crear un Categoria sin id
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_categoria=None, nombre=None):
        self.id_categoria = id_categoria
        self.nombre = nombre

    def __repr__(self):
        return f'Categoria({self.id_categoria}, {self.nombre})'

    def __str__(self):
        return str(self.id_categoria)

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Las fechas se devuelven como AAAA-MM-DD HH:MM:SS
    def toDict(self):
        return {'id_categoria': self.id_categoria,
                'nombre': self.nombre}
