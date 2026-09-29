from DataAccess.conexion import getConnection, unconnection

def findAllProductos():
    conn = getConnection()
    c = conn.cursor()

    productos = """SELECT * FROM Producto"""

    c.execute(productos)

    productosData = c.fetchall()

    for p in productosData:
        print(p)

    unconnection(conn)

def crearProducto(id, nombre, descripcion, precio, cantidad_disponible, id_categoria):
    conn = getConnection()
    c = conn.cursor()

    productoInsert = """INSERT INTO Producto (id_producto, nombre, descripcion, precio, cantidad_disponible, Categoria_id_categoria) 
    VALUES (%s, %s, %s, %s, %s, %s)"""
    val = (id, nombre, descripcion, precio, cantidad_disponible, id_categoria)

    c.execute(productoInsert, val)
    conn.commit()
    print(c.rowcount, "producto insertado.")

    unconnection(conn)

    c.execute(productoInsert, val)
    conn.commit()
    print(c.rowcount, "producto insertado.")

    unconnection(conn)
#se necesita tener una categoria creada para poder crear un producto
#crearProducto(1, "Producto Prueba 1", "descripcion ejemplo", 10.99, 100, 1)

def editarProducto(nombre, descripcion, precio, cantidad_disponible, id_categoria, id):
    conn = getConnection()
    c = conn.cursor()

    productoUpdate = """UPDATE Producto SET 
    nombre = %s, 
    descripcion = %s, 
    precio = %s, 
    cantidad_disponible = %s, 
    Categoria_id_categoria = %s 
    WHERE id_producto = %s"""
    val = (nombre, descripcion, precio, cantidad_disponible, id_categoria, id)

    c.execute(productoUpdate, val)
    conn.commit()
    print(c.rowcount, "producto actualizado.")

    unconnection(conn)
#editarProducto("Producto Prueba 1 Editado", "descripcion editada", 15.99, 50, 1, 1)

def eliminarProducto(id):
    conn = getConnection()
    c = conn.cursor()

    productoDelete = """DELETE FROM Producto WHERE id_producto = %s"""
    val = (id,)

    c.execute(productoDelete, val)
    conn.commit()
    print(c.rowcount, "producto eliminado.")

    unconnection(conn)
#eliminarProducto(1)
#findAllProductos()