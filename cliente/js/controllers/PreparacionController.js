/**
 * PreparacionController.js (CONTROLADOR) - HU-09.
 * PENDIENTE → EN PREPARACION → LISTO. El servidor valida el orden de los estados.
 * Si quien inició sesión es cocinero, queda elegido como responsable automáticamente.
 */
import { obtenerSesion } from '../core/sesion.js';

const REFRESCO_MS = 30000;

export class PreparacionController {
  constructor(pedidoModel, detalleModel, personalModel, vista, panel) {
    this.pedidoModel = pedidoModel;
    this.detalleModel = detalleModel;
    this.personalModel = personalModel;
    this.vista = vista;
    this.panel = panel;
    this.pedidos = [];

    this.vista.alActualizar(() => this.cargar());
    this.vista.alAccionar((accion, id) => this.accionar(accion, id));
  }

  async iniciar() {
    try {
      const sesion = obtenerSesion();
      const fijo = sesion?.rol === 'Cocinero' ? sesion.idRol : null;
      this.vista.mostrarCocineros(await this.personalModel.listarCocineros(), fijo);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.cargar();
    setInterval(() => this.cargar(), REFRESCO_MS);
  }

  async cargar() {
    try {
      const [pendientes, enPreparacion] = await Promise.all([
        this.pedidoModel.listar({ estado: 'PENDIENTE' }),
        this.pedidoModel.listar({ estado: 'EN PREPARACION' }),
      ]);
      this.pedidos = [...pendientes, ...enPreparacion];
      this.vista.mostrarPendientes(pendientes);
      this.vista.mostrarEnPreparacion(enPreparacion);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async accionar(accion, idPedido) {
    if (accion === 'detalle') return this.#verDetalle(idPedido);

    if (!this.vista.cocineroSeleccionado()) {
      this.vista.mostrarMensaje('Seleccione el cocinero responsable.', 'error');
      return;
    }
    const nuevoEstado = accion === 'iniciar' ? 'EN PREPARACION' : 'LISTO';
    try {
      await this.pedidoModel.cambiarEstado(idPedido, nuevoEstado);
      this.vista.mostrarMensaje(accion === 'iniciar'
        ? `Pedido ${idPedido} en preparación.`
        : `Pedido ${idPedido} listo para entregar.`);
      this.panel.cerrar();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');   // transición no permitida
    }
    await this.cargar();
  }

  async #verDetalle(idPedido) {
    const pedido = this.pedidos.find((p) => p.idPedido === idPedido);
    if (!pedido) return;
    try {
      this.panel.abrir(pedido, await this.detalleModel.listar(idPedido));
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}
