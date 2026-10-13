from rest import db
from sqlalchemy import Column, Integer, ForeignKey


class Administrador(db.Base):
    __tablename__ = 'Administrador'
    id_administrador = Column(Integer, primary_key=True, autoincrement=False)
    Usuario_idUsuario = Column(Integer, ForeignKey("Usuario.idUsuario"), nullable=False)

    # Valores por defecto: permiten crear un Administrador sin id (autoincremental)
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_administrador=None, Usuario_idUsuario=None):
        self.id_administrador = id_administrador
        self.Usuario_idUsuario = Usuario_idUsuario

    def __repr__(self):
        return f'Administrador({self.id_administrador}, {self.Usuario_idUsuario})'

    def __str__(self):
        return f'Administrador {self.id_administrador}'

    def toDict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # JSON no representa datetime directamente; ISO 8601 mantiene un formato estable.
        for clave, valor in d.items():
            if hasattr(valor, 'isoformat'):
                d[clave] = valor.isoformat()
        return d
