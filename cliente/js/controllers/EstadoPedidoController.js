/**
 * EstadoPedidoController.js (CONTROLADOR) - HU-05, HU-06, HU-07.
 * Recibe los eventos de la Vista, pide los datos al Modelo y decide qué mostrar.
 * Si quien inició sesión es mesero puede filtrar "solo mis pedidos".
 */
import { obtenerSesion } from '../core/sesion.js';

const REFRESCO_MS = 30000;   // así el mesero ve cuándo cocina marca un pedido como LISTO

export class EstadoPedidoController {
  constructor(modelo, detalleModel, vista, panel) {
    this.modelo = modelo;
    this.detalleModel = detalleModel;
    this.vista = vista;
    this.panel = panel;
    this.pedidos = [];
    const sesion = obtenerSesion();
    this.idMesero = sesion?.rol === 'Mesero' ? sesion.idRol : null;

    this.vista.alFiltrar(() => this.cargar());
    this.vista.alAccionar((accion, id) => this.accionar(accion, id));
  }

  async iniciar() {
    this.vista.habilitarSoloMios(Boolean(this.idMesero));
    await this.cargar();
    setInterval(() => this.cargar(), REFRESCO_MS);
  }

  async cargar() {
    const f = this.vista.filtros();
    try {
      let pedidos = await this.modelo.listar({
        estado: f.estado,
        activos: f.activos,
        mesero: f.soloMios ? this.idMesero : null,
      });
      // Los domicilios los entrega el repartidor (pantalla entregas.html), no el mesero
      pedidos = pedidos.filter((p) => (p.tipo ?? '').toLowerCase() !== 'domicilio');
      if (f.numero) pedidos = pedidos.filter((p) => String(p.idPedido).includes(f.numero));
      this.pedidos = pedidos;
      this.vista.mostrarPedidos(pedidos);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async accionar(accion, idPedido) {
    try {
      if (accion === 'detalle') {
        const pedido = await this.modelo.estado(idPedido);          // HU-05: estado actualizado
        this.panel.abrir(pedido, await this.detalleModel.listar(idPedido));
        return;
      }
      if (accion === 'entregar') {
        await this.modelo.entregar(idPedido);                        // HU-06
        this.vista.mostrarMensaje(`Pedido ${idPedido} entregado. La atención quedó finalizada.`);
      } else if (accion === 'cancelar') {
        await this.modelo.cancelar(idPedido);                        // HU-07
        this.vista.mostrarMensaje(`Pedido ${idPedido} cancelado.`);
      }
      this.panel.cerrar();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');             // p. ej. entregar un pedido que no está LISTO
    }
    await this.cargar();
  }
}
