from DataAccess.conexion import getConnection, unconnection


def findAllCategorias():
    conn = getConnection()
    c = conn.cursor()

    categorias = """SELECT * FROM Categoria"""

    c.execute(categorias)

    categoriasData = c.fetchall()

    for cat in categoriasData:
        print(cat)

    unconnection(conn)
    return categoriasData


def buscarCategoriaPorId(id_categoria):
    conn = getConnection()
    c = conn.cursor()

    categoriaSelect = """SELECT * FROM Categoria WHERE id_categoria = %s"""
    val = (id_categoria,)

    c.execute(categoriaSelect, val)

    categoriaData = c.fetchone()
    print(categoriaData)

    unconnection(conn)
    return categoriaData


def crearCategoria(id_categoria, nombre):
    conn = getConnection()
    c = conn.cursor()

    categoriaInsert = """INSERT INTO Categoria (id_categoria, nombre)
    VALUES (%s, %s)"""
    val = (id_categoria, nombre)

    c.execute(categoriaInsert, val)
    conn.commit()

    print(c.rowcount, "categoria insertada.")

    unconnection(conn)


def editarCategoria(nombre, id_categoria):
    conn = getConnection()
    c = conn.cursor()

    categoriaUpdate = """UPDATE Categoria SET
    nombre = %s
    WHERE id_categoria = %s"""
    val = (nombre, id_categoria)

    c.execute(categoriaUpdate, val)
    conn.commit()

    print(c.rowcount, "categoria actualizada.")

    unconnection(conn)


def eliminarCategoria(id_categoria):
    conn = getConnection()
    c = conn.cursor()

    categoriaDelete = """DELETE FROM Categoria WHERE id_categoria = %s"""
    val = (id_categoria,)

    c.execute(categoriaDelete, val)
    conn.commit()

    print(c.rowcount, "categoria eliminada.")

    unconnection(conn)
