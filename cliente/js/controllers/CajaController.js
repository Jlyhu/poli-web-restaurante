/** CajaController.js (CONTROLADOR) - Cajero: abrir y cerrar su caja. Usa el id del cajero de la sesión. */
import { obtenerSesion } from '../core/sesion.js';

export class CajaController {
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;
    this.caja = null;
    const sesion = obtenerSesion();
    this.idCajero = sesion?.rol === 'Cajero' ? sesion.idRol : null;
    this.vista.alAbrir((monto) => this.abrir(monto));
    this.vista.alCerrar((monto) => this.cerrar(monto));
  }

  async iniciar() {
    if (!this.idCajero) {
      this.vista.mostrarMensaje('Esta pantalla es para el cajero que inició sesión.', 'error');
      return;
    }
    await this.cargar();
  }

  async cargar() {
    try {
      this.caja = await this.modelo.cajaAbierta(this.idCajero);
      if (this.caja) this.vista.mostrarCaja(this.caja);
      else this.vista.mostrarSinCaja();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async abrir(montoInicial) {
    if (!(montoInicial >= 0)) {
      this.vista.mostrarMensaje('El monto inicial debe ser 0 o mayor.', 'error');
      return;
    }
    try {
      await this.modelo.abrir(this.idCajero, montoInicial);
      this.vista.mostrarMensaje('Caja abierta. Ya puede registrar pagos.');
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.cargar();
  }

  async cerrar(montoFinal) {
    if (!this.caja) return;
    if (!(montoFinal >= 0)) {
      this.vista.mostrarMensaje('Escriba el dinero contado.', 'error');
      return;
    }
    try {
      await this.modelo.cerrar(this.caja.id_caja, montoFinal);
      this.vista.mostrarMensaje(`Caja ${this.caja.id_caja} cerrada.`);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.cargar();
  }
}
