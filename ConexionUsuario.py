from DataAccess import UsuarioDAO as u

def main() -> int:
    try:
        u.findAllUsuarios()

        print("Crear usuario")
        id = input("digite el id ")
        nombre = input("digite el nombre ")
        credenciales = input("digite las credenciales ")
        u.crearUsuario(id, nombre, credenciales)
        u.findAllUsuarios()

        print("Editar usuario")
        idU = input("digite el id a actualizar ")
        nombreU = input("digite el nombre actualizado ")
        credencialesU = input("digite las credenciales actualizadas ")
        u.editarUsuario(nombreU, credencialesU, idU)
        u.findAllUsuarios()

        print("Desactivar usuario")
        idD = input("digite el id a desactivar ")
        u.desactivarUsuario(idD)
        u.findAllUsuarios()

        print("Activar usuario")
        idA = input("digite el id a activar ")
        u.activarUsuario(idA)
        u.findAllUsuarios()
        
    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()