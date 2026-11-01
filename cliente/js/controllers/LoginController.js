/**
 * LoginController.js  (CONTROLADOR)
 * -----------------------------------
 * Coordina el Modelo y la Vista. Es el único que conoce a ambos.
 *
 * Flujo típico:
 *   1. El usuario hace algo en la página  → la Vista llama al Controlador.
 *   2. El Controlador valida y le pide al Modelo los datos o el cambio.
 *   3. Con el resultado, el Controlador le indica a la Vista qué mostrar.
 *
 *     Usuario ──► Vista ──► Controlador ──► Modelo ──► Flask (REST)
 *                   ▲            │
 *                   └────────────┘  (actualiza la pantalla)
 */
export class LoginController {
  /**
   * @param {import('../models/UsuarioModel.js').UsuarioModel} modelo
   * @param {import('../views/LoginView.js').LoginView} vista
   */
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;
    this.vista.alIniciarSesion((datos) => this.iniciarSesion(datos));
  }

  async iniciarSesion({ nombre, credenciales }) {
    if (!nombre || !credenciales) {
      this.vista.mostrarMensaje('Ingrese el nombre y la contraseña.', 'error');
      return;
    }

    this.vista.bloquearFormulario(true);
    try {
      const respuesta = await this.modelo.iniciarSesion(nombre, credenciales);
      this.vista.mostrarMensaje(`Bienvenido, ${respuesta?.nombre ?? nombre}.`);
      setTimeout(() => this.vista.irA('index.html'), 800);
    } catch (error) {
      // 401 (datos malos), 403 (inactivo o sin rol), 400/415 (campos vacíos o sin JSON)
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquearFormulario(false);
    }
  }
}