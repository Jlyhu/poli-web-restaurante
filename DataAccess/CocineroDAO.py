from DataAccess.conexion import getConnection, unconnection

def findAllCocineros():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT * FROM Cocinero")
    for co in c.fetchall():
        print(co)

    unconnection(conn)

def crearCocinero(id_cocinero, estacion, id_usuario):
    conn = getConnection()
    c = conn.cursor()

    sql = """INSERT INTO Cocinero (id_cocinero, estacion, Usuario_id_usuario)
    VALUES (%s, %s, %s)"""
    val = (id_cocinero, estacion, id_usuario)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "cocinero insertado.")

    unconnection(conn)

def editarCocinero(estacion, id_usuario, id_cocinero):
    conn = getConnection()
    c = conn.cursor()

    sql = """UPDATE Cocinero SET
    estacion = %s,
    Usuario_id_usuario = %s
    WHERE id_cocinero = %s"""
    val = (estacion, id_usuario, id_cocinero)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "cocinero actualizado.")

    unconnection(conn)

def eliminarCocinero(id_cocinero):
    conn = getConnection()
    c = conn.cursor()

    sql = "DELETE FROM Cocinero WHERE id_cocinero = %s"
    c.execute(sql, (id_cocinero,))
    conn.commit()
    print(c.rowcount, "cocinero eliminado.")

    unconnection(conn)
    