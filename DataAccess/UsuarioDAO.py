from DataAccess.conexion import getConnection, unconnection

def findAllUsuarios():
    conn = getConnection()
    c = conn.cursor()

    usuarios = """SELECT * FROM Usuario"""

    c.execute(usuarios)

    usuariosData = c.fetchall()

    for u in usuariosData:
        print(u)

    unconnection(conn)

def crearUsuario(id, nombre, credenciales):
    conn = getConnection()
    c = conn.cursor()

    usuarioInsert = """INSERT INTO Usuario (idUsuario, nombre, credenciales) 
    VALUES (%s, %s, %s)"""
    val = (id, nombre, credenciales)

    c.execute(usuarioInsert, val)
    conn.commit()
    print(c.rowcount, "usuario insertado.")

    unconnection(conn)
#crearUsuario(1, "Usuario Prueba 1", "prueba:1234")
def editarUsuario(nombre, credenciales, id):
    conn = getConnection()
    c = conn.cursor()

    usuarioUpdate = """UPDATE Usuario SET 
    nombre = %s, 
    credenciales = %s 
    WHERE idUsuario = %s"""
    val = (nombre, credenciales, id)

    c.execute(usuarioUpdate, val)
    conn.commit()
    print(c.rowcount, "usuario actualizado.")

    unconnection(conn)
#editarUsuario("Usuario Prueba 1 Editado", "nueva_clave:9999", 1)

def desactivarUsuario(id):
    conn = getConnection()
    c = conn.cursor()

    usuarioDesactivar = """UPDATE Usuario SET estado = 'inactivo' WHERE idUsuario = %s"""
    val = (id,)

    c.execute(usuarioDesactivar, val)
    conn.commit()
    print(c.rowcount, "usuario desactivado.")

    unconnection(conn)
#desactivarUsuario(1)
def activarUsuario(id):
    conn = getConnection()
    c = conn.cursor()

    usuarioActivar = """UPDATE Usuario SET estado = 'activo' WHERE idUsuario = %s"""
    val = (id,)

    c.execute(usuarioActivar, val)
    conn.commit()
    print(c.rowcount, "usuario activado.")

    unconnection(conn)
#findAllUsuarios()