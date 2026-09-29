from DataAccess import PedidoMesaDAO as pm

def main() -> int:
    try:
        pm.findAllPedidoMesa()

        print("Crear pedido mesa")
        id = int(input("digite el id del pedido mesa "))
        idMesa = int(input("digite el id de la mesa "))
        idPedido = int(input("digite el id del pedido "))
        pm.crearPedidoMesa(id, idMesa, idPedido)
        pm.findAllPedidoMesa()

        print("Editar pedido mesa")
        idU = int(input("digite el id a actualizar "))
        idMesaU = int(input("digite el id de la mesa actualizada "))
        idPedidoU = int(input("digite el id del pedido actualizado "))
        pm.editarPedidoMesa(idMesaU, idPedidoU, idU)
        pm.findAllPedidoMesa()

        print("Eliminar pedido mesa")
        idD = int(input("digite el id a eliminar "))
        pm.eliminarPedidoMesa(idD)
        pm.findAllPedidoMesa()

    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()