# ============================================================
# ConsolaMesa.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume MesaDAO
# para realizar operaciones CRUD sobre la entidad Mesa
# ============================================================

from orm.dao import MesaDAO as mdao
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = mdao.MesaDAO(session)


# ------------------------------------------------------------
# Función: mostrar_mesas
# Imprime en consola la lista de mesas recibida
#
# Parámetros:
#   mesas (list[Mesa]) -- Lista de objetos Mesa a mostrar
#
# Retorna:
#   None
#
# Ejemplo:
#   mesas = miDao.obtener_todos()
#   mostrar_mesas(mesas)
# ------------------------------------------------------------
def mostrar_mesas(mesas):
    if not mesas:
        print("No hay registros.")
    else:
        for m in mesas:
            print(f"ID: {m.id_mesa} | Número: {m.numero} | Estado: {m.estado}")


# ------------------------------------------------------------
# Función: run
# Flujo principal de la aplicación — ejecuta en secuencia:
#   1. Listar  
#   2. Crear  
#   3. Buscar por número  
#   4. Editar  
#   5. Eliminar
#
# Retorna:
#   None
# ------------------------------------------------------------
def run():

    # --- 1. Listar todas las mesas ---
    print("=== Ver todas ===")
    mostrar_mesas(miDao.obtener_todos())

    # --- 2. Crear nueva mesa ---
    print("\n=== Crear mesa ===")
    id_mesa = int(input("Digite el id: "))
    numero  = int(input("Digite el número de la mesa: "))
    estado  = input("Digite el estado (por ejemplo Disponible): ")
    miDao.crear(id_mesa, numero, estado)
    mostrar_mesas(miDao.obtener_todos())

    # --- 3. Buscar por número ---
    print("\n=== Buscar por número ===")
    numerob = int(input("Digite el número de mesa a buscar: "))
    mesaE   = miDao.obtener_por_numero(numerob)
    if mesaE:
        mostrar_mesas([mesaE])
    else:
        print("Mesa no encontrada.")

    # --- 4. Editar mesa ---
    print("\n=== Editar mesa ===")
    id_mesae = int(input("Digite el id a editar: "))
    numeroe  = int(input("Digite el nuevo número: "))
    estadoe  = input("Digite el nuevo estado: ")
    if miDao.actualizar(id_mesae, numeroe, estadoe) is None:
        print("Mesa no encontrada.")
    mostrar_mesas(miDao.obtener_todos())

    # --- 5. Eliminar mesa ---
    print("\n=== Eliminar mesa ===")
    id_mesael = int(input("Digite el id de la mesa a eliminar: "))
    if not miDao.eliminar(id_mesael):
        print("Mesa no encontrada.")
    mostrar_mesas(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
