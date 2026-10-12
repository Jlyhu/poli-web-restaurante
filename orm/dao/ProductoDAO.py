# ============================================================
# ProductoDAO.py
# Capa de acceso a datos (DAO) para la entidad Producto, con ORM
# Encapsula todas las operaciones CRUD sobre la tabla 'Producto'
# ============================================================

from orm.modelos.ProductoModel import Producto
from sqlalchemy.orm import Session


# ------------------------------------------------------------
# Clase: ProductoDAO
# Parámetros del constructor:
#   db_session (Session) -- Sesión activa de SQLAlchemy
#
# Ejemplo de uso:
#   session = SessionLocal()
#   dao = ProductoDAO(session)
# ------------------------------------------------------------
class ProductoDAO:

    # Recibe la sesión de base de datos por inyección de dependencias
    def __init__(self, db_session: Session):
        self.db = db_session

    # --------------------------------------------------------
    # Método: crear
    # Inserta un nuevo producto. La categoría debe existir en
    # la base de datos, si no, MySQL rechaza el insert.
    # Parámetros:
    #   idproducto          (int/str) -- Identificador único del producto
    #   nombre              (str)     -- Nombre del producto
    #   descripcion         (str)     -- Descripción del producto
    #   precio              (float)   -- Precio del producto
    #   cantidad_disponible (int)     -- Cantidad disponible del producto
    #   id_categoria        (int/str) -- Identificador de la categoría a la que pertenece el producto
    # Retorna:
    #   Producto -- El objeto recién creado y persistido
    #
    # Ejemplo:
    #   p = dao.crear(1, "Jugo de mora", "Natural", 6500, 20, 1)
    # --------------------------------------------------------
    def crear(self, idproducto, nombre, descripcion, precio, cantidad_disponible, id_categoria):
        nuevo_producto = Producto(
            idProducto=idproducto,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad_disponible=cantidad_disponible,
            Categoria_id_categoria=id_categoria
        )
        self.db.add(nuevo_producto)
        self.db.commit()
        self.db.refresh(nuevo_producto)  # sincroniza el objeto con los datos de la BD
        return nuevo_producto

    # --------------------------------------------------------
    # Método: obtener_por_id
    # Busca un producto por su clave primaria
    # Parámetros:
    #   idproducto (int/str) -- Identificador único del producto
    # Retorna:
    #   Producto | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_id(self, idproducto):
        return self.db.query(Producto).filter(Producto.idProducto == idproducto).first()

    # --------------------------------------------------------
    # Método: obtener_por_nombre
    # Busca el primer producto que coincida con el nombre dado
    # Parámetros:
    #   nombre (str) -- Nombre del producto a buscar
    # Retorna:
    #   Producto | None -- El objeto encontrado o None si no existe
    # --------------------------------------------------------
    def obtener_por_nombre(self, nombre):
        return self.db.query(Producto).filter(Producto.nombre == nombre).first()

    # --------------------------------------------------------
    # Método: obtener_todos
    # Recupera todos los productos de la tabla
    # PArámetros: ninguno
    # Retorna:
    #   list[Producto] -- Lista de objetos Producto (puede ser vacía)
    # --------------------------------------------------------
    def obtener_todos(self):
        return self.db.query(Producto).all()

    # --------------------------------------------------------
    # Método: obtener_disponibles
    # Recupera solo los productos con unidades disponibles
    # (los que un mesero puede agregar a un pedido)
    # Parámetros: ninguno
    # Retorna:
    #   list[Producto] -- Productos con cantidad_disponible mayor a 0
    # --------------------------------------------------------
    def obtener_disponibles(self):
        return self.db.query(Producto).filter(Producto.cantidad_disponible > 0).all()

    # --------------------------------------------------------
    # Método: actualizar
    # Modifica los datos de un producto existente. También sirve
    # para volver a poner unidades disponibles de un producto agotado.
    # Parámetros:
    #   idproducto          (int/str) -- Identificador único del producto a modificar
    #   nuevo_nombre        (str)     -- Nuevo nombre del producto
    #   nueva_descripcion   (str)     -- Nueva descripción del producto
    #   nuevo_precio        (float)   -- Nuevo precio del producto
    #   nueva_cantidad      (int)     -- Nueva cantidad disponible del producto
    # Retorna:
    #   Producto | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def actualizar(self, idproducto, nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_cantidad):
        producto = self.obtener_por_id(idproducto)
        if producto:
            producto.nombre              = nuevo_nombre
            producto.descripcion         = nueva_descripcion
            producto.precio              = nuevo_precio
            producto.cantidad_disponible = nueva_cantidad
            self.db.commit()
        return producto

    # --------------------------------------------------------
    # Método: marcar_agotado  (HU-12)
    # Deja la cantidad disponible en 0, así el producto deja de
    # aparecer en obtener_disponibles()
    # Parámetros:
    #   idproducto (int/str) -- Identificador único del producto a marcar como
    # Retorna:
    #   Producto | None -- El objeto actualizado, o None si no se encontró
    # --------------------------------------------------------
    def marcar_agotado(self, idproducto):
        producto = self.obtener_por_id(idproducto)
        if producto:
            producto.cantidad_disponible = 0
            self.db.commit()
        return producto

    # --------------------------------------------------------
    # Método: eliminar
    # Elimina un producto de la base de datos por su ID
    # (falla si ya está en algún pedido: en ese caso, marcarlo agotado)
    # Parámetros:
    #   idproducto (int/str) -- Identificador único del producto a eliminar
    # Retorna:
    #   bool -- True si se eliminó, False si no existía
    # --------------------------------------------------------
    def eliminar(self, idproducto):
        producto = self.obtener_por_id(idproducto)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
