# ============================================================
# ConsolaProducto.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume ProductoDAO
# para realizar operaciones CRUD sobre la entidad Producto
# ============================================================

from orm.dao import ProductoDAO as pdao
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = pdao.ProductoDAO(session)


# ------------------------------------------------------------
# Función: mostrar_productos
# Imprime en consola la lista de productos recibida
#
# Parámetros:
#   productos (list[Producto]) -- Lista de objetos Producto a mostrar
#
# Retorna:
#   None
#
# Ejemplo:
#   productos = miDao.obtener_todos()
#   mostrar_productos(productos)
# ------------------------------------------------------------
def mostrar_productos(productos):
    if not productos:
        print("No hay registros.")
    else:
        for p in productos:
            print(f"ID: {p.idProducto} | {p.nombre} | {p.descripcion} | "
                f"Precio: {p.precio} | Disponibles: {p.cantidad_disponible} | "
                f"Categoría: {p.Categoria_id_categoria}")


# ------------------------------------------------------------
# Función: run
# Flujo principal de la aplicación — ejecuta en secuencia:
#   1. Listar todos los productos
#   2. Crear un nuevo producto
#   3. Buscar por nombre
#   4. Editar un producto existente
#   5. Marcar un producto como agotado y ver solo los disponibles
#   6. Eliminar un producto
#
# Retorna:
#   None
# ------------------------------------------------------------
def run():

    # --- 1. Listar todos los productos ---
    print("=== Ver todos ===")
    mostrar_productos(miDao.obtener_todos())

    # --- 2. Crear nuevo producto ---
    print("\n=== Crear producto ===")
    idproducto  = int(input("Digite el id: "))
    nombre      = input("Digite el nombre: ")
    descripcion = input("Digite la descripción: ")
    precio      = float(input("Digite el precio: "))
    cantidad    = int(input("Digite la cantidad disponible: "))
    idcategoria = int(input("Digite el id de la categoría (debe existir): "))
    miDao.crear(idproducto, nombre, descripcion, precio, cantidad, idcategoria)
    mostrar_productos(miDao.obtener_todos())

    # --- 3. Buscar por nombre ---
    print("\n=== Buscar por nombre ===")
    nombreb   = input("Digite el nombre a buscar: ")
    productoE = miDao.obtener_por_nombre(nombreb)
    if productoE:
        mostrar_productos([productoE])
    else:
        print("Producto no encontrado.")

    # --- 4. Editar producto ---
    print("\n=== Editar producto ===")
    idproductoe  = int(input("Digite el id a editar: "))
    nombree      = input("Digite el nuevo nombre: ")
    descripcione = input("Digite la nueva descripción: ")
    precioe      = float(input("Digite el nuevo precio: "))
    cantidade    = int(input("Digite la nueva cantidad disponible: "))
    if miDao.actualizar(idproductoe, nombree, descripcione, precioe, cantidade) is None:
        print("Producto no encontrado.")
    mostrar_productos(miDao.obtener_todos())

    # --- 5. Disponibilidad (HU-12) ---
    print("\n=== Marcar producto como agotado ===")
    idproductoa = int(input("Digite el id del producto a marcar como agotado: "))
    if miDao.marcar_agotado(idproductoa) is None:
        print("Producto no encontrado.")
    print("Productos disponibles (los que un mesero puede agregar a un pedido):")
    mostrar_productos(miDao.obtener_disponibles())

    # --- 6. Eliminar producto ---
    print("\n=== Eliminar producto ===")
    idproductod = int(input("Digite el id del producto a eliminar: "))
    if not miDao.eliminar(idproductod):
        print("Producto no encontrado.")
    mostrar_productos(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
