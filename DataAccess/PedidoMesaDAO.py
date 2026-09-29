from DataAccess.conexion import getConnection, unconnection

def findAllPedidoMesa():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT * FROM PedidoMesa")
    for p in c.fetchall():
        print(p)

    unconnection(conn)

def crearPedidoMesa(id_pedido_mesa, id_mesa, id_pedido):
    conn = getConnection()
    c = conn.cursor()

    sql = """INSERT INTO PedidoMesa (id_pedido_mesa, Mesa_id_mesa, Pedido_id_pedido)
    VALUES (%s, %s, %s)"""
    val = (id_pedido_mesa, id_mesa, id_pedido)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "pedido mesa insertado.")

    unconnection(conn)

def editarPedidoMesa(id_mesa, id_pedido, id_pedido_mesa):
    conn = getConnection()
    c = conn.cursor()

    sql = """UPDATE PedidoMesa SET
    Mesa_id_mesa = %s,
    Pedido_id_pedido = %s
    WHERE id_pedido_mesa = %s"""
    val = (id_mesa, id_pedido, id_pedido_mesa)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "pedido mesa actualizado.")

    unconnection(conn)

def eliminarPedidoMesa(id_pedido_mesa):
    conn = getConnection()
    c = conn.cursor()

    sql = "DELETE FROM PedidoMesa WHERE id_pedido_mesa = %s"
    c.execute(sql, (id_pedido_mesa,))
    conn.commit()
    print(c.rowcount, "pedido mesa eliminado.")

    unconnection(conn)