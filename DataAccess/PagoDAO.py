from DataAccess.conexion import getConnection, unconnection

def findAllPagos():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT * FROM Pago")
    for p in c.fetchall():
        print(p)

    unconnection(conn)

def crearPago(id_pago, monto, metodo_pago, fecha_pago, id_pedido, id_caja):
    conn = getConnection()
    c = conn.cursor()

    sql = """INSERT INTO Pago
    (id_pago, monto, metodo_pago, fecha_pago, Pedido_id_pedido, Caja_id_caja)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (id_pago, monto, metodo_pago, fecha_pago, id_pedido, id_caja)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "pago insertado.")

    unconnection(conn)

def editarPago(monto, metodo_pago, fecha_pago, id_pedido, id_caja, id_pago):
    conn = getConnection()
    c = conn.cursor()

    sql = """UPDATE Pago SET
    monto = %s,
    metodo_pago = %s,
    fecha_pago = %s,
    Pedido_id_pedido = %s,
    Caja_id_caja = %s
    WHERE id_pago = %s"""
    val = (monto, metodo_pago, fecha_pago, id_pedido, id_caja, id_pago)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "pago actualizado.")

    unconnection(conn)

def eliminarPago(id_pago):
    conn = getConnection()
    c = conn.cursor()

    sql = "DELETE FROM Pago WHERE id_pago = %s"
    c.execute(sql, (id_pago,))
    conn.commit()
    print(c.rowcount, "pago eliminado.")

    unconnection(conn)
    