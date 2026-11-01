/**
 * Producto.js  (MODELO - Entidad)
 * Representa un producto del menú. Equivale a la tabla Producto.
 */
export class Producto {
  /**
   * @param {number|null} idProducto  null mientras el producto no existe.
   * @param {string} nombre
   * @param {string} descripcion
   * @param {number} precio
   * @param {number} cantidad         Unidades disponibles (0 = agotado).
   * @param {number} idCategoria      Categoría a la que pertenece.
   */
  constructor(idProducto, nombre, descripcion, precio, cantidad, idCategoria) {
    this.idProducto = idProducto;
    this.nombre = nombre;
    this.descripcion = descripcion;
    this.precio = precio;
    this.cantidad = cantidad;
    this.idCategoria = idCategoria;
  }

  /** Crea un Producto desde un objeto de GET /getProductos. */
  static desdeJSON(obj) {
    return new Producto(
      Number(obj.idProducto),
      obj.nombre ?? '',
      obj.descripcion ?? '',
      Number(obj.precio ?? 0),
      Number(obj.cantidad_disponible ?? 0),
      Number(obj.Categoria_id_categoria)
    );
  }

  /**
   * Cuerpo de POST y PUT. Las llaves deben llamarse igual que en el
   * ProductoSchema del backend (que rechaza campos desconocidos).
   */
  aJSON() {
    return {
      nombre: this.nombre,
      descripcion: this.descripcion.trim() || null,
      precio: this.precio,
      cantidad_disponible: this.cantidad,
      Categoria_id_categoria: this.idCategoria
    };
  }

  /** @returns {string[]} Errores de validación. Vacía si todo es válido. */
  validar(esNuevo) {
    const errores = [];
    if (!esNuevo && (!Number.isInteger(this.idProducto) || this.idProducto <= 0)) {
      errores.push('El id del producto no es válido.');
    }
    if (!this.nombre.trim()) {
      errores.push('El nombre es obligatorio.');
    }
    if (this.nombre.length > 100) {
      errores.push('El nombre no puede pasar de 100 caracteres.');
    }
    if (this.descripcion.length > 100) {
      errores.push('La descripción no puede pasar de 100 caracteres.');
    }
    if (!Number.isFinite(this.precio) || this.precio < 0) {
      errores.push('El precio debe ser un número mayor o igual a 0.');
    }
    if (!Number.isInteger(this.cantidad) || this.cantidad < 0) {
      errores.push('La cantidad debe ser un entero mayor o igual a 0.');
    }
    if (!Number.isInteger(this.idCategoria) || this.idCategoria <= 0) {
      errores.push('Seleccione una categoría.');
    }
    return errores;
  }

  /** @returns {boolean} true si quedan unidades para vender. */
  get disponible() {
    return this.cantidad > 0;
  }
}