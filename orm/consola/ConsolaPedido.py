# ============================================================
# ConsolaPedido.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume PedidoDAO
# para realizar operaciones CRUD sobre la entidad Pedido
# Ejecutar desde la carpeta principal:  python -m orm.consola.ConsolaPedido
# ============================================================

from orm.dao import PedidoDAO as dao_mod
from orm.models import SessionLocal

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = dao_mod.PedidoDAO(session)


# Convierte el texto escrito en un entero; si se deja vacío devuelve None
def entero_o_none(texto):
    return int(texto) if texto.strip() else None


# ------------------------------------------------------------
# Función: mostrar
# Imprime en consola la lista recibida
# ------------------------------------------------------------
def mostrar(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_pedido} | Estado: {r.estado} | Tipo: {r.tipo_pedido} | Creado: {r.fecha_creacion} | Actualizado: {r.fecha_ultima_actualizacion} | Mesero: {r.Mesero_id_mesero} | Repartidor: {r.Repartidor_id_repartidor} | Cliente: {r.Cliente_id_cliente}")


# ------------------------------------------------------------
# Función: run
# Flujo principal — ejecuta en secuencia:
#   1. Listar todos los pedidos
#   2. Crear un pedido (lo que se deje vacío queda sin asignar)
#   3. Buscar por id
#   4. Listar por estado
#   5. Cambiar el estado
#   6. Editar
#   7. Eliminar (falla si el pedido ya tiene detalles o pagos)
# ------------------------------------------------------------
def run():
    # --- 1. Listar todos los pedidos ---
    print("\n=== Listar todos los pedidos ===")
    mostrar(miDao.obtener_todos())

    # --- 2. Crear un pedido (lo que se deje vacío queda sin asignar) ---
    print("\n=== Crear un pedido (lo que se deje vacío queda sin asignar) ===")
    id_x = int(input("Digite el id: "))
    tipo = input("Digite el tipo de pedido (SALON, DOMICILIO...): ")
    id_mesero = entero_o_none(input("Digite el id del mesero (vacío si no aplica): "))
    id_repartidor = entero_o_none(input("Digite el id del repartidor (vacío si no aplica): "))
    id_cliente = entero_o_none(input("Digite el id del cliente (vacío si no aplica): "))
    miDao.crear(id_x, tipo, id_mesero, id_repartidor, id_cliente)
    mostrar(miDao.obtener_todos())

    # --- 3. Buscar por id ---
    print("\n=== Buscar por id ===")
    id_b = int(input("Digite el id a buscar: "))
    x = miDao.obtener_por_id(id_b)
    mostrar([x] if x else [])

    # --- 4. Listar por estado ---
    print("\n=== Listar por estado ===")
    estado = input("Digite el estado (PENDIENTE, EN PREPARACION, LISTO, ENTREGADO, CANCELADO): ")
    mostrar(miDao.obtener_por_estado(estado))

    # --- 5. Cambiar el estado ---
    print("\n=== Cambiar el estado ===")
    id_s = int(input("Digite el id del pedido: "))
    nuevo = input("Digite el nuevo estado: ")
    if miDao.actualizar_estado(id_s, nuevo) is None:
        print("Pedido no encontrado.")
    mostrar(miDao.obtener_todos())

    # --- 6. Editar ---
    print("\n=== Editar ===")
    id_e = int(input("Digite el id a editar: "))
    tipo_e = input("Digite el tipo de pedido: ")
    mesero_e = entero_o_none(input("Digite el id del mesero (vacío si no aplica): "))
    repartidor_e = entero_o_none(input("Digite el id del repartidor (vacío si no aplica): "))
    cliente_e = entero_o_none(input("Digite el id del cliente (vacío si no aplica): "))
    if miDao.actualizar(id_e, tipo_e, mesero_e, repartidor_e, cliente_e) is None:
        print("Pedido no encontrado.")
    mostrar(miDao.obtener_todos())

    # --- 7. Eliminar (falla si el pedido ya tiene detalles o pagos) ---
    print("\n=== Eliminar (falla si el pedido ya tiene detalles o pagos) ===")
    id_d = int(input("Digite el id a eliminar: "))
    if not miDao.eliminar(id_d):
        print("Pedido no encontrado.")
    mostrar(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
