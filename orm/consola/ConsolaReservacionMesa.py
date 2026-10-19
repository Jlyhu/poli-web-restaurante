# ============================================================
# ConsolaReservacionMesa.py
# Punto de entrada de la aplicación
# Gestiona la interacción con el usuario y consume ReservacionMesaDAO
# para realizar operaciones CRUD sobre la entidad ReservacionMesa
#
# Requiere una mesa y una reservación creadas antes
# (ver ConsolaMesa.py y ConsolaReservacion.py).
# ============================================================

from orm.dao import ReservacionMesaDAO as rmdao
from orm.models import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Crear sesión de base de datos y pasarla al DAO (inyección de dependencias)
session = SessionLocal()
miDao   = rmdao.ReservacionMesaDAO(session)


# ------------------------------------------------------------
# Función: mostrar_personas
# Imprime en consola la lista de personas recibida
#
# Parámetros:
#   personas (list[Persona]) -- Lista de objetos Persona a mostrar
#
# Retorna:
#   None
#
# Ejemplo:
#   personas = miDao.obtener_todos()
#   mostrar_personas(personas)
# ------------------------------------------------------------a
def mostrar_registros(registros):
    if not registros:
        print("No hay registros.")
    else:
        for r in registros:
            print(f"ID: {r.id_reservacion_mesa} | Mesa: {r.Mesa_id_mesa} | Reservación: {r.Reservacion_id_reservacion}")


# ------------------------------------------------------------
# Flujo principal de la aplicación — ejecuta en secuencia:
#   1. Listar  
#   2. Asignar mesa  
#   3. Buscar por reservación  
#   4. Editar  
#   5. Eliminar
#
# Retorna:
#   None
# ------------------------------------------------------------
def run():

    # --- 1. Listar todos los registros ---
    print("=== Ver todos ===")
    mostrar_registros(miDao.obtener_todos())

    # --- 2. Asignar una mesa a una reservación ---
    print("\n=== Asignar mesa a reservación ===")
    id_rm          = int(input("Digite el id del registro: "))
    id_mesa        = int(input("Digite el id de la mesa (debe existir): "))
    id_reservacion = int(input("Digite el id de la reservación (debe existir): "))
    miDao.crear(id_rm, id_mesa, id_reservacion)
    mostrar_registros(miDao.obtener_todos())

    # --- 3. Buscar por reservación ---
    print("\n=== Buscar por reservación ===")
    id_reservacionb = int(input("Digite el id de la reservación: "))
    mostrar_registros(miDao.obtener_por_reservacion(id_reservacionb))

    # --- 4. Editar registro ---
    print("\n=== Editar registro ===")
    id_rme          = int(input("Digite el id del registro a editar: "))
    id_mesae        = int(input("Digite el nuevo id de la mesa: "))
    id_reservacione = int(input("Digite el nuevo id de la reservación: "))
    if miDao.actualizar(id_rme, id_mesae, id_reservacione) is None:
        print("Registro no encontrado.")
    mostrar_registros(miDao.obtener_todos())

    # --- 5. Eliminar registro ---
    print("\n=== Eliminar registro ===")
    id_rmel = int(input("Digite el id del registro a eliminar: "))
    if not miDao.eliminar(id_rmel):
        print("Registro no encontrado.")
    mostrar_registros(miDao.obtener_todos())


# Punto de entrada del programa
if __name__ == '__main__':
    try:
        run()
    except ValueError:
        print("Valores no válidos: todos los ids deben ser números enteros.")
    except SQLAlchemyError as e:
        session.rollback()   # deshace lo que haya quedado a medias
        print("Error en la base de datos:", e.__cause__ or e)
    finally:
        session.close()      # siempre cierra la sesión
