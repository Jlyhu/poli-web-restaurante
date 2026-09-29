from DataAccess.conexion import getConnection, unconnection

def findAllClientes():
    conn = getConnection()
    c = conn.cursor()

    clientes = """SELECT * FROM Cliente"""

    c.execute(clientes)

    clientesData = c.fetchall()

    for c in clientesData:
        print(c)

    unconnection(conn)

def crearCliente(id, nombre, direccion, telefono):
    conn = getConnection()
    c = conn.cursor()

    clienteInsert = """INSERT INTO Cliente (id_cliente, nombre, direccion, telefono) 
    VALUES (%s, %s, %s, %s)"""
    val = (id, nombre, direccion, telefono)

    c.execute(clienteInsert, val)
    conn.commit()
    print(c.rowcount, "cliente insertado.")

    unconnection(conn)
#crearCliente(1, "Cliente Prueba 1", "calle ejemplo", "123456789")

def editarCliente(nombre, direccion, telefono, id):
    conn = getConnection()
    c = conn.cursor()

    clienteUpdate = """UPDATE Cliente SET 
    nombre = %s, 
    direccion = %s, 
    telefono = %s 
    WHERE id_cliente = %s"""
    val = (nombre, direccion, telefono, id)

    c.execute(clienteUpdate, val)
    conn.commit()
    print(c.rowcount, "cliente actualizado.")

    unconnection(conn)
#editarCliente("Cliente Prueba 1 Editado", "calle editada", "987654321", 1)

def eliminarCliente(id):
    conn = getConnection()
    c = conn.cursor()

    clienteDelete = """DELETE FROM Cliente WHERE id_cliente = %s"""
    val = (id,)

    c.execute(clienteDelete, val)
    conn.commit()
    print(c.rowcount, "cliente eliminado.")

    unconnection(conn)
#eliminarCliente(1)
#findAllClientes()