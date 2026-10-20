# ============================================================
# ConsolaCaja.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume CajaDAO
# para realizar operaciones CRUD sobre la entidad Caja
# Ejecutar desde la carpeta principal:  python -m orm.consola.ConsolaCaja
# ============================================================

from orm.dao import CajaDAO as dao_mod
from orm.models import SessionLocal

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.CajaDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_caja} | Apertura: {r.fecha_apertura} | Cierre: {r.fecha_cierre} | Inicial: {r.monto_inicial} | Final: {r.monto_final} | Cajero: {r.Cajero_id_cajero}")


# ------------------------------------------------------------
# Función: run
# Flujo principal — ejecuta en secuencia:
#   1. Listar todas las cajas
#   2. Abrir una caja (el cajero ya debe existir)
#   3. Cerrar una caja
#   4. Buscar por id
#   5. Editar
#   6. Eliminar (falla si la caja ya tiene pagos)
# ------------------------------------------------------------
def run():
    # --- 1. Listar todas las cajas ---
    print("\n=== Listar todas las cajas ===")
    mostrar(miDao.obtener_todos())

    # --- 2. Abrir una caja (el cajero ya debe existir) ---
    print("\n=== Abrir una caja (el cajero ya debe existir) ===")
    id_x = int(input("Digite el id: "))
    monto = float(input("Digite el monto inicial: "))
    id_cajero = int(input("Digite el id del cajero: "))
    miDao.crear(id_x, monto, id_cajero)
    mostrar(miDao.obtener_todos())

    # --- 3. Cerrar una caja ---
    print("\n=== Cerrar una caja ===")
    id_c = int(input("Digite el id de la caja a cerrar: "))
    monto_f = float(input("Digite el monto final: "))
    if miDao.cerrar(id_c, monto_f) is None:
        print("Caja no encontrada.")
    mostrar(miDao.obtener_todos())

    # --- 4. Buscar por id ---
    print("\n=== Buscar por id ===")
    id_b = int(input("Digite el id a buscar: "))
    x = miDao.obtener_por_id(id_b)
    mostrar([x] if x else [])

    # --- 5. Editar ---
    print("\n=== Editar ===")
    id_e = int(input("Digite el id a editar: "))
    monto_i = float(input("Digite el monto inicial: "))
    monto_f = float(input("Digite el monto final: "))
    id_cajero = int(input("Digite el id del cajero: "))
    if miDao.actualizar(id_e, monto_i, monto_f, id_cajero) is None:
        print("Caja no encontrada.")
    mostrar(miDao.obtener_todos())

    # --- 6. Eliminar (falla si la caja ya tiene pagos) ---
    print("\n=== Eliminar (falla si la caja ya tiene pagos) ===")
    id_d = int(input("Digite el id a eliminar: "))
    if not miDao.eliminar(id_d):
        print("Caja no encontrada.")
    mostrar(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
