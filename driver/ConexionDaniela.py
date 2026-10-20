"""Prueba de los DAO de Daniela: Categoria, Mesero, Repartidor, Cajero, Caja y Pedido.

Como la base de datos es compartida, usa ids 981-983 (los de prueba de las
demas son otros) y al final borra todo lo que creo, en orden inverso por las
llaves foraneas.

Ejecutar desde la carpeta principal del proyecto:  python -m driver.ConexionDaniela
"""
from driver.DataAccess import UsuarioDAO as u
from driver.DataAccess import CategoriaDAO as cat
from driver.DataAccess import MeseroDAO as me
from driver.DataAccess import RepartidorDAO as re
from driver.DataAccess import CajeroDAO as cj
from driver.DataAccess import CajaDAO as ca
from driver.DataAccess import PedidoDAO as pe
from driver.DataAccess.conexion import getConnection, unconnection


def limpiar():
    """Borra los datos de prueba (si existen), hijos primero."""
    conn = getConnection()
    c = conn.cursor()
    pasos = [
        "DELETE FROM Pedido WHERE id_pedido = 981",
        "DELETE FROM Caja WHERE id_caja = 981",
        "DELETE FROM Cajero WHERE id_cajero = 981",
        "DELETE FROM Mesero WHERE id_mesero = 981",
        "DELETE FROM Repartidor WHERE id_repartidor = 981",
        "DELETE FROM Categoria WHERE id_categoria = 981",
        "DELETE FROM Usuario WHERE idUsuario IN (981, 982, 983)",
    ]
    for sql in pasos:
        try:
            c.execute(sql)
        except Exception as e:
            print("No se pudo limpiar:", sql, "->", e)
    conn.commit()
    unconnection(conn)


def main() -> int:
    try:
        limpiar()  # por si una prueba anterior quedo a medias

        print("=== CATEGORIA ===")
        cat.crearCategoria(981, "Prueba Entradas")
        cat.buscarCategoriaPorId(981)
        cat.editarCategoria("Prueba Entradas Editada", 981)
        cat.buscarCategoriaPorId(981)

        print("\n=== USUARIOS DE PRUEBA (los necesitan Mesero, Repartidor y Cajero) ===")
        u.crearUsuario(981, "Mesero Prueba", "mesero:1")
        u.crearUsuario(982, "Repartidor Prueba", "repartidor:1")
        u.crearUsuario(983, "Cajero Prueba", "cajero:1")

        print("\n=== MESERO ===")
        me.crearMesero(981, "Terraza", 981)
        me.buscarMeseroPorId(981)
        me.editarMesero("Salon principal", 981, 981)
        me.buscarMeseroPorId(981)

        print("\n=== REPARTIDOR ===")
        re.crearRepartidor(981, "ABC123", 982)
        re.buscarRepartidorPorId(981)
        re.editarRepartidor("XYZ789", 982, 981)
        re.buscarRepartidorPorId(981)

        print("\n=== CAJERO ===")
        cj.crearCajero(981, 983)
        cj.buscarCajeroPorId(981)
        cj.editarCajero(983, 981)

        print("\n=== CAJA ===")
        ca.crearCaja(981, 50000, 981)
        ca.buscarCajaPorId(981)
        ca.cerrarCaja(120000, 981)
        ca.buscarCajaPorId(981)

        print("\n=== PEDIDO ===")
        pe.crearPedido(981, "SALON", Mesero_id_mesero=981)
        pe.buscarPedidoPorId(981)
        pe.actualizarEstadoPedido("EN PREPARACION", 981)
        pe.buscarPedidoPorId(981)
        pe.editarPedido("DOMICILIO", 981, 981, None, 981)
        pe.buscarPedidoPorId(981)

        print("\n=== ELIMINAR (en orden inverso) ===")
        pe.eliminarPedido(981)
        ca.eliminarCaja(981)
        cj.eliminarCajero(981)
        re.eliminarRepartidor(981)
        me.eliminarMesero(981)
        cat.eliminarCategoria(981)

    except Exception as e:
        print("Error:", e)
    finally:
        limpiar()  # deja la base compartida como estaba
        print("\nDatos de prueba eliminados.")


if __name__ == "__main__":
    main()
