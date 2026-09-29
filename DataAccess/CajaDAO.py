from DataAccess.conexion import getConnection, unconnection


def findAllCajas():
    conn = getConnection()
    c = conn.cursor()

    cajas = """SELECT * FROM Caja"""

    c.execute(cajas)

    cajasData = c.fetchall()

    for ca in cajasData:
        print(ca)

    unconnection(conn)
    return cajasData


def buscarCajaPorId(id_caja):
    conn = getConnection()
    c = conn.cursor()

    cajaSelect = """SELECT * FROM Caja WHERE id_caja = %s"""
    val = (id_caja,)

    c.execute(cajaSelect, val)

    cajaData = c.fetchone()
    print(cajaData)

    unconnection(conn)
    return cajaData


def crearCaja(id_caja, monto_inicial, Cajero_id_cajero):
    """Abre una caja: la fecha de apertura la pone la base de datos (NOW())."""
    conn = getConnection()
    c = conn.cursor()

    cajaInsert = """INSERT INTO Caja
    (id_caja, fecha_apertura, monto_inicial, Cajero_id_cajero)
    VALUES (%s, NOW(), %s, %s)"""
    val = (id_caja, monto_inicial, Cajero_id_cajero)

    c.execute(cajaInsert, val)
    conn.commit()

    print(c.rowcount, "caja insertada.")

    unconnection(conn)


def cerrarCaja(monto_final, id_caja):
    """Cierra una caja: guarda el monto final y la fecha de cierre (NOW())."""
    conn = getConnection()
    c = conn.cursor()

    cajaCerrar = """UPDATE Caja SET
    fecha_cierre = NOW(),
    monto_final = %s
    WHERE id_caja = %s"""
    val = (monto_final, id_caja)

    c.execute(cajaCerrar, val)
    conn.commit()

    print(c.rowcount, "caja cerrada.")

    unconnection(conn)


def editarCaja(monto_inicial, monto_final, Cajero_id_cajero, id_caja):
    conn = getConnection()
    c = conn.cursor()

    cajaUpdate = """UPDATE Caja SET
    monto_inicial = %s,
    monto_final = %s,
    Cajero_id_cajero = %s
    WHERE id_caja = %s"""
    val = (monto_inicial, monto_final, Cajero_id_cajero, id_caja)

    c.execute(cajaUpdate, val)
    conn.commit()

    print(c.rowcount, "caja actualizada.")

    unconnection(conn)


def eliminarCaja(id_caja):
    conn = getConnection()
    c = conn.cursor()

    cajaDelete = """DELETE FROM Caja WHERE id_caja = %s"""
    val = (id_caja,)

    c.execute(cajaDelete, val)
    conn.commit()

    print(c.rowcount, "caja eliminada.")

    unconnection(conn)
