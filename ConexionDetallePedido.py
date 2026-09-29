from DataAccess import DetallePedidoDAO as dp

def main() -> int:
    try:
        dp.findAllDetallePedido()

        print("Crear detalle de pedido")
        id = int(input("digite el id del detalle "))
        cantidad = int(input("digite la cantidad "))
        notas = input("digite las notas ")
        idPedido = int(input("digite el id del pedido "))
        idProducto = int(input("digite el id del producto "))
        dp.crearDetallePedido(id, cantidad, notas, idPedido, idProducto)
        dp.findAllDetallePedido()

        print("Editar detalle de pedido")
        idU = int(input("digite el id a actualizar "))
        cantidadU = int(input("digite la cantidad actualizada "))
        notasU = input("digite las notas actualizadas ")
        idPedidoU = int(input("digite el id del pedido actualizado "))
        idProductoU = int(input("digite el id del producto actualizado "))
        dp.editarDetallePedido(cantidadU, notasU, idPedidoU, idProductoU, idU)
        dp.findAllDetallePedido()

        print("Eliminar detalle de pedido")
        idD = int(input("digite el id a eliminar "))
        dp.eliminarDetallePedido(idD)
        dp.findAllDetallePedido()

    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()
    