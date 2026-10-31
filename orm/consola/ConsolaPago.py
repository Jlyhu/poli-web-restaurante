# ============================================================
# ConsolaPago.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume PagoDAO
# para realizar operaciones CRUD sobre la entidad Pago
# Ejecutar desde la raíz del repo:  python -m orm.consola.ConsolaPago
# ============================================================

from datetime import datetime

from orm.dao import PagoDAO as dao_mod
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.PagoDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista de registros recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_pago} | Monto: {r.monto} | Método de pago: {r.metodo_pago} | Fecha de pago: {r.fecha_pago} | Id del pedido: {r.Pedido_id_pedido} | Id de la caja: {r.Caja_id_caja}")


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
    print("\n=== Crear pago ===")
    id_pago = int(input("Digite el id: "))
    monto = float(input("Digite el monto: "))
    metodo_pago = input("Digite el método de pago: ")
    fecha_pago = datetime.now()   # se registra la fecha y hora actuales
    Pedido_id_pedido = int(input("Digite el id del pedido (debe existir): "))
    Caja_id_caja = int(input("Digite el id de la caja (debe existir): "))
    ejecutar(lambda: miDao.crear(id_pago, monto, metodo_pago, fecha_pago, Pedido_id_pedido, Caja_id_caja))
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por id de pedido ---
    print("\n=== Buscar por id de pedido ===")
    valor = int(input("Digite el id de pedido a buscar: "))
    mostrar(miDao.obtener_por_pedido(valor))

    # --- 4. Editar ---
    print("\n=== Editar pago ===")
    id_e = int(input("Digite el id a editar: "))
    monto = float(input("Digite el nuevo monto: "))
    metodo_pago = input("Digite el nuevo método de pago: ")
    Pedido_id_pedido = int(input("Digite el nuevo id del pedido (debe existir): "))
    Caja_id_caja = int(input("Digite el nuevo id de la caja (debe existir): "))
    if ejecutar(lambda: miDao.actualizar(id_e, monto, metodo_pago, Pedido_id_pedido, Caja_id_caja)) is None:
        print("Registro no encontrado (o la base de datos lo rechazó).")
    mostrar(miDao.obtener_todos())

    # --- 5. Eliminar ---
    print("\n=== Eliminar pago ===")
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
