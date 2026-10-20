# ============================================================
# ConsolaDetallePedido.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume DetallePedidoDAO
# para realizar operaciones CRUD sobre la entidad DetallePedido
# Ejecutar desde la raíz del repo:  python -m orm.consola.ConsolaDetallePedido
# ============================================================

from orm.dao import DetallePedidoDAO as dao_mod
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.DetallePedidoDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista de registros recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_detalle_pedido} | Cantidad: {r.cantidad} | Notas: {r.notas} | Id del pedido: {r.Pedido_id_pedido} | Id del producto: {r.Producto_idProducto}")


# ------------------------------------------------------------
# Función: ejecutar
# Ejecuta una operación de base de datos. Si MySQL la rechaza
# (id repetido, llave foránea inexistente, dependencias...)
# deshace la transacción y muestra el motivo en lugar de cerrar el programa.
# ------------------------------------------------------------
def ejecutar(accion):
    try:
        return accion()
    except SQLAlchemyError as e:
        session.rollback()
        print("Error de base de datos:", getattr(e, "orig", e))
        return None


# ------------------------------------------------------------
# Función: run
# Flujo principal — ejecuta en secuencia:
#   1. Listar   2. Crear   3. Buscar   4. Editar   5. Eliminar
# ------------------------------------------------------------
def run():

    # --- 1. Listar todos ---
    print("=== Ver todos ===")
    mostrar(miDao.obtener_todos())

    # --- 2. Crear ---
    print("\n=== Crear detalle de pedido ===")
    id_detalle_pedido = int(input("Digite el id: "))
    cantidad = int(input("Digite la cantidad: "))
    notas = input("Digite las notas: ")
    Pedido_id_pedido = int(input("Digite el id del pedido (debe existir): "))
    Producto_idProducto = int(input("Digite el id del producto (debe existir): "))
    ejecutar(lambda: miDao.crear(id_detalle_pedido, cantidad, notas, Pedido_id_pedido, Producto_idProducto))
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por id de pedido ---
    print("\n=== Buscar por id de pedido ===")
    valor = int(input("Digite el id de pedido a buscar: "))
    mostrar(miDao.obtener_por_pedido(valor))

    # --- 4. Editar ---
    print("\n=== Editar detalle de pedido ===")
    id_e = int(input("Digite el id a editar: "))
    cantidad = int(input("Digite la nueva cantidad: "))
    notas = input("Digite las nuevas notas: ")
    Pedido_id_pedido = int(input("Digite el nuevo id del pedido (debe existir): "))
    Producto_idProducto = int(input("Digite el nuevo id del producto (debe existir): "))
    if ejecutar(lambda: miDao.actualizar(id_e, cantidad, notas, Pedido_id_pedido, Producto_idProducto)) is None:
        print("Registro no encontrado (o la base de datos lo rechazó).")
    mostrar(miDao.obtener_todos())

    # --- 5. Eliminar ---
    print("\n=== Eliminar detalle de pedido ===")
    id_el = int(input("Digite el id a eliminar: "))
    if ejecutar(lambda: miDao.eliminar(id_el)) is False:
        print("Registro no encontrado.")
    mostrar(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    try:
        run()
    except ValueError:
        print("Debe digitar un número válido.")
