from DataAccess.conexion import getConnection, unconnection

def findAllMesas():
    conn = getConnection()
    c = conn.cursor()

    mesas = """SELECT * FROM Mesa"""

    c.execute(mesas)

    mesasData = c.fetchall()

    for m in mesasData:
        print(m)

    unconnection(conn)

def crearMesa(id, numero, estado):
    conn = getConnection()
    c = conn.cursor()

    mesaInsert = """INSERT INTO Mesa (id_mesa, numero, estado) 
    VALUES (%s, %s, %s)"""
    val = (id, numero, estado)

    c.execute(mesaInsert, val)
    conn.commit()
    print(c.rowcount, "mesa insertada.")

    unconnection(conn)
#crearMesa(1, 1, "Disponible")

def editarMesa(numero, estado, id):
    conn = getConnection()
    c = conn.cursor()

    mesaUpdate = """UPDATE Mesa SET 
    numero = %s, 
    estado = %s 
    WHERE id_mesa = %s"""
    val = (numero, estado, id)

    c.execute(mesaUpdate, val)
    conn.commit()
    print(c.rowcount, "mesa actualizada.")

    unconnection(conn)
#editarMesa(1, "Ocupada", 1)

def eliminarMesa(id):
    conn = getConnection()
    c = conn.cursor()

    mesaDelete = """DELETE FROM Mesa WHERE id_mesa = %s"""
    val = (id,)

    c.execute(mesaDelete, val)
    conn.commit()
    print(c.rowcount, "mesa eliminada.")

    unconnection(conn)
#eliminarMesa(1)
#findAllMesas()