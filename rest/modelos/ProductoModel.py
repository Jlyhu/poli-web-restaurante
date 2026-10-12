from rest import db
from sqlalchemy import Column, Float, Integer, String


class Producto(db.Base):
    __tablename__ = 'Producto'
    idProducto = Column(Integer, primary_key=True, autoincrement=False)
    nombre = Column(String(100), nullable=True)
    descripcion = Column(String(100), nullable=True)
    precio = Column(Float, nullable=True)
    cantidad_disponible = Column(Integer, nullable=True)

    # Referencia a Categoria.id_categoria: la llave foránea la controla la base de datos
    Categoria_id_categoria = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear un Producto sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, idProducto=None, nombre=None, descripcion=None, precio=None, 
                cantidad_disponible=None, Categoria_id_categoria=None):
        self.idProducto = idProducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad_disponible = cantidad_disponible
        self.Categoria_id_categoria = Categoria_id_categoria

    def __repr__(self):
        return f'Producto({self.idProducto}, {self.nombre}, {self.precio}, {self.cantidad_disponible}, {self.Categoria_id_categoria})'

    def __str__(self):
        return self.nombre

    def toDict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
