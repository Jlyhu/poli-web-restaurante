# ============================================================
# PedidoMesaDAO.py
# Capa de acceso a datos (DAO) para la entidad PedidoMesa, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'PedidoMesa'
# ============================================================

from orm.modelos.PedidoMesaModel import PedidoMesa
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: PedidoMesaDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = PedidoMesaDAO(session)
# ------------------------------------------------------------
class PedidoMesaDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo registro.
    # Falla si el id ya existe o si una llave foránea no existe.
    # Retorna: PedidoMesa -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_pedido_mesa, Mesa_id_mesa, Pedido_id_pedido):
        nuevo = PedidoMesa(
            id_pedido_mesa=id_pedido_mesa,
            Mesa_id_mesa=Mesa_id_mesa,
            Pedido_id_pedido=Pedido_id_pedido
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Retorna: PedidoMesa -- El objeto encontrado, o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_pedido_mesa):
        return self.db.query(PedidoMesa).filter(PedidoMesa.id_pedido_mesa == id_pedido_mesa).first()

    # --------------------------------------------------------
    # Método: obtener_por_mesa
    # Busca por id de mesa.
    # Retorna: list[PedidoMesa] -- Lista de registros encontrados (puede estar vacía)
    # --------------------------------------------------------
    def obtener_por_mesa(self, valor):
        return self.db.query(PedidoMesa).filter(PedidoMesa.Mesa_id_mesa == valor).all()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros.
    # Retorna: list[PedidoMesa]
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(PedidoMesa).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica un registro existente (el id no se modifica).
    # Retorna: PedidoMesa -- El objeto actualizado, o None si no existe
    # --------------------------------------------------------
    def actualizar(self, id_pedido_mesa, Mesa_id_mesa, Pedido_id_pedido):
        registro = self.obtener_por_id(id_pedido_mesa)
        if registro:
            registro.Mesa_id_mesa = Mesa_id_mesa
            registro.Pedido_id_pedido = Pedido_id_pedido
            self.db.commit()
        return registro

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un registro.
    # Falla si otros registros dependen de él (llave foránea).
    # Retorna: bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_pedido_mesa):
        registro = self.obtener_por_id(id_pedido_mesa)
        if registro:
            self.db.delete(registro)
            self.db.commit()
            return True
        return False
