# ============================================================
# ConsolaCategoria.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume CategoriaDAO
# para realizar operaciones CRUD sobre la entidad Categoria
# Ejecutar desde la carpeta principal:  python -m orm.consola.ConsolaCategoria
# ============================================================

from orm.dao import CategoriaDAO as dao_mod
from orm.models import SessionLocal

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.CategoriaDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_categoria} | Nombre: {r.nombre}")


# ------------------------------------------------------------
# Función: run
# Flujo principal — ejecuta en secuencia:
#   1. Listar todas las categorías
#   2. Crear una categoría
#   3. Buscar por nombre
#   4. Editar una categoría
#   5. Eliminar una categoría
# ------------------------------------------------------------
def run():
    # --- 1. Listar todas las categorías ---
    print("\n=== Listar todas las categorías ===")
    mostrar(miDao.obtener_todos())

    # --- 2. Crear una categoría ---
    print("\n=== Crear una categoría ===")
    id_c = int(input("Digite el id: "))
    nombre = input("Digite el nombre: ")
    miDao.crear(id_c, nombre)
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por nombre ---
    print("\n=== Buscar por nombre ===")
    nombreb = input("Digite el nombre a buscar: ")
    c = miDao.obtener_por_nombre(nombreb)
    mostrar([c] if c else [])

    # --- 4. Editar una categoría ---
    print("\n=== Editar una categoría ===")
    id_e = int(input("Digite el id a editar: "))
    nombre_e = input("Digite el nuevo nombre: ")
    if miDao.actualizar(id_e, nombre_e) is None:
        print("Categoría no encontrada.")
    mostrar(miDao.obtener_todos())

    # --- 5. Eliminar una categoría ---
    print("\n=== Eliminar una categoría ===")
    id_d = int(input("Digite el id de la categoría a eliminar: "))
    if not miDao.eliminar(id_d):
        print("Categoría no encontrada.")
    mostrar(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
