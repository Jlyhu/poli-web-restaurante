from rest import db
from sqlalchemy import Column, Integer


class Cajero(db.Base):
    __tablename__ = 'Cajero'
    id_cajero = Column(Integer, primary_key=True, autoincrement=False)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Usuario_idUsuario = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear un Cajero sin id
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_cajero=None, Usuario_idUsuario=None):
        self.id_cajero = id_cajero
        self.Usuario_idUsuario = Usuario_idUsuario

    def __repr__(self):
        return f'Cajero({self.id_cajero}, {self.Usuario_idUsuario})'

    def __str__(self):
        return str(self.id_cajero)

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Las fechas se devuelven como AAAA-MM-DD HH:MM:SS
    def toDict(self):
        return {'id_cajero': self.id_cajero,
                'Usuario_idUsuario': self.Usuario_idUsuario}
