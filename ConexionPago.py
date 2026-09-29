from datetime import datetime
from DataAccess import PagoDAO as pa

def main() -> int:
    try:
        pa.findAllPagos()

        print("Crear pago")
        id = int(input("digite el id del pago "))
        monto = float(input("digite el monto "))
        metodo = input("digite el metodo de pago ")
        idPedido = int(input("digite el id del pedido "))
        idCaja = int(input("digite el id de la caja "))
        pa.crearPago(id, monto, metodo, datetime.now(), idPedido, idCaja)
        pa.findAllPagos()

        print("Editar pago")
        idU = int(input("digite el id a actualizar "))
        montoU = float(input("digite el monto actualizado "))
        metodoU = input("digite el metodo actualizado ")
        idPedidoU = int(input("digite el id del pedido actualizado "))
        idCajaU = int(input("digite el id de la caja actualizada "))
        pa.editarPago(montoU, metodoU, datetime.now(), idPedidoU, idCajaU, idU)
        pa.findAllPagos()

        print("Eliminar pago")
        idD = int(input("digite el id a eliminar "))
        pa.eliminarPago(idD)
        pa.findAllPagos()

    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()
    