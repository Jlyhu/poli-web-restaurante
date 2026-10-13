from rest import db
from sqlalchemy import Column, Integer, String, ForeignKey


class Cocinero(db.Base):
    __tablename__ = 'Cocinero'
    id_cocinero = Column(Integer, primary_key=True, autoincrement=False)
    estacion = Column(String(45), nullable=True)
    Usuario_idUsuario = Column(Integer, ForeignKey("Usuario.idUsuario"), nullable=False)

    # Valores por defecto: permiten crear un Cocinero sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_cocinero=None, estacion=None, Usuario_idUsuario=None):
        self.id_cocinero = id_cocinero
        self.estacion = estacion
        self.Usuario_idUsuario = Usuario_idUsuario

    def __repr__(self):
        return f'Cocinero({self.id_cocinero}, {self.estacion}, {self.Usuario_idUsuario})'

    def __str__(self):
        return f'Cocinero {self.id_cocinero}'

    def toDict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # JSON no representa datetime directamente; ISO 8601 mantiene un formato estable.
        for clave, valor in d.items():
            if hasattr(valor, 'isoformat'):
                d[clave] = valor.isoformat()
        return d
