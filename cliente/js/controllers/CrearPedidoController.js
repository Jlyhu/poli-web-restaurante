/**
 * CrearPedidoController.js (CONTROLADOR) - HU-02 Crear pedido.
 * Si quien inició sesión es un mesero, su id queda asociado al pedido.
 */
import { obtenerSesion } from '../core/sesion.js';

export class CrearPedidoController {
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;
    this.vista.alCrear(() => this.crear());
  }

  iniciar() {
    return this.cargar();
  }

  async cargar() {
    try {
      const [mesas, pedidos] = await Promise.all([
        this.modelo.mesasDisponibilidad(),
        this.modelo.listar({ activos: true }),
      ]);
      this.vista.mostrarMesas(mesas);
      this.vista.mostrarPedidos(pedidos);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async crear() {
    const idMesa = this.vista.mesaSeleccionada();
    if (!idMesa) {
      this.vista.mostrarMensaje('Debe seleccionar una mesa antes de continuar.', 'error');
      return;
    }
    const sesion = obtenerSesion();
    const idMesero = sesion?.rol === 'Mesero' ? sesion.idRol : null;

    this.vista.bloquear(true);
    try {
      const pedido = await this.modelo.crear(idMesa, idMesero);
      this.vista.mostrarMensaje(`Pedido ${pedido.idPedido} creado para la mesa ${pedido.numeroMesa}. Quedó PENDIENTE para cocina.`);
    } catch (error) {
      // 409: la mesa ya tiene un pedido activo
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquear(false);
      await this.cargar();
    }
  }
}
