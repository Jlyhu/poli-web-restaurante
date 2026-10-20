from rest import db
from sqlalchemy import Column, DateTime, Float, Integer


class Caja(db.Base):
    __tablename__ = 'Caja'
    id_caja = Column(Integer, primary_key=True, autoincrement=False)
    fecha_apertura = Column(DateTime, nullable=True)
    fecha_cierre = Column(DateTime, nullable=True)
    monto_inicial = Column(Float, nullable=True)
    monto_final = Column(Float, nullable=True)
    # Referencia a otra tabla: la llave foránea la controla la base de datos
    Cajero_id_cajero = Column(Integer, nullable=False)

    # Valores por defecto: permiten crear un Caja sin id
    # (en nuestra tabla el id no se genera solo: el servicio asigna el siguiente)
    def __init__(self, id_caja=None, fecha_apertura=None, fecha_cierre=None, monto_inicial=None, monto_final=None, Cajero_id_cajero=None):
        self.id_caja = id_caja
        self.fecha_apertura = fecha_apertura
        self.fecha_cierre = fecha_cierre
        self.monto_inicial = monto_inicial
        self.monto_final = monto_final
        self.Cajero_id_cajero = Cajero_id_cajero

    def __repr__(self):
        return f'Caja({self.id_caja}, {self.fecha_apertura}, {self.fecha_cierre}, {self.monto_inicial}, {self.monto_final}, {self.Cajero_id_cajero})'

    def __str__(self):
        return str(self.id_caja)

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Las fechas se devuelven como AAAA-MM-DD HH:MM:SS
    def toDict(self):
        return {'id_caja': self.id_caja,
                'fecha_apertura': self.fecha_apertura.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_apertura else None,
                'fecha_cierre': self.fecha_cierre.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_cierre else None,
                'monto_inicial': self.monto_inicial,
                'monto_final': self.monto_final,
                'Cajero_id_cajero': self.Cajero_id_cajero}
