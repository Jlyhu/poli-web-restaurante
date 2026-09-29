from DataAccess import MesaDAO as m

def main() -> int:
    try:
        m.findAllMesas()

        print("Crear mesa")
        id = input("digite el id ")
        nombre = input("digite el numero de la mesa ")
        credenciales = input("digite el estado de la mesa ")
        m.crearMesa(id, nombre, credenciales)
        m.findAllMesas()

        print("Editar mesa")
        idU = input("digite el id a actualizar ")
        nombreU = input("digite el numero de la mesa actualizado ")
        credencialesU = input("digite el estado de la mesa actualizado ")
        m.editarMesa(nombreU, credencialesU, idU)
        m.findAllMesas()

        print("Eliminar mesa")
        idD = input("digite el id a eliminar ")
        m.eliminarMesa(idD)
        m.findAllMesas()

        
    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()