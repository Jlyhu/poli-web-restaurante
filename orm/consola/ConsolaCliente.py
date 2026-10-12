# ============================================================
# ConsolaCliente.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume ClienteDAO
# para realizar operaciones CRUD sobre la entidad Cliente
# ============================================================

from orm.dao import ClienteDAO as cdao
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = cdao.ClienteDAO(session)

# ------------------------------------------------------------
# Función: mostrar_clientes
# Imprime en consola la lista de clientes recibida

# Parámetros:
#   clientes (list[Cliente]) -- Lista de objetos Cliente a mostrar
#
# Retorna:
#   None
#
# Ejemplo:
#   clientes = miDao.obtener_todos()
#   mostrar_clientes(clientes)
# ------------------------------------------------------------
def mostrar_clientes(clientes):
    if not clientes:
        print("No hay registros.")
    else:
        for c in clientes:
            print(f"ID: {c.id_cliente} | Nombre: {c.nombre} | Dirección: {c.direccion} | Teléfono: {c.telefono}")


# ------------------------------------------------------------
# Función: run
# Flujo principal de la aplicación — ejecuta en secuencia:
#   1. Listar  
#   2. Crear  
#   3. Buscar por nombre  
#   4. Editar  
#   5. Eliminar
#
# Retorna:
#   None
# ------------------------------------------------------------
def run():

    # --- 1. Listar todos los clientes ---
    print("=== Ver todos ===")
    mostrar_clientes(miDao.obtener_todos())

    # --- 2. Crear nuevo cliente ---
    print("\n=== Crear cliente ===")
    id_cliente = int(input("Digite el id: "))
    nombre     = input("Digite el nombre: ")
    direccion  = input("Digite la dirección: ")
    telefono   = input("Digite el teléfono: ")
    miDao.crear(id_cliente, nombre, direccion, telefono)
    mostrar_clientes(miDao.obtener_todos())

    # --- 3. Buscar por nombre ---
    print("\n=== Buscar por nombre ===")
    nombreb  = input("Digite el nombre a buscar: ")
    clienteE = miDao.obtener_por_nombre(nombreb)
    if clienteE:
        mostrar_clientes([clienteE])
    else:
        print("Cliente no encontrado.")

    # --- 4. Editar cliente ---
    print("\n=== Editar cliente ===")
    id_clientee = int(input("Digite el id a editar: "))
    nombree     = input("Digite el nuevo nombre: ")
    direccione  = input("Digite la nueva dirección: ")
    telefonoe   = input("Digite el nuevo teléfono: ")
    if miDao.actualizar(id_clientee, nombree, direccione, telefonoe) is None:
        print("Cliente no encontrado.")
    mostrar_clientes(miDao.obtener_todos())

    # --- 5. Eliminar cliente ---
    print("\n=== Eliminar cliente ===")
    id_clienteel = int(input("Digite el id del cliente a eliminar: "))
    if not miDao.eliminar(id_clienteel):
        print("Cliente no encontrado.")
    mostrar_clientes(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()