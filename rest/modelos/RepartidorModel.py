from rest import db
from sqlalchemy import Column, Integer, String


class Repartidor(db.Base):
    __tablename__ = 'Repartidor'
    id_repartidor = Column(Integer, primary_key=True, autoincrement=False)
    placa_vehiculo = Column(String(45), nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Usuario_idUsuario = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear un Repartidor sin id
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_repartidor=None, placa_vehiculo=None, Usuario_idUsuario=None):
        self.id_repartidor = id_repartidor
        self.placa_vehiculo = placa_vehiculo
        self.Usuario_idUsuario = Usuario_idUsuario

    def __repr__(self):
        return f'Repartidor({self.id_repartidor}, {self.placa_vehiculo}, {self.Usuario_idUsuario})'

    def __str__(self):
        return str(self.id_repartidor)

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Las fechas se devuelven como AAAA-MM-DD HH:MM:SS
    def toDict(self):
        return {'id_repartidor': self.id_repartidor,
                'placa_vehiculo': self.placa_vehiculo,
                'Usuario_idUsuario': self.Usuario_idUsuario}
