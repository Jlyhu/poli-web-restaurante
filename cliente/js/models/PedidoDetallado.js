/**
 * PedidoDetallado.js (MODELO - Entidad).
 * Pedido con su mesa, mesero, repartidor, cliente, total y pago (GET /getPedidosDetallados).
 * La usan HU-05, HU-06, HU-07, HU-15 y las pantallas de Cajero y Repartidor.
 */
export class PedidoDetallado {
  constructor(o) {
    this.idPedido = Number(o.id_pedido);
    this.estado = (o.estado ?? '').toUpperCase();
    this.tipo = o.tipo_pedido ?? '—';
    this.creado = o.fecha_creacion;
    this.actualizado = o.fecha_ultima_actualizacion;
    this.idMesa = o.id_mesa ?? null;
    this.numeroMesa = o.numero_mesa ?? null;
    this.idMesero = o.Mesero_id_mesero ?? null;
    this.nombreMesero = o.nombre_mesero ?? null;
    this.idRepartidor = o.Repartidor_id_repartidor ?? null;
    this.nombreRepartidor = o.nombre_repartidor ?? null;
    this.cliente = {
      nombre: o.cliente_nombre ?? null,
      direccion: o.cliente_direccion ?? null,
      telefono: o.cliente_telefono ?? null,
    };
    this.total = Number(o.total ?? 0);
    this.pagado = Boolean(o.pagado);
    this.fechaPago = o.fecha_pago ?? null;
    this.metodoPago = o.metodo_pago ?? null;
    this.minutos = o.minutos_abierto ?? o.minutos_transcurridos ?? null;
    this.eventos = o.eventos ?? [];
  }

  static desdeJSON(o) {
    return new PedidoDetallado(o);
  }

  /** HU-06: solo un pedido LISTO se puede entregar. */
  sePuedeEntregar() { return this.estado === 'LISTO'; }

  /** HU-07: se puede cancelar mientras no esté listo ni entregado. */
  sePuedeCancelar() { return this.estado === 'PENDIENTE' || this.estado === 'EN PREPARACION'; }

  /** Texto corto de dónde va el pedido: la mesa o el cliente a domicilio. */
  destino() {
    if (this.numeroMesa != null) return `Mesa ${this.numeroMesa}`;
    if (this.cliente.nombre) return `Domicilio · ${this.cliente.nombre}`;
    return '—';
  }
}
