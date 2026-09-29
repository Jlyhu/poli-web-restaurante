from DataAccess.conexion import getConnection, unconnection


def findAllRepartidores():
    conn = getConnection()
    c = conn.cursor()

    repartidores = """SELECT * FROM Repartidor"""

    c.execute(repartidores)

    repartidoresData = c.fetchall()

    for r in repartidoresData:
        print(r)

    unconnection(conn)
    return repartidoresData


def buscarRepartidorPorId(id_repartidor):
    conn = getConnection()
    c = conn.cursor()

    repartidorSelect = """SELECT * FROM Repartidor WHERE id_repartidor = %s"""
    val = (id_repartidor,)

    c.execute(repartidorSelect, val)

    repartidorData = c.fetchone()
    print(repartidorData)

    unconnection(conn)
    return repartidorData


def crearRepartidor(id_repartidor, placa_vehiculo, Usuario_idUsuario):
    conn = getConnection()
    c = conn.cursor()

    repartidorInsert = """INSERT INTO Repartidor
    (id_repartidor, placa_vehiculo, Usuario_idUsuario)
    VALUES (%s, %s, %s)"""
    val = (id_repartidor, placa_vehiculo, Usuario_idUsuario)

    c.execute(repartidorInsert, val)
    conn.commit()

    print(c.rowcount, "repartidor insertado.")

    unconnection(conn)


def editarRepartidor(placa_vehiculo, Usuario_idUsuario, id_repartidor):
    conn = getConnection()
    c = conn.cursor()

    repartidorUpdate = """UPDATE Repartidor SET
    placa_vehiculo = %s,
    Usuario_idUsuario = %s
    WHERE id_repartidor = %s"""
    val = (placa_vehiculo, Usuario_idUsuario, id_repartidor)

    c.execute(repartidorUpdate, val)
    conn.commit()

    print(c.rowcount, "repartidor actualizado.")

    unconnection(conn)


def eliminarRepartidor(id_repartidor):
    conn = getConnection()
    c = conn.cursor()

    repartidorDelete = """DELETE FROM Repartidor WHERE id_repartidor = %s"""
    val = (id_repartidor,)

    c.execute(repartidorDelete, val)
    conn.commit()

    print(c.rowcount, "repartidor eliminado.")

    unconnection(conn)
