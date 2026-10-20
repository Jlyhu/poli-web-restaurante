# ============================================================
# ConsolaPedidoMesa.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume PedidoMesaDAO
# para realizar operaciones CRUD sobre la entidad PedidoMesa
# Ejecutar desde la raíz del repo:  python -m orm.consola.ConsolaPedidoMesa
# ============================================================

from orm.dao import PedidoMesaDAO as dao_mod
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.PedidoMesaDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista de registros recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_pedido_mesa} | Id de la mesa: {r.Mesa_id_mesa} | Id del pedido: {r.Pedido_id_pedido}")


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
    print("\n=== Crear pedido de mesa ===")
    id_pedido_mesa = int(input("Digite el id: "))
    Mesa_id_mesa = int(input("Digite el id de la mesa (debe existir): "))
    Pedido_id_pedido = int(input("Digite el id del pedido (debe existir): "))
    ejecutar(lambda: miDao.crear(id_pedido_mesa, Mesa_id_mesa, Pedido_id_pedido))
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por id de mesa ---
    print("\n=== Buscar por id de mesa ===")
    valor = int(input("Digite el id de mesa a buscar: "))
    mostrar(miDao.obtener_por_mesa(valor))

    # --- 4. Editar ---
    print("\n=== Editar pedido de mesa ===")
    id_e = int(input("Digite el id a editar: "))
    Mesa_id_mesa = int(input("Digite el nuevo id de la mesa (debe existir): "))
    Pedido_id_pedido = int(input("Digite el nuevo id del pedido (debe existir): "))
    if ejecutar(lambda: miDao.actualizar(id_e, Mesa_id_mesa, Pedido_id_pedido)) is None:
        print("Registro no encontrado (o la base de datos lo rechazó).")
    mostrar(miDao.obtener_todos())

    # --- 5. Eliminar ---
    print("\n=== Eliminar pedido de mesa ===")
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
