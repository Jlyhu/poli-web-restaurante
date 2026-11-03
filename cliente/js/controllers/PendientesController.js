/**
 * PendientesController.js (CONTROLADOR) - HU-08.
 * Lista los pedidos PENDIENTES (más antiguo primero) y muestra su detalle completo.
 * Se refresca sola cada 30 segundos.
 */
const REFRESCO_MS = 30000;

export class PendientesController {
  constructor(pedidoModel, detalleModel, vista, panel) {
    this.pedidoModel = pedidoModel;
    this.detalleModel = detalleModel;
    this.vista = vista;
    this.panel = panel;
    this.pedidos = [];

    this.vista.alActualizar(() => this.cargar());
    this.vista.alVerDetalle((id) => this.verDetalle(id));
  }

  iniciar() {
    this.cargar();
    setInterval(() => this.cargar(), REFRESCO_MS);
  }

  async cargar() {
    try {
      this.pedidos = await this.pedidoModel.listar({ estado: 'PENDIENTE' });
      this.vista.mostrarPendientes(this.pedidos);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async verDetalle(idPedido) {
    const pedido = this.pedidos.find((p) => p.idPedido === idPedido);
    if (!pedido) return;
    try {
      this.panel.abrir(pedido, await this.detalleModel.listar(idPedido));
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}
