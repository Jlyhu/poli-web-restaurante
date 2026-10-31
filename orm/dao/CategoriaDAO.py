# ============================================================
# CategoriaDAO.py
# Capa de acceso a datos (DAO) para la entidad Categoria, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Categoria'
# ============================================================

from orm.modelos.CategoriaModel import Categoria
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: CategoriaDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = CategoriaDAO(session)
# ------------------------------------------------------------
class CategoriaDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta una categoría nuevo
    # Retorna:
    #   Categoria -- El objeto recién creado y persistido
    # --------------------------------------------------------
    def crear(self, id_categoria, nombre):
        nuevo = Categoria(
            id_categoria=id_categoria,
            nombre=nombre,
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)  # sincroniza el objeto con los datos de la BD
        return nuevo

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca por clave primaria
    # Retorna:
    #   Categoria | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, id_categoria):
        return self.db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los registros de la tabla Categoria
    # Retorna:
    #   list[Categoria] -- Lista de objetos (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Categoria).order_by(Categoria.id_categoria).all()

    # --------------------------------------------------------
    # Método: obtener_por_nombre
    # Busca la primera categoría que coincida con el nombre dado
    # Retorna:
    #   Categoria | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_nombre(self, nombre):
        return self.db.query(Categoria).filter(Categoria.nombre == nombre).first()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de una categoría existente
    # Retorna:
    #   Categoria | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, id_categoria, nuevo_nombre):
        categoria = self.obtener_por_id(id_categoria)
        if categoria:
            categoria.nombre = nuevo_nombre
            self.db.commit()
        return categoria

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina una categoría por su ID
    # (falla si otras tablas dependen de este registro)
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, id_categoria):
        categoria = self.obtener_por_id(id_categoria)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False
