/** PagosController.js (CONTROLADOR) - Cajero: ver pedidos y registrar el pago de los entregados. */
import { obtenerSesion } from '../core/sesion.js';

export class PagosController {
  constructor(seguimientoModel, cajaModel, vista) {
    this.seguimientoModel = seguimientoModel;
    this.cajaModel = cajaModel;
    this.vista = vista;
    const sesion = obtenerSesion();
    this.idCajero = sesion?.rol === 'Cajero' ? sesion.idRol : null;
    this.vista.alActualizar(() => this.cargar());
    this.vista.alCobrar((id, metodo) => this.cobrar(id, metodo));
  }

  iniciar() {
    return this.cargar();
  }

  async cargar() {
    try {
      const [entregados, enCurso, caja] = await Promise.all([
        this.seguimientoModel.listar({ estado: 'ENTREGADO' }),
        this.seguimientoModel.listar({ activos: true }),
        this.idCajero ? this.cajaModel.cajaAbierta(this.idCajero) : Promise.resolve(null),
      ]);
      const hayCaja = Boolean(caja);
      this.vista.mostrarAvisoCaja(!hayCaja);
      this.vista.mostrarPorCobrar(entregados.filter((p) => !p.pagado), hayCaja);
      this.vista.mostrarEnCurso(enCurso);
      this.vista.mostrarPagados(entregados.filter((p) => p.pagado));
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async cobrar(idPedido, metodo) {
    try {
      const pago = await this.cajaModel.registrarPago(idPedido, this.idCajero, metodo);
      this.vista.mostrarMensaje(`Pago del pedido ${idPedido} registrado: ${this.vista.dinero(pago.monto)} (${metodo}).`);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.cargar();
  }
}
