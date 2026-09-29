from DataAccess import CocineroDAO as co

def main() -> int:
    try:
        co.findAllCocineros()

        print("Crear cocinero")
        id = int(input("digite el id del cocinero "))
        estacion = input("digite la estacion ")
        idUsuario = int(input("digite el id del usuario "))
        co.crearCocinero(id, estacion, idUsuario)
        co.findAllCocineros()

        print("Editar cocinero")
        idU = int(input("digite el id a actualizar "))
        estacionU = input("digite la estacion actualizada ")
        idUsuarioU = int(input("digite el id de usuario actualizado "))
        co.editarCocinero(estacionU, idUsuarioU, idU)
        co.findAllCocineros()

        print("Eliminar cocinero")
        idD = int(input("digite el id a eliminar "))
        co.eliminarCocinero(idD)
        co.findAllCocineros()

    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()
    