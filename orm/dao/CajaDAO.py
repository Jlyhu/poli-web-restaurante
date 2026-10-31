# ============================================================
# CajaDAO.py
# Capa de acceso a datos (DAO) para la entidad Caja, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Caja'
# ============================================================

from datetime import datetime

from orm.modelos.CajaModel import Caja
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: CajaDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = CajaDAO(session)
# ------------------------------------------------------------
class CajaDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta una caja nuevo. La fecha de apertura se pone sola (ahora).
    # Retorna:
    #   Caja -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_caja, monto_inicial, id_cajero):
        nuevo = Caja(
            id_caja=id_caja,
            fecha_apertura=datetime.now(),
            monto_inicial=monto_inicial,
            Cajero_id_cajero=id_cajero,
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria
    # Retorna:
    #   Caja | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_caja):
        return self.db.query(Caja).filter(Caja.id_caja == id_caja).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Caja
    # Retorna:
    #   list[Caja] -- Lista de objetos (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Caja).order_by(Caja.id_caja).all()

    # --------------------------------------------------------
    # Método: cerrar
    # Cierra la caja: guarda el monto final y la fecha de cierre (ahora)
    # Retorna:
    #   Caja | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def cerrar(self, id_caja, monto_final):
        caja = self.obtener_por_id(id_caja)
        if caja:
            caja.fecha_cierre = datetime.now()
            caja.monto_final  = monto_final
            self.db.commit()
        return caja

    # --------------------------------------------------------
    # Método: obtener_por_cajero
    # Recupera todas las cajas de un cajero
    # --------------------------------------------------------
    def obtener_por_cajero(self, id_cajero):
        return self.db.query(Caja).filter(Caja.Cajero_id_cajero == id_cajero).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de una caja existente
    # Retorna:
    #   Caja | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, id_caja, monto_inicial, monto_final, id_cajero):
        caja = self.obtener_por_id(id_caja)
        if caja:
            caja.monto_inicial = monto_inicial
            caja.monto_final = monto_final
            caja.Cajero_id_cajero = id_cajero
            self.db.commit()
        return caja

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina una caja por su ID
    # (falla si otras tablas dependen de este registro)
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_caja):
        caja = self.obtener_por_id(id_caja)
        if caja:
            self.db.delete(caja)
            self.db.commit()
            return True
        return False
