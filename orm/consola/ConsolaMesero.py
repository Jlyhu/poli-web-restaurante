# ============================================================
# ConsolaMesero.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume MeseroDAO
# para realizar operaciones CRUD sobre la entidad Mesero
# Ejecutar desde la carpeta principal:  python -m orm.consola.ConsolaMesero
# ============================================================

from orm.dao import MeseroDAO as dao_mod
from orm.models import SessionLocal

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.MeseroDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_mesero} | Zona: {r.zona_asignada} | Usuario: {r.Usuario_idUsuario}")


# ------------------------------------------------------------
# Función: run
# Flujo principal — ejecuta en secuencia:
#   1. Listar todos los meseros
#   2. Crear un mesero (el usuario ya debe existir)
#   3. Buscar por id
#   4. Editar
#   5. Eliminar
# ------------------------------------------------------------
def run():
    # --- 1. Listar todos los meseros ---
    print("\n=== Listar todos los meseros ===")
    mostrar(miDao.obtener_todos())

    # --- 2. Crear un mesero (el usuario ya debe existir) ---
    print("\n=== Crear un mesero (el usuario ya debe existir) ===")
    id_x = int(input("Digite el id: "))
    valor = input("Digite Zona: ")
    id_usuario = int(input("Digite el id del usuario: "))
    miDao.crear(id_x, valor, id_usuario)
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por id ---
    print("\n=== Buscar por id ===")
    id_b = int(input("Digite el id a buscar: "))
    x = miDao.obtener_por_id(id_b)
    mostrar([x] if x else [])

    # --- 4. Editar ---
    print("\n=== Editar ===")
    id_e = int(input("Digite el id a editar: "))
    valor_e = input("Digite Zona nueva: ")
    id_usuario_e = int(input("Digite el id del usuario: "))
    if miDao.actualizar(id_e, valor_e, id_usuario_e) is None:
        print("No encontrado.")
    mostrar(miDao.obtener_todos())

    # --- 5. Eliminar ---
    print("\n=== Eliminar ===")
    id_d = int(input("Digite el id a eliminar: "))
    if not miDao.eliminar(id_d):
        print("No encontrado.")
    mostrar(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
