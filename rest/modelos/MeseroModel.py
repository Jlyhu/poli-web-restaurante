from rest import db
from sqlalchemy import Column, Integer, String


class Mesero(db.Base):
    __tablename__ = 'Mesero'
    id_mesero = Column(Integer, primary_key=True, autoincrement=False)
    zona_asignada = Column(String(45), nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Usuario_idUsuario = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear un Mesero sin id
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_mesero=None, zona_asignada=None, Usuario_idUsuario=None):
        self.id_mesero = id_mesero
        self.zona_asignada = zona_asignada
        self.Usuario_idUsuario = Usuario_idUsuario

    def __repr__(self):
        return f'Mesero({self.id_mesero}, {self.zona_asignada}, {self.Usuario_idUsuario})'

    def __str__(self):
        return str(self.id_mesero)

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Las fechas se devuelven como AAAA-MM-DD HH:MM:SS
    def toDict(self):
        return {'id_mesero': self.id_mesero,
                'zona_asignada': self.zona_asignada,
                'Usuario_idUsuario': self.Usuario_idUsuario}
