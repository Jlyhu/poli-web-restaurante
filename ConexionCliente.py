from DataAccess import ClienteDAO as c

def main() -> int:
    try:
        c.findAllClientes()

        print("Crear cliente")
        id = input("digite el id ")
        nombre = input("digite el nombre ")
        direccion = input("digite la direccion ")
        telefono = input("digite el telefono ")
        c.crearCliente(id, nombre, direccion, telefono)
        c.findAllClientes()

        print("Editar cliente")
        idC = input("digite el id a actualizar ")
        nombreU = input("digite el nombre actualizado ")
        direccionU = input("digite la direccion actualizada ")
        telefonoU = input("digite el telefono actualizado ")
        c.editarCliente(nombreU, direccionU, telefonoU, idC)
        c.findAllClientes()

        print("Eliminar cliente")
        idD = input("digite el id a eliminar ")
        c.eliminarCliente(idD)
        c.findAllClientes()
        
    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()