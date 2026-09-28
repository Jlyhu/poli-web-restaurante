from DataAccess.conexion import getConnection, unconnection
# `id_reservacion_mesa` INT NOT NULL,  `Mesa_id_mesa` INT NOT NULL,  `Reservacion_id_reservacion` INT NOT NULL,
def findAllReservacionesMesa():
    conn = getConnection()
    c = conn.cursor()

    reservaciones = """SELECT * FROM ReservacionMesa"""

    c.execute(reservaciones)

    reservacionesData = c.fetchall()

    for r in reservacionesData:
        print(r)

    unconnection(conn)

def crearReservacionMesa(id, id_mesa, id_reservacion):
    conn = getConnection()
    c = conn.cursor()

    reservacionInsert = """INSERT INTO ReservacionMesa (id_reservacion_mesa, Mesa_id_mesa, Reservacion_id_reservacion) 
    VALUES (%s, %s, %s)"""
    val = (id, id_mesa, id_reservacion)

    c.execute(reservacionInsert, val)
    conn.commit()
    print(c.rowcount, "reservación de mesa insertada.")

    unconnection(conn)
#para crear una reservación de mesa, se debe tener una mesa y una reservación creadas previamente
#crearReservacionMesa(1, 1, 1)

def editarReservacionMesa(id_mesa, id_reservacion, id):
    conn = getConnection()
    c = conn.cursor()

    reservacionUpdate = """UPDATE ReservacionMesa SET 
    Mesa_id_mesa = %s, 
    Reservacion_id_reservacion = %s 
    WHERE id_reservacion_mesa = %s"""
    val = (id_mesa, id_reservacion, id)

    c.execute(reservacionUpdate, val)
    conn.commit()
    print(c.rowcount, "reservación de mesa actualizada.")

    unconnection(conn)
#editarReservacionMesa(2, 1, 1)

def eliminarReservacionMesa(id):
    conn = getConnection()
    c = conn.cursor()

    reservacionDelete = """DELETE FROM ReservacionMesa WHERE id_reservacion_mesa = %s"""
    val = (id,)

    c.execute(reservacionDelete, val)
    conn.commit()
    print(c.rowcount, "reservación de mesa eliminada.")

    unconnection(conn)
#eliminarReservacionMesa(1)
#findAllReservacionesMesa()