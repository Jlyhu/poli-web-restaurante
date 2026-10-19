# ============================================================
# ConsolaReservacion.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume ReservacionDAO
# para realizar operaciones CRUD sobre la entidad Reservacion
#
# Requiere un cliente creado antes (ver ConsolaCliente.py).
# ============================================================

from datetime import datetime

from orm.dao import ReservacionDAO as rdao
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = rdao.ReservacionDAO(session)

# ------------------------------------------------------------
# Función: mostrar_reservaciones
# Imprime en consola la lista de reservaciones recibida
#
# Parámetros:
#   reservaciones (list[Reservacion]) -- Lista de objetos Reservacion a mostrar
#
# Retorna:
#   None
#
# Ejemplo:
#   reservaciones = miDao.obtener_todos()
#   mostrar_reservaciones(reservaciones)
# ------------------------------------------------------------
def mostrar_reservaciones(reservaciones):
    if not reservaciones:
        print("No hay registros.")
    else:
        for r in reservaciones:
            print(f"ID: {r.id_reservacion} | Fecha: {r.fecha} | Hora: {r.hora} | "
                f"Personas: {r.numero_personas} | Estado: {r.estado} | Cliente: {r.Cliente_id_cliente}")


# Convierte el texto escrito por el usuario en objetos datetime
# (fecha: AAAA-MM-DD, hora: HH:MM). Si el formato está mal, lanza ValueError.
def leer_fecha_y_hora():
    fecha_txt = input("Digite la fecha (AAAA-MM-DD): ")
    hora_txt  = input("Digite la hora (HH:MM): ")
    fecha = datetime.strptime(fecha_txt, "%Y-%m-%d")
    hora  = datetime.strptime(f"{fecha_txt} {hora_txt}", "%Y-%m-%d %H:%M")
    return fecha, hora


# ------------------------------------------------------------
# Flujo principal de la aplicación — ejecuta en secuencia:
#   1. Listar  
#   2. Crear  
#   3. Buscar por cliente  
#   4. Editar  
#   5. Eliminar
#
# Retorna:
#   None
# ------------------------------------------------------------
def run():

    # --- 1. Listar todas las reservaciones ---
    print("=== Ver todas ===")
    mostrar_reservaciones(miDao.obtener_todos())

    # --- 2. Crear nueva reservación ---
    print("\n=== Crear reservación ===")
    id_reservacion  = int(input("Digite el id: "))
    fecha, hora     = leer_fecha_y_hora()
    numero_personas = int(input("Digite el número de personas: "))
    estado          = input("Digite el estado (por ejemplo Pendiente): ")
    id_cliente      = int(input("Digite el id del cliente (debe existir): "))
    miDao.crear(id_reservacion, fecha, hora, numero_personas, estado, id_cliente)
    mostrar_reservaciones(miDao.obtener_todos())

    # --- 3. Buscar por cliente ---
    print("\n=== Buscar por cliente ===")
    id_clienteb = int(input("Digite el id del cliente: "))
    mostrar_reservaciones(miDao.obtener_por_cliente(id_clienteb))

    # --- 4. Editar reservación ---
    print("\n=== Editar reservación ===")
    id_reservacione  = int(input("Digite el id a editar: "))
    fechae, horae    = leer_fecha_y_hora()
    personase        = int(input("Digite el nuevo número de personas: "))
    estadoe          = input("Digite el nuevo estado: ")
    if miDao.actualizar(id_reservacione, fechae, horae, personase, estadoe) is None:
        print("Reservación no encontrada.")
    mostrar_reservaciones(miDao.obtener_todos())

    # --- 5. Eliminar reservación ---
    print("\n=== Eliminar reservación ===")
    id_reservacionel = int(input("Digite el id de la reservación a eliminar: "))
    if not miDao.eliminar(id_reservacionel):
        print("Reservación no encontrada.")
    mostrar_reservaciones(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    run()
