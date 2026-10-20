# ============================================================
# ConsolaAdministrador.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume AdministradorDAO
# para realizar operaciones CRUD sobre la entidad Administrador
# Ejecutar desde la raíz del repo:  python -m orm.consola.ConsolaAdministrador
# ============================================================

from orm.dao import AdministradorDAO as dao_mod
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.AdministradorDAO(session)


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista de registros recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_administrador} | Id del usuario: {r.Usuario_idUsuario}")


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
    print("\n=== Crear administrador ===")
    id_administrador = int(input("Digite el id: "))
    Usuario_idUsuario = int(input("Digite el id del usuario (debe existir): "))
    ejecutar(lambda: miDao.crear(id_administrador, Usuario_idUsuario))
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por id de usuario ---
    print("\n=== Buscar por id de usuario ===")
    valor = int(input("Digite el id de usuario a buscar: "))
    mostrar(miDao.obtener_por_usuario(valor))

    # --- 4. Editar ---
    print("\n=== Editar administrador ===")
    id_e = int(input("Digite el id a editar: "))
    Usuario_idUsuario = int(input("Digite el nuevo id del usuario (debe existir): "))
    if ejecutar(lambda: miDao.actualizar(id_e, Usuario_idUsuario)) is None:
        print("Registro no encontrado (o la base de datos lo rechazó).")
    mostrar(miDao.obtener_todos())

    # --- 5. Eliminar ---
    print("\n=== Eliminar administrador ===")
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
