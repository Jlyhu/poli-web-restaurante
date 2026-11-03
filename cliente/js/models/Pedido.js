/** Pedido.js (MODELO - Entidad). Pedido con el número de su mesa (GET /getPedidosConMesa). */
export class Pedido {
  constructor(idPedido, estado, creado, actualizado, idMesa, numeroMesa) {
    this.idPedido = idPedido;
    this.estado = estado;
    this.creado = creado;
    this.actualizado = actualizado;
    this.idMesa = idMesa;
    this.numeroMesa = numeroMesa;
  }

  static desdeJSON(o) {
    return new Pedido(
      Number(o.id_pedido), o.estado, o.fecha_creacion, o.fecha_ultima_actualizacion,
      o.id_mesa ?? null, o.numero_mesa ?? null
    );
  }
}
