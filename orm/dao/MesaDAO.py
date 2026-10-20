# ============================================================
# MesaDAO.py
# Capa de acceso a datos (DAO) para la entidad Mesa, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Mesa'
# ============================================================

from orm.modelos.MesaModel import Mesa
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: MesaDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = MesaDAO(session)
# ------------------------------------------------------------
class MesaDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta una nueva mesa.    #
    # Parámetros:
    #   id_mesa (int/str) -- Identificador único de la mesa
    #   numero (int)      -- Número de la mesa
    #   estado (str)      -- Estado de la mesa ('disponible', 'ocupada', etc.)
    # Retorna:
    #   Mesa -- El objeto recién creado y persistido
    # Ejemplo:
    #   m = dao.crear(id_mesa=1, numero=10, estado='disponible')
    # --------------------------------------------------------

    def crear(self, id_mesa, numero, estado):
        nueva_mesa = Mesa(id_mesa=id_mesa, numero=numero, estado=estado)
        self.db.add(nueva_mesa)
        self.db.commit()
        self.db.refresh(nueva_mesa)  # sincroniza el objeto con los datos de la BD
        return nueva_mesa
    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria.
    # Parámetros:
    #   id_mesa (int/str) -- Identificador único de la mesa
    # Retorna:
    #   Mesa -- El objeto encontrado, o None si no existe
    # Ejemplo:
    #   m = dao.obtener_por_id(1)
    # --------------------------------------------------------
    def obtener_por_id(self, id_mesa):
        return self.db.query(Mesa).filter(Mesa.id_mesa == id_mesa).first()

    # --------------------------------------------------------
    # Método: obtener_por_numero
    # Busca por número de mesa.
    # Parámetros:
    #   numero (int) -- Número de la mesa
    # Retorna:
    #   Mesa -- El objeto encontrado, o None si no existe
    # Ejemplo:
    #   m = dao.obtener_por_numero(10)
    # --------------------------------------------------------
    def obtener_por_numero(self, numero):
        return self.db.query(Mesa).filter(Mesa.numero == numero).first()
    #--------------------------------------------------------
    # Método: obtener_todos
    # Recupera todas las mesas.
    # Parámetros: ninguno
    # Retorna:
    #   list[Mesa] -- Lista de todas las mesas en la base de datos
    # Ejemplo:
    #   mesas = dao.obtener_todos()
    #--------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Mesa).all()

    #--------------------------------------------------------
    # Método: actualizar
    # Modifica una mesa existente.
    # Parámetros:
    #   id_mesa (int/str) -- Identificador único de la mesa a modificar
    #   nuevo_numero (int) -- Nuevo número de la mesa
    #   nuevo_estado (str) -- Nuevo estado de la mesa
    # Retorna:  
    #   Mesa -- El objeto actualizado, o None si no existe
    # Ejemplo:
    #   m = dao.actualizar(1, nuevo_numero=20, nuevo_estado='ocupada')
    #--------------------------------------------------------
    def actualizar(self, id_mesa, nuevo_numero, nuevo_estado):
        mesa = self.obtener_por_id(id_mesa)
        if mesa:
            mesa.numero = nuevo_numero
            mesa.estado = nuevo_estado
            self.db.commit()
        return mesa

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina una mesa.
    # Falla si la mesa ya está en alguna reservación o pedido.
    # Parámetros:
    #   id_mesa (int/str) -- Identificador único de la mesa a eliminar
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_mesa):
        mesa = self.obtener_por_id(id_mesa)
        if mesa:
            self.db.delete(mesa)
            self.db.commit()
            return True
        return False
