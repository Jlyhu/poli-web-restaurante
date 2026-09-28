from DataAccess.conexion import getConnection, unconnection

def findAllReservaciones():
    conn = getConnection()
    c = conn.cursor()

    reservaciones = """SELECT * FROM Reservacion"""

    c.execute(reservaciones)

    reservacionesData = c.fetchall()

    for r in reservacionesData:
        print(r)

    unconnection(conn)

def crearReservacion(id, fecha, hora, numero_personas, estado, id_cliente):
    conn = getConnection()
    c = conn.cursor()

    mesaInsert = """INSERT INTO Reservacion (id_reservacion, fecha, hora, numero_personas, estado, Cliente_id_cliente) 
    VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (id, fecha, hora, numero_personas, estado, id_cliente)

    c.execute(mesaInsert, val)
    conn.commit()
    print(c.rowcount, "reservación insertada.")

    unconnection(conn)
#crearReservacion(1, "2023-01-01", "12:00:00", 2, "Confirmada", 1)

def editarReservacion(fecha, hora, numero_personas, estado, id):
    conn = getConnection()
    c = conn.cursor()

    reservacionUpdate = """UPDATE Reservacion SET 
    fecha = %s, 
    hora = %s, 
    numero_personas = %s, 
    estado = %s 
    WHERE id_reservacion = %s"""
    val = (fecha, hora, numero_personas, estado, id)

    c.execute(reservacionUpdate, val)
    conn.commit()
    print(c.rowcount, "reservación actualizada.")

    unconnection(conn)
#editarReservacion("2023-01-02", "13:00:00", 3, "Confirmada", 1)

def eliminarReservacion(id):
    conn = getConnection()
    c = conn.cursor()

    reservacionDelete = """DELETE FROM Reservacion WHERE id_reservacion = %s"""
    val = (id,)

    c.execute(reservacionDelete, val)
    conn.commit()
    print(c.rowcount, "reservación eliminada.")

    unconnection(conn)
#eliminarReservacion(1)
#findAllReservaciones()