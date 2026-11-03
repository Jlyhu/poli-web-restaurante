/**
 * LoginController.js  (CONTROLADOR)
 * HU-01: valida campos, pide el login al Modelo, guarda la sesión (usuario y rol)
 * y lleva al inicio, donde solo se muestran las opciones de ese rol.
 */
import { guardarSesion } from '../core/sesion.js';

export class LoginController {
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;
    this.vista.alIniciarSesion((datos) => this.iniciarSesion(datos));
  }

  async iniciarSesion({ nombre, credenciales }) {
    if (!nombre || !credenciales) {
      this.vista.mostrarMensaje('El nombre y la contraseña son obligatorios.', 'error');
      return;
    }
    this.vista.bloquearFormulario(true);
    try {
      const respuesta = await this.modelo.iniciarSesion(nombre, credenciales);
      guardarSesion(respuesta);
      this.vista.mostrarMensaje(`Bienvenido, ${respuesta.nombre} (${respuesta.rol}).`);
      setTimeout(() => this.vista.irA('index.html'), 800);
    } catch (error) {
      // 401 datos incorrectos, 403 usuario inactivo o sin rol
      this.vista.mostrarMensaje(error.message, 'error');
      this.vista.bloquearFormulario(false);
    }
  }
}
