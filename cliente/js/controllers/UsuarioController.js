/**
 * UsuarioController.js  (CONTROLADOR)
 * Coordina el Modelo y la Vista. Es el único que conoce a ambos.
 */
import { Usuario } from '../models/Usuario.js';

export class UsuarioController {
  /**
   * @param {import('../models/UsuarioModel.js').UsuarioModel} modelo
   * @param {import('../views/UsuarioView.js').UsuarioView} vista
   */
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;

    /** Copia local de los usuarios, para editar y filtrar sin volver al servidor. */
    this.usuarios = [];
    this.textoBusqueda = '';

    // Las funciones flecha conservan el "this" del Controlador.
    this.vista.alEnviarFormulario((datos) => this.guardar(datos));
    this.vista.alClicEditar((id) => this.editar(id));
    this.vista.alEliminar((id) => this.eliminar(id));
    this.vista.alBuscar((texto) => this.buscar(texto));
  }

  iniciar() {
    this.cargarUsuarios();
  }

  async cargarUsuarios() {
    this.vista.mostrarCargando();
    try {
      this.usuarios = await this.modelo.listar();
      this.mostrarFiltrados();
    } catch (error) {
      this.vista.mostrarUsuarios([]);
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  /** Filtra por nombre en el cliente y redibuja la tabla. */
  buscar(texto) {
    this.textoBusqueda = texto.toLowerCase();
    this.mostrarFiltrados();
  }

  mostrarFiltrados() {
    const filtrados = this.usuarios.filter((u) =>
      u.nombre.toLowerCase().includes(this.textoBusqueda)
    );
    this.vista.mostrarUsuarios(filtrados);
  }

  /**
   * Crea o actualiza según datos.idUsuario (null = crear).
   * @param {Object} datos  Lo que entrega la vista al enviar el formulario.
   */
  async guardar(datos) {
    const esNuevo = datos.idUsuario === null;

    const usuario = new Usuario(
      datos.idUsuario,
      datos.nombre,
      datos.credenciales,
      datos.estado,
      datos.rol,
      datos.datoRol
    );

    const errores = usuario.validar(esNuevo);
    if (errores.length > 0) {
      this.vista.mostrarMensaje(errores.join(' '), 'error');
      return;
    }

    this.vista.bloquearFormulario(true);
    try {
      if (esNuevo) {
        await this.modelo.insertar(usuario);
        this.vista.mostrarMensaje(`Se creó a ${usuario.nombre}.`);
      } else {
        await this.modelo.actualizar(usuario);
        this.vista.mostrarMensaje(`Se actualizó a ${usuario.nombre}.`);
      }
      this.vista.cerrarPanel();
      await this.cargarUsuarios();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquearFormulario(false);
    }
  }

  /** Abre el panel en modo edición con el usuario seleccionado. */
  editar(id) {
    const usuario = this.usuarios.find((u) => u.idUsuario === id);
    if (!usuario) return;
    this.vista.activarModoEdicion(usuario);
  }

  /** La vista ya pidió confirmación antes de llamar aquí. */
  async eliminar(id) {
    const usuario = this.usuarios.find((u) => u.idUsuario === id);
    const nombre = usuario ? usuario.nombre : `el usuario ${id}`;

    try {
      await this.modelo.eliminar(id);
      this.vista.mostrarMensaje(`Se eliminó a ${nombre}.`);
      this.vista.cerrarPanel();
      await this.cargarUsuarios();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}