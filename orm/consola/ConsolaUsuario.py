# ============================================================
# ConsolaUsuario.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume UsuarioDAO
# para realizar operaciones CRUD sobre la entidad Usuario
# ============================================================

from orm.dao import UsuarioDAO as udao
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = udao.UsuarioDAO(session)


# ------------------------------------------------------------
# Función: mostrar_usuarios
# Imprime en consola la lista de usuarios recibida
# (no se imprimen las credenciales)
#
# Parámetros:
#   usuarios (list[Usuario]) -- Lista de objetos Usuario a mostrar
#
# Retorna:
#   None
#
# Ejemplo:
#   usuarios = miDao.obtener_todos()
#   mostrar_usuarios(usuarios)
# ------------------------------------------------------------
def mostrar_usuarios(usuarios):
    if not usuarios:
        print("No hay registros.")
    else:
        for u in usuarios:
            print(f"ID: {u.idUsuario} | Nombre: {u.nombre} | Estado: {u.estado}")


# ------------------------------------------------------------
# Función: run
# Flujo principal de la aplicación — ejecuta en secuencia:
#   1. Listar todos los usuarios
#   2. Crear un nuevo usuario
#   3. Buscar por nombre
#   4. Editar un usuario existente
#   5. Desactivar un usuario
#   6. Eliminar un usuario
#
# Retorna:
#   None
# ------------------------------------------------------------
def run():

    # --- 1. Listar todos los usuarios ---
    print("=== Ver todos ===")
    mostrar_usuarios(miDao.obtener_todos())

    # --- 2. Crear nuevo usuario ---
    print("\n=== Crear usuario ===")
    idusuario    = int(input("Digite el id: "))
    nombre       = input("Digite el nombre: ")
    credenciales = input("Digite las credenciales: ")
    miDao.crear(idusuario, nombre, credenciales)
    mostrar_usuarios(miDao.obtener_todos())

    # --- 3. Buscar por nombre ---
    print("\n=== Buscar por nombre ===")
    nombreb  = input("Digite el nombre a buscar: ")
    usuarioE = miDao.obtener_por_nombre(nombreb)
    if usuarioE:
        mostrar_usuarios([usuarioE])
    else:
        print("Usuario no encontrado.")

    # --- 4. Editar usuario ---
    print("\n=== Editar usuario ===")
    idusuarioe    = int(input("Digite el id a editar: "))
    nombree       = input("Digite el nuevo nombre: ")
    credencialese = input("Digite las nuevas credenciales: ")
    if miDao.actualizar(idusuarioe, nombree, credencialese) is None:
        print("Usuario no encontrado.")
    mostrar_usuarios(miDao.obtener_todos())

    # --- 5. Desactivar usuario ---
    print("\n=== Desactivar usuario ===")
    idusuariod = int(input("Digite el id a desactivar: "))
    if miDao.desactivar(idusuariod) is None:
        print("Usuario no encontrado.")
    mostrar_usuarios(miDao.obtener_todos())

    # --- 6. Eliminar usuario ---
    print("\n=== Eliminar usuario ===")
    idusuarioel = int(input("Digite el id del usuario a eliminar: "))
    if not miDao.eliminar(idusuarioel):
        print("Usuario no encontrado.")
    mostrar_usuarios(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
