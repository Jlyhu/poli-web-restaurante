from DataAccess.conexion import getConnection, unconnection


def findAllPedidos():
    conn = getConnection()
    c = conn.cursor()

    pedidos = """SELECT * FROM Pedido"""

    c.execute(pedidos)

    pedidosData = c.fetchall()

    for p in pedidosData:
        print(p)

    unconnection(conn)
    return pedidosData


def buscarPedidoPorId(id_pedido):
    conn = getConnection()
    c = conn.cursor()

    pedidoSelect = """SELECT * FROM Pedido WHERE id_pedido = %s"""
    val = (id_pedido,)

    c.execute(pedidoSelect, val)

    pedidoData = c.fetchone()
    print(pedidoData)

    unconnection(conn)
    return pedidoData


def crearPedido(id_pedido, tipo_pedido, Mesero_id_mesero=None,
                Repartidor_id_repartidor=None, Cliente_id_cliente=None,
                estado="PENDIENTE"):
    """Las fechas de creacion y ultima actualizacion las pone la base de datos (NOW())."""
    conn = getConnection()
    c = conn.cursor()

    pedidoInsert = """INSERT INTO Pedido
    (id_pedido, estado, fecha_creacion, fecha_ultima_actualizacion, tipo_pedido,
     Mesero_id_mesero, Repartidor_id_repartidor, Cliente_id_cliente)
    VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s)"""
    val = (id_pedido, estado, tipo_pedido, Mesero_id_mesero,
           Repartidor_id_repartidor, Cliente_id_cliente)

    c.execute(pedidoInsert, val)
    conn.commit()

    print(c.rowcount, "pedido insertado.")

    unconnection(conn)


def editarPedido(tipo_pedido, Mesero_id_mesero, Repartidor_id_repartidor,
                 Cliente_id_cliente, id_pedido):
    conn = getConnection()
    c = conn.cursor()

    pedidoUpdate = """UPDATE Pedido SET
    tipo_pedido = %s,
    Mesero_id_mesero = %s,
    Repartidor_id_repartidor = %s,
    Cliente_id_cliente = %s,
    fecha_ultima_actualizacion = NOW()
    WHERE id_pedido = %s"""
    val = (tipo_pedido, Mesero_id_mesero, Repartidor_id_repartidor,
           Cliente_id_cliente, id_pedido)

    c.execute(pedidoUpdate, val)
    conn.commit()

    print(c.rowcount, "pedido actualizado.")

    unconnection(conn)


def actualizarEstadoPedido(estado, id_pedido):
    """Solo cambia el estado. Las reglas del flujo (que estados se permiten)
    van en el Manager, no aqui."""
    conn = getConnection()
    c = conn.cursor()

    pedidoEstado = """UPDATE Pedido SET
    estado = %s,
    fecha_ultima_actualizacion = NOW()
    WHERE id_pedido = %s"""
    val = (estado, id_pedido)

    c.execute(pedidoEstado, val)
    conn.commit()

    print(c.rowcount, "estado del pedido actualizado.")

    unconnection(conn)


def eliminarPedido(id_pedido):
    conn = getConnection()
    c = conn.cursor()

    pedidoDelete = """DELETE FROM Pedido WHERE id_pedido = %s"""
    val = (id_pedido,)

    c.execute(pedidoDelete, val)
    conn.commit()

    print(c.rowcount, "pedido eliminado.")

    unconnection(conn)
