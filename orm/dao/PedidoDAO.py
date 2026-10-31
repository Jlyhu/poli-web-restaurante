# ============================================================
# PedidoDAO.py
# Capa de acceso a datos (DAO) para la entidad Pedido, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Pedido'
# ============================================================

from datetime import datetime

from orm.modelos.PedidoModel import Pedido
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: PedidoDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = PedidoDAO(session)
# ------------------------------------------------------------
class PedidoDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un pedido nuevo. Las fechas se ponen solas (ahora) y el estado inicial es 'PENDIENTE'.
    # Retorna:
    #   Pedido -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_pedido, tipo_pedido, id_mesero=None, id_repartidor=None, id_cliente=None, estado='PENDIENTE'):
        nuevo = Pedido(
            id_pedido=id_pedido,
            estado=estado,
            fecha_creacion=datetime.now(),
            fecha_ultima_actualizacion=datetime.now(),
            tipo_pedido=tipo_pedido,
            Mesero_id_mesero=id_mesero,
            Repartidor_id_repartidor=id_repartidor,
            Cliente_id_cliente=id_cliente,
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria
    # Retorna:
    #   Pedido | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_pedido):
        return self.db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Pedido
    # Retorna:
    #   list[Pedido] -- Lista de objetos (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Pedido).order_by(Pedido.id_pedido).all()

    # --------------------------------------------------------
    # Método: obtener_por_estado
    # Recupera los pedidos que están en un estado (por ejemplo la cola de cocina: 'PENDIENTE')
    # --------------------------------------------------------
    def obtener_por_estado(self, estado):
        return self.db.query(Pedido).filter(Pedido.estado == estado).order_by(Pedido.id_pedido).all()

    # --------------------------------------------------------
    # Método: actualizar_estado
    # Cambia solo el estado y la fecha de última actualización.
    # Las reglas del flujo (qué cambio de estado se permite) van en el Manager.
    # Retorna:
    #   Pedido | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar_estado(self, id_pedido, nuevo_estado):
        pedido = self.obtener_por_id(id_pedido)
        if pedido:
            pedido.estado = nuevo_estado
            pedido.fecha_ultima_actualizacion = datetime.now()
            self.db.commit()
        return pedido

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de un pedido existente
    # Retorna:
    #   Pedido | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, id_pedido, tipo_pedido, id_mesero, id_repartidor, id_cliente):
        pedido = self.obtener_por_id(id_pedido)
        if pedido:
            pedido.tipo_pedido = tipo_pedido
            pedido.Mesero_id_mesero = id_mesero
            pedido.Repartidor_id_repartidor = id_repartidor
            pedido.Cliente_id_cliente = id_cliente
            pedido.fecha_ultima_actualizacion = datetime.now()
            self.db.commit()
        return pedido

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un pedido por su ID
    # (falla si otras tablas dependen de este registro)
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_pedido):
        pedido = self.obtener_por_id(id_pedido)
        if pedido:
            self.db.delete(pedido)
            self.db.commit()
            return True
        return False
