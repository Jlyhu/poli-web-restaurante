from DataAccess.conexion import getConnection, unconnection


def findAllMeseros():
    conn = getConnection()
    c = conn.cursor()

    meseros = """SELECT * FROM Mesero"""

    c.execute(meseros)

    meserosData = c.fetchall()

    for m in meserosData:
        print(m)

    unconnection(conn)
    return meserosData


def buscarMeseroPorId(id_mesero):
    conn = getConnection()
    c = conn.cursor()

    meseroSelect = """SELECT * FROM Mesero WHERE id_mesero = %s"""
    val = (id_mesero,)

    c.execute(meseroSelect, val)

    meseroData = c.fetchone()
    print(meseroData)

    unconnection(conn)
    return meseroData


def crearMesero(id_mesero, zona_asignada, Usuario_idUsuario):
    conn = getConnection()
    c = conn.cursor()

    meseroInsert = """INSERT INTO Mesero
    (id_mesero, zona_asignada, Usuario_idUsuario)
    VALUES (%s, %s, %s)"""
    val = (id_mesero, zona_asignada, Usuario_idUsuario)

    c.execute(meseroInsert, val)
    conn.commit()

    print(c.rowcount, "mesero insertado.")

    unconnection(conn)


def editarMesero(zona_asignada, Usuario_idUsuario, id_mesero):
    conn = getConnection()
    c = conn.cursor()

    meseroUpdate = """UPDATE Mesero SET
    zona_asignada = %s,
    Usuario_idUsuario = %s
    WHERE id_mesero = %s"""
    val = (zona_asignada, Usuario_idUsuario, id_mesero)

    c.execute(meseroUpdate, val)
    conn.commit()

    print(c.rowcount, "mesero actualizado.")

    unconnection(conn)


def eliminarMesero(id_mesero):
    conn = getConnection()
    c = conn.cursor()

    meseroDelete = """DELETE FROM Mesero WHERE id_mesero = %s"""
    val = (id_mesero,)

    c.execute(meseroDelete, val)
    conn.commit()

    print(c.rowcount, "mesero eliminado.")

    unconnection(conn)
