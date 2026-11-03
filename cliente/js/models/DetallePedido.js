/** DetallePedido.js (MODELO - Entidad). Un renglón del pedido con nombre y precio del producto. */
export class DetallePedido {
  constructor(idDetalle, idProducto, nombre, cantidad, notas, precio, subtotal) {
    this.idDetalle = idDetalle;
    this.idProducto = idProducto;
    this.nombre = nombre;
    this.cantidad = cantidad;
    this.notas = notas;
    this.precio = precio;
    this.subtotal = subtotal;
  }

  static desdeJSON(o) {
    return new DetallePedido(
      Number(o.id_detalle_pedido), Number(o.Producto_idProducto), o.producto_nombre ?? '',
      Number(o.cantidad), o.notas ?? '', Number(o.precio_unitario ?? 0), Number(o.subtotal ?? 0)
    );
  }
}
