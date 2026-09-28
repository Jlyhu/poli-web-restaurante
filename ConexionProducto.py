from DataAccess import ProductoDAO as p

def main() -> int:
    try:
        p.findAllProductos()

        print("Crear producto")
        id = input("digite el id ")
        nombre = input("digite el nombre ")
        descripcion = input("digite la descripcion ")
        precio = input("digite el precio ")
        cantidad_disponible = input("digite la cantidad disponible ")
        Categoria_id_categoria = input("digite el id de la categoria ")
        p.crearProducto(id, nombre, descripcion, precio, cantidad_disponible, Categoria_id_categoria)
        p.findAllProductos()

        print("Editar producto")
        idU = input("digite el id a actualizar ")
        nombreU = input("digite el nombre actualizado ")
        descripcionU = input("digite la descripcion actualizada ")
        precioU = input("digite el precio actualizado ")
        p.editarProducto(nombreU, precioU, idU)
        p.findAllProductos()

        print("Eliminar producto")
        idD = input("digite el id a eliminar ")
        p.eliminarProducto(idD)
        p.findAllProductos()

        
    except ValueError:
        print("Valores no validos")

if __name__ == "__main__":
    main()