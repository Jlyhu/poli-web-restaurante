/** MesasController.js (CONTROLADOR) - Mesero: ver mesas (reutiliza GET /getMesasDisponibilidad de HU-02). */
export class MesasController {
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;
    this.vista.alActualizar(() => this.cargar());
  }

  iniciar() { return this.cargar(); }

  async cargar() {
    try {
      this.vista.mostrarMesas(await this.modelo.mesasDisponibilidad());
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}
