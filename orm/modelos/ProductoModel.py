# ============================================================
# ProductoModel.py
# Modelo Producto, mapeado a la tabla 'Producto' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from sqlalchemy import Column, Float, Integer, String

from orm.models import Base


# ------------------------------------------------------------
# Clase: Producto
# Atributos:
#   idProducto             (int)   -- Clave primaria
#   nombre                 (str)   -- Nombre del producto
#   descripcion            (str)   -- Descripción corta
#   precio                 (float) -- Precio de venta
#   cantidad_disponible    (int)   -- Unidades disponibles (0 = agotado)
#   Categoria_id_categoria (int)   -- id de la categoría a la que pertenece
# ------------------------------------------------------------
class Producto(Base):
    __tablename__ = 'Producto'   # mismo nombre (y mayúsculas) que en la base de datos

    # autoincrement=False: en la tabla el id NO se genera solo, hay que enviarlo
    idProducto             = Column(Integer, primary_key=True, autoincrement=False)
    nombre                 = Column(String(100), nullable=True)
    descripcion            = Column(String(100), nullable=True)
    precio                 = Column(Float, nullable=True)
    cantidad_disponible    = Column(Integer, nullable=True)

    # Referencia a Categoria.id_categoria. La llave foránea la controla la base de datos:
    # si la categoría no existe, MySQL rechaza el producto. Se deja como Integer simple
    # para no depender del archivo del modelo Categoria (que lo hace otra persona del equipo).
    Categoria_id_categoria = Column(Integer, nullable=False)
