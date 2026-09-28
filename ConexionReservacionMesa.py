from DataAccess import ReservacionMesaDAO as rm

def main() -> int:
    try:
        rm.findAllReservacionesMesa()

        print("Crear reservacion de mesa")
        id = input("digite el id ")
        Mesa_id_mesa = input("digite el id de la mesa ")
        Reservacion_id_reservacion = input("digite el id de la reservacion ")
        rm.crearReservacionMesa(id, Mesa_id_mesa, Reservacion_id_reservacion)
        rm.findAllReservacionesMesa()

        print("Editar reservacion de mesa")
        idU = input("digite el id a actualizar ")
        Mesa_id_mesaU = input("digite el id de la mesa actualizado ")
        Reservacion_id_reservacionU = input("digite el id de la reservacion actualizado ")
        rm.editarReservacionMesa(Mesa_id_mesaU, Reservacion_id_reservacionU, idU)
        rm.findAllReservacionesMesa()

        print("Eliminar reservacion de mesa")
        idD = input("digite el id a eliminar ")
        rm.eliminarReservacionMesa(idD)
        rm.findAllReservacionesMesa()

    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()