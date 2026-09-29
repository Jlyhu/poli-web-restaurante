from DataAccess.conexion import getConnection, unconnection

def findAllDetallePedido():
    conn = getConnection()
    c = conn.cursor()

    c.execute("SELECT * FROM DetallePedido")
    for d in c.fetchall():
        print(d)

    unconnection(conn)

def crearDetallePedido(id_detalle, cantidad, notas, id_pedido, id_producto):
    conn = getConnection()
    c = conn.cursor()

    sql = """INSERT INTO DetallePedido
    (id_detalle_pedido, cantidad, notas, Pedido_id_pedido, Producto_idProducto)
    VALUES (%s, %s, %s, %s, %s)"""
    val = (id_detalle, cantidad, notas, id_pedido, id_producto)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "detalle de pedido insertado.")

    unconnection(conn)

def editarDetallePedido(cantidad, notas, id_pedido, id_producto, id_detalle):
    conn = getConnection()
    c = conn.cursor()

    sql = """UPDATE DetallePedido SET
    cantidad = %s,
    notas = %s,
    Pedido_id_pedido = %s,
    Producto_idProducto = %s
    WHERE id_detalle_pedido = %s"""
    val = (cantidad, notas, id_pedido, id_producto, id_detalle)

    c.execute(sql, val)
    conn.commit()
    print(c.rowcount, "detalle de pedido actualizado.")

    unconnection(conn)

def eliminarDetallePedido(id_detalle):
    conn = getConnection()
    c = conn.cursor()

    sql = "DELETE FROM DetallePedido WHERE id_detalle_pedido = %s"
    c.execute(sql, (id_detalle,))
    conn.commit()
    print(c.rowcount, "detalle de pedido eliminado.")

    unconnection(conn)
    