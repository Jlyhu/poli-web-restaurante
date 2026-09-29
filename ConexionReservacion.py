from DataAccess import ReservacionDAO as r
# Acepta dd/mm/aaaa o dd/mm/aaaa HH:MM
def main() -> int:
    try:
        r.findAllReservaciones()

        print("Crear reservacion")
        id = input("digite el id ")
        fecha = input("digite la fecha ")
        hora = input("digite la hora ")
        numero_personas = input("digite el numero de personas ")
        estado = input("digite el estado ")
        Cliente_id_cliente = input("digite el id del cliente ")
        r.crearReservacion(id, fecha, hora, numero_personas, estado, Cliente_id_cliente)
        r.findAllReservaciones()

        print("Editar reservacion")
        idU = input("digite el id a actualizar ")
        fechaU = input("digite la fecha actualizada ")
        horaU = input("digite la hora actualizada ")
        numero_personasU = input("digite el numero de personas actualizado ")
        estadoU = input("digite el estado actualizado ")
        Cliente_id_clienteU = input("digite el id del cliente actualizado ")
        r.editarReservacion(fechaU, horaU, numero_personasU, estadoU, Cliente_id_clienteU, idU)
        r.findAllReservaciones()

        print("Eliminar reservacion")
        idD = input("digite el id a eliminar ")
        r.eliminarReservacion(idD)
        r.findAllReservaciones()
        
    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()