from DataAccess import UsuarioDAO as u
from DataAccess import AdministradorDAO as a


def main() -> int:
    try:
        print("=== CREAR USUARIO DE PRUEBA ===")
        u.crearUsuario(999, "Usuario Prueba", "prueba")

        print("\n=== CREAR ADMINISTRADOR ===")
        a.crearAdministrador(999, 999)

        print("\n=== ADMINISTRADORES ACTUALES ===")
        a.findAllAdministradores()

        print("\n=== EDITAR ADMINISTRADOR ===")
        a.editarAdministrador(999, 999)

        print("\n=== ADMINISTRADORES DESPUES DE EDITAR ===")
        a.findAllAdministradores()

        print("\n=== ELIMINAR ADMINISTRADOR ===")
        a.eliminarAdministrador(999)

        print("\n=== ADMINISTRADORES DESPUES DE ELIMINAR ===")
        a.findAllAdministradores()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()