/**
 * ReportesController.js (CONTROLADOR) - HU-14.
 * Reporte de ventas (pedidos ENTREGADOS, con filtro de fechas) y de tiempos de preparación.
 * Si quien inició sesión es administrador, queda elegido automáticamente.
 */
import { obtenerSesion } from '../core/sesion.js';

export class ReportesController {
  constructor(reporteModel, personalModel, vista) {
    this.reporteModel = reporteModel;
    this.personalModel = personalModel;
    this.vista = vista;
    this.vista.alConsultar(() => this.consultar());
    this.vista.alLimpiar(() => this.vista.limpiar());
  }

  async iniciar() {
    try {
      const sesion = obtenerSesion();
      const fijo = sesion?.rol === 'Administrador' ? sesion.idRol : null;
      this.vista.mostrarAdministradores(await this.personalModel.listarAdministradores(), fijo);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async consultar() {
    const filtros = this.vista.filtros();
    if (!filtros.administrador) {
      this.vista.mostrarMensaje('Seleccione el administrador que consulta el reporte.', 'error');
      return;
    }
    if (filtros.desde && filtros.hasta && filtros.desde > filtros.hasta) {
      this.vista.mostrarMensaje('La fecha inicial no puede ser mayor que la final.', 'error');
      return;
    }
    try {
      const [ventas, tiempos] = await Promise.all([
        this.reporteModel.ventas(filtros),
        this.reporteModel.tiempos(filtros),
      ]);
      this.vista.mostrar(ventas, tiempos);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}
