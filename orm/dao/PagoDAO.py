# ============================================================
# PagoDAO.py
# Capa de acceso a datos (DAO) para la entidad Pago, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Pago'
# ============================================================

from orm.modelos.PagoModel import Pago
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: PagoDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = PagoDAO(session)
# ------------------------------------------------------------
class PagoDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo registro.
    # Falla si el id ya existe o si una llave foránea no existe.
    # Retorna: Pago -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_pago, monto, metodo_pago, fecha_pago, Pedido_id_pedido, Caja_id_caja):
        nuevo = Pago(
            id_pago=id_pago,
            monto=monto,
            metodo_pago=metodo_pago,
            fecha_pago=fecha_pago,
            Pedido_id_pedido=Pedido_id_pedido,
            Caja_id_caja=Caja_id_caja
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Retorna: Pago -- El objeto encontrado, o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_pago):
        return self.db.query(Pago).filter(Pago.id_pago == id_pago).first()

    # --------------------------------------------------------
    # Método: obtener_por_pedido
    # Busca por id de pedido.
    # Retorna: list[Pago] -- Lista de registros encontrados (puede estar vacía)
    # --------------------------------------------------------
    def obtener_por_pedido(self, valor):
        return self.db.query(Pago).filter(Pago.Pedido_id_pedido == valor).all()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros.
    # Retorna: list[Pago]
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Pago).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica un registro existente (el id no se modifica).
    # Retorna: Pago -- El objeto actualizado, o None si no existe
    # --------------------------------------------------------
    def actualizar(self, id_pago, monto, metodo_pago, Pedido_id_pedido, Caja_id_caja):
        registro = self.obtener_por_id(id_pago)
        if registro:
            registro.monto = monto
            registro.metodo_pago = metodo_pago
            registro.Pedido_id_pedido = Pedido_id_pedido
            registro.Caja_id_caja = Caja_id_caja
            self.db.commit()
        return registro

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un registro.
    # Falla si otros registros dependen de él (llave foránea).
    # Retorna: bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_pago):
        registro = self.obtener_por_id(id_pago)
        if registro:
            self.db.delete(registro)
            self.db.commit()
            return True
        return False
