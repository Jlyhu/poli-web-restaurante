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
   * El Modelo y la Vista se reciben como parámetros (inyección de
   * dependencias) en lugar de crearse aquí dentro. Así se pueden reemplazar
   * fácilmente, por ejemplo por un modelo falso para hacer pruebas.
   *
   * @param {import('../models/UsuarioModel.js').UsuarioModel} modelo
   * @param {import('../views/UsuarioView.js').UsuarioView} vista
   */
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;

    /**
     * Copia local de los usuarios que se muestran en la tabla. Se usa para
     * llenar el formulario al editar sin volver a consultar el servidor.
     * @type {import('../models/Usuario.js').Usuario[]}
     */
    this.usuarios = [];

    /** true cuando el formulario está editando un usuario existente. */
    this.editando = false;

    // Se conectan los eventos de la Vista con los métodos del Controlador.
    // Las funciones flecha conservan el "this" del Controlador; si se pasara
    // this.guardar directamente, dentro de él "this" sería undefined.
    this.vista.alEnviarFormulario((usuario) => this.guardar(usuario));
    this.vista.alCancelarEdicion(() => this.cancelarEdicion());
    this.vista.alRecargar(() => this.cargarUsuarios());
    this.vista.alEditarOEliminar((accion, id) =>
      accion === 'editar' ? this.editar(id) : this.eliminar(id)
    );
  }

  /** Arranca la aplicación cargando la lista inicial. */
  iniciar() {
    this.cargarUsuarios();
  }

  /** Consulta los usuarios al servidor y los muestra en la tabla. */
  async cargarUsuarios() {
    this.vista.mostrarCargando();
    try {
      this.usuarios = await this.modelo.listar();
      this.vista.mostrarUsuarios(this.usuarios);
    } catch (error) {
      this.vista.mostrarUsuarios([]);
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  /**
   * Inserta o actualiza, según el modo en que esté el formulario.
   * @param {import('../models/Usuario.js').Usuario} usuario
   */
  async guardar(usuario) {
    // 1. Validación en el cliente: evita viajes innecesarios al servidor.
    const errores = usuario.validar();
    if (errores.length > 0) {
      this.vista.mostrarMensaje(errores.join(' '), 'error');
      return;
    }

    // 2. Al insertar, se revisa que el id no exista ya en la lista.
    //    (La base de datos también lo rechazaría, pero con un mensaje técnico.)
    if (!this.editando && this.usuarios.some((u) => u.idusuario === usuario.idusuario)) {
      this.vista.mostrarMensaje(`Ya existe un usuario con id ${usuario.idusuario}.`, 'error');
      return;
    }

    // 3. Petición al servidor. try/finally garantiza que el botón se
    //    desbloquee aunque ocurra un error.
    this.vista.bloquearFormulario(true);
    try {
      if (this.editando) {
        await this.modelo.actualizar(usuario);
        this.vista.mostrarMensaje(`Se actualizó a ${usuario.nombreCompleto}.`);
      } else {
        await this.modelo.insertar(usuario);
        this.vista.mostrarMensaje(`Se registró a ${usuario.nombreCompleto}.`);
      }
      this.cancelarEdicion();       // limpia el formulario
      await this.cargarUsuarios();  // refresca la tabla con los datos reales
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquearFormulario(false);
    }
  }

  /**
   * Pasa el formulario a modo edición con el usuario seleccionado.
   * @param {number} id
   */
  editar(id) {
    const usuario = this.usuarios.find((u) => u.idusuario === id);
    if (!usuario) return;
    this.editando = true;
    this.vista.activarModoEdicion(usuario);
  }

  /** Sale del modo edición y deja el formulario vacío. */
  cancelarEdicion() {
    this.editando = false;
    this.vista.activarModoCreacion();
  }

  /**
   * Elimina un usuario previa confirmación del usuario.
   * @param {number} id
   */
  async eliminar(id) {
    const usuario = this.usuarios.find((u) => u.idusuario === id);
    const nombre = usuario ? usuario.nombreCompleto : `el usuario ${id}`;

    if (!this.vista.confirmar(`¿Seguro que desea eliminar a ${nombre}?`)) {
      return;
    }

    try {
      await this.modelo.eliminar(id);
      this.vista.mostrarMensaje(`Se eliminó a ${nombre}.`);
      await this.cargarUsuarios();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}
