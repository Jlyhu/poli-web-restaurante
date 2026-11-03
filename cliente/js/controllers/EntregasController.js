/** EntregasController.js (CONTROLADOR) - Repartidor: ver pedidos asignados, datos de entrega y entregar. */
import { obtenerSesion } from '../core/sesion.js';

const REFRESCO_MS = 30000;

export class EntregasController {
  constructor(modelo, detalleModel, vista, panel) {
    this.modelo = modelo;
    this.detalleModel = detalleModel;
    this.vista = vista;
    this.panel = panel;
    const sesion = obtenerSesion();
    this.idRepartidor = sesion?.rol === 'Repartidor' ? sesion.idRol : null;
    this.vista.alActualizar(() => this.cargar());
    this.vista.alAccionar((accion, id) => this.accionar(accion, id));
  }

  async iniciar() {
    if (!this.idRepartidor) {
      this.vista.mostrarMensaje('Esta pantalla es para el repartidor que inició sesión.', 'error');
      return;
    }
    await this.cargar();
    setInterval(() => this.cargar(), REFRESCO_MS);
  }

  async cargar() {
    try {
      let pedidos = await this.modelo.listar({ repartidor: this.idRepartidor });
      if (!this.vista.verEntregados()) {
        pedidos = pedidos.filter((p) => p.estado !== 'ENTREGADO' && p.estado !== 'CANCELADO');
      }
      this.vista.mostrarEntregas(pedidos);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async accionar(accion, idPedido) {
    try {
      if (accion === 'detalle') {
        const pedido = await this.modelo.estado(idPedido);
        this.panel.abrir(pedido, await this.detalleModel.listar(idPedido));
        return;
      }
      await this.modelo.entregar(idPedido);      // mismo servicio de HU-06: LISTO → ENTREGADO
      this.vista.mostrarMensaje(`Pedido ${idPedido} entregado al cliente.`);
      this.panel.cerrar();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.cargar();
  }
}
