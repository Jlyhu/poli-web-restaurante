from rest import db
from sqlalchemy import Column, Integer


class ReservacionMesa(db.Base):
    __tablename__ = 'ReservacionMesa'
    id_reservacion_mesa = Column(Integer, primary_key=True, autoincrement=False)

    # Referencias a Mesa y Reservacion: las llaves foráneas las controla la base de datos
    Mesa_id_mesa = Column(Integer, nullable=False)
    Reservacion_id_reservacion = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear una ReservacionMesa sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_reservacion_mesa=None, Mesa_id_mesa=None, Reservacion_id_reservacion=None):
        self.id_reservacion_mesa = id_reservacion_mesa
        self.Mesa_id_mesa = Mesa_id_mesa
        self.Reservacion_id_reservacion = Reservacion_id_reservacion

    def __repr__(self):
        return f'ReservacionMesa({self.id_reservacion_mesa}, {self.Mesa_id_mesa}, {self.Reservacion_id_reservacion})'

    def __str__(self):
        return str(self.id_reservacion_mesa)

    def toDict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
