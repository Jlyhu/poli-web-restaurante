# ============================================================
# DetallePedidoDAO.py
# Capa de acceso a datos (DAO) para la entidad DetallePedido, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'DetallePedido'
# ============================================================

from orm.modelos.DetallePedidoModel import DetallePedido
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: DetallePedidoDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = DetallePedidoDAO(session)
# ------------------------------------------------------------
class DetallePedidoDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo registro.
    # Falla si el id ya existe o si una llave foránea no existe.
    # Retorna: DetallePedido -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_detalle_pedido, cantidad, notas, Pedido_id_pedido, Producto_idProducto):
        nuevo = DetallePedido(
            id_detalle_pedido=id_detalle_pedido,
            cantidad=cantidad,
            notas=notas,
            Pedido_id_pedido=Pedido_id_pedido,
            Producto_idProducto=Producto_idProducto
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Retorna: DetallePedido -- El objeto encontrado, o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_detalle_pedido):
        return self.db.query(DetallePedido).filter(DetallePedido.id_detalle_pedido == id_detalle_pedido).first()

    # --------------------------------------------------------
    # Método: obtener_por_pedido
    # Busca por id de pedido.
    # Retorna: list[DetallePedido] -- Lista de registros encontrados (puede estar vacía)
    # --------------------------------------------------------
    def obtener_por_pedido(self, valor):
        return self.db.query(DetallePedido).filter(DetallePedido.Pedido_id_pedido == valor).all()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros.
    # Retorna: list[DetallePedido]
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(DetallePedido).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica un registro existente (el id no se modifica).
    # Retorna: DetallePedido -- El objeto actualizado, o None si no existe
    # --------------------------------------------------------
    def actualizar(self, id_detalle_pedido, cantidad, notas, Pedido_id_pedido, Producto_idProducto):
        registro = self.obtener_por_id(id_detalle_pedido)
        if registro:
            registro.cantidad = cantidad
            registro.notas = notas
            registro.Pedido_id_pedido = Pedido_id_pedido
            registro.Producto_idProducto = Producto_idProducto
            self.db.commit()
        return registro

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un registro.
    # Falla si otros registros dependen de él (llave foránea).
    # Retorna: bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_detalle_pedido):
        registro = self.obtener_por_id(id_detalle_pedido)
        if registro:
            self.db.delete(registro)
            self.db.commit()
            return True
        return False
