# ============================================================
# PagoModel.py
# Modelo Pago, mapeado a la tabla 'Pago' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Integer, String, Float, DateTime

from orm.models import Base


# ------------------------------------------------------------
# Clase: Pago
# Las llaves foráneas las valida MySQL: el registro referenciado debe existir.
# ------------------------------------------------------------
class Pago(Base):
    __tablename__ = 'Pago'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    id_pago = Column(Integer, primary_key=True, autoincrement=False)
    monto = Column(Float, nullable=True)
    metodo_pago = Column(String(45), nullable=True)
    fecha_pago = Column(DateTime, nullable=True)
    Pedido_id_pedido = Column(Integer, nullable=False)
    Caja_id_caja = Column(Integer, nullable=False)
