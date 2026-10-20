from DataAccess.conexion import getConnection, unconnection


def findAllAdministradores():
    conn = getConnection()
    c = conn.cursor()

    administradores = """SELECT * FROM Administrador"""

    c.execute(administradores)

    administradoresData = c.fetchall()

    for a in administradoresData:
        print(a)

    unconnection(conn)


def crearAdministrador(id_administrador, Usuario_idUsuario):
    conn = getConnection()
    c = conn.cursor()

    administradorInsert = """INSERT INTO Administrador
    (id_administrador, Usuario_idUsuario)
    VALUES (%s, %s)"""

    val = (id_administrador, Usuario_idUsuario)

    c.execute(administradorInsert, val)
    conn.commit()

    print(c.rowcount, "administrador insertado.")

    unconnection(conn)


def editarAdministrador(Usuario_idUsuario, id_administrador):
    conn = getConnection()
    c = conn.cursor()

    administradorUpdate = """UPDATE Administrador SET
    Usuario_idUsuario = %s
    WHERE id_administrador = %s"""

    val = (Usuario_idUsuario, id_administrador)

    c.execute(administradorUpdate, val)
    conn.commit()

    print(c.rowcount, "administrador actualizado.")

    unconnection(conn)


def eliminarAdministrador(id_administrador):
    conn = getConnection()
    c = conn.cursor()

    administradorDelete = """DELETE FROM Administrador
    WHERE id_administrador = %s"""

    val = (id_administrador,)

    c.execute(administradorDelete, val)
    conn.commit()

    print(c.rowcount, "administrador eliminado.")

    unconnection(conn)