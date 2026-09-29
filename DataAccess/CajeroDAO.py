from DataAccess.conexion import getConnection, unconnection


def findAllCajeros():
    conn = getConnection()
    c = conn.cursor()

    cajeros = """SELECT * FROM Cajero"""

    c.execute(cajeros)

    cajerosData = c.fetchall()

    for cj in cajerosData:
        print(cj)

    unconnection(conn)
    return cajerosData


def buscarCajeroPorId(id_cajero):
    conn = getConnection()
    c = conn.cursor()

    cajeroSelect = """SELECT * FROM Cajero WHERE id_cajero = %s"""
    val = (id_cajero,)

    c.execute(cajeroSelect, val)

    cajeroData = c.fetchone()
    print(cajeroData)

    unconnection(conn)
    return cajeroData


def crearCajero(id_cajero, Usuario_idUsuario):
    conn = getConnection()
    c = conn.cursor()

    cajeroInsert = """INSERT INTO Cajero
    (id_cajero, Usuario_idUsuario)
    VALUES (%s, %s)"""
    val = (id_cajero, Usuario_idUsuario)

    c.execute(cajeroInsert, val)
    conn.commit()

    print(c.rowcount, "cajero insertado.")

    unconnection(conn)


def editarCajero(Usuario_idUsuario, id_cajero):
    conn = getConnection()
    c = conn.cursor()

    cajeroUpdate = """UPDATE Cajero SET
    Usuario_idUsuario = %s
    WHERE id_cajero = %s"""
    val = (Usuario_idUsuario, id_cajero)

    c.execute(cajeroUpdate, val)
    conn.commit()

    print(c.rowcount, "cajero actualizado.")

    unconnection(conn)


def eliminarCajero(id_cajero):
    conn = getConnection()
    c = conn.cursor()

    cajeroDelete = """DELETE FROM Cajero WHERE id_cajero = %s"""
    val = (id_cajero,)

    c.execute(cajeroDelete, val)
    conn.commit()

    print(c.rowcount, "cajero eliminado.")

    unconnection(conn)
