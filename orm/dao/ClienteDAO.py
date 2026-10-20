# ============================================================
# ClienteDAO.py
# Capa de acceso a datos (DAO) para la entidad Cliente, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Cliente'
# ============================================================

from orm.modelos.ClienteModel import Cliente
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: ClienteDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = ClienteDAO(session)
# ------------------------------------------------------------
class ClienteDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo cliente.
    #
    # Parámetros:
    #   idcliente     (int/str) -- Identificador único
    #   nombre        (str)     -- Nombre del cliente
    #   direccion      (str)     -- Dirección del cliente
    #   telefono         (str)     -- Número de teléfono
    #
    # Retorna:
    #   Cliente -- El objeto recién creado y persistido
    #
    # Ejemplo:
    #   p = dao.crear(idcliente=1, nombre="Juan", direccion="Calle 123", telefono="555-1234")
    # --------------------------------------------------------

    def crear(self, id_cliente, nombre, direccion, telefono):
        nuevo_cliente = Cliente(
            id_cliente=id_cliente,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        self.db.add(nuevo_cliente)
        self.db.commit()
        self.db.refresh(nuevo_cliente)  # sincroniza el objeto con los datos de la BD
        return nuevo_cliente
    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Parámetros:
    #   id_cliente (int/str) -- Identificador único del cliente
    # Retorna:
    #   Cliente -- El objeto encontrado, o None si no existe
    # Ejemplo:
    #  cliente = dao.obtener_por_id(1)
    # --------------------------------------------------------
    def obtener_por_id(self, id_cliente):
        return self.db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

    # --------------------------------------------------------
    # Método: obtener_por_nombre
    # Busca por nombre.
    # Parámetros:
    #   nombre (str) -- Nombre del cliente
    # Retorna:
    #   Cliente -- El objeto encontrado, o None si no existe
    # Ejemplo:
    #  cliente = dao.obtener_por_nombre("Juan")
    # --------------------------------------------------------

    def obtener_por_nombre(self, nombre):
        return self.db.query(Cliente).filter(Cliente.nombre == nombre).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los clientes.
    # Parámetros: ninguno
    # Retorna:
    #   list[Cliente] -- Lista de todos los clientes en la base de datos
    # Ejemplo:
    #  clientes = dao.obtener_todos()
    #--------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Cliente).all()

    #--------------------------------------------------------
    # Método: actualizar
    # Modifica un cliente existente.
    # Parámetros:
    #   id_cliente      (int/str) -- Identificador único del cliente a modificar
    #   nuevo_nombre    (str)     -- Nuevo nombre del cliente
    #   nueva_direccion (str)     -- Nueva dirección del cliente
    #   nuevo_telefono  (str)     -- Nuevo número de teléfono del cliente
    # Retorna:
    #   Cliente -- El objeto actualizado, o None si no existe
    # Ejemplo:
    #  cliente = dao.actualizar(1, "Juan Pérez", "Calle 456", "555-5678")
    #--------------------------------------------------------
    def actualizar(self, id_cliente, nuevo_nombre, nueva_direccion, nuevo_telefono):
        cliente = self.obtener_por_id(id_cliente)
        if cliente:
            cliente.nombre    = nuevo_nombre
            cliente.direccion = nueva_direccion
            cliente.telefono  = nuevo_telefono
            self.db.commit()
        return cliente

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un cliente.
    # Falla si el cliente ya tiene reservaciones o pedidos asociados.
    # Parámetros:
    #   id_cliente (int/str) -- Identificador único del cliente a eliminar
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_cliente):
        cliente = self.obtener_por_id(id_cliente)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
