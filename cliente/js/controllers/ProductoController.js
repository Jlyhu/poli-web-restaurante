/**
 * ProductoController.js  (CONTROLADOR)
 * Coordina ProductoModel, CategoriaModel y ProductoView.
 */
import { Producto } from '../models/Producto.js';

/** Convierte el texto de un input a número; '' queda como NaN (inválido). */
const numero = (texto) => (texto === '' ? NaN : Number(texto));

export class ProductoController {
  /**
   * @param {import('../models/ProductoModel.js').ProductoModel} modelo
   * @param {import('../models/CategoriaModel.js').CategoriaModel} modeloCategoria
   * @param {import('../views/ProductoView.js').ProductoView} vista
   */
  constructor(modelo, modeloCategoria, vista) {
    this.modelo = modelo;
    this.modeloCategoria = modeloCategoria;
    this.vista = vista;

    /** Copias locales para editar y filtrar sin volver al servidor. */
    this.productos = [];
    this.categorias = [];
    this.textoBusqueda = '';

    this.vista.alEnviarFormulario((datos) => this.guardar(datos));
    this.vista.alClicEditar((id) => this.editar(id));
    this.vista.alEliminar((id) => this.eliminar(id));
    this.vista.alBuscar((texto) => this.buscar(texto));
  }

  async iniciar() {
    this.vista.mostrarCargando();
    try {
      // Primero las categorías: la lista desplegable y la tabla las necesitan.
      this.categorias = await this.modeloCategoria.listar();
      this.vista.cargarCategorias(this.categorias);
      if (this.categorias.length === 0) {
        this.vista.mostrarMensaje('Primero cree al menos una categoría en "Gestionar categorías y mesas".', 'error');
      }
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.cargarProductos();
  }

  async cargarProductos() {
    this.vista.mostrarCargando();
    try {
      this.productos = await this.modelo.listar();
      this.mostrarFiltrados();
    } catch (error) {
      this.vista.mostrarProductos([], new Map());
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  buscar(texto) {
    this.textoBusqueda = texto.toLowerCase();
    this.mostrarFiltrados();
  }

  mostrarFiltrados() {
    const nombresCategoria = new Map(this.categorias.map((c) => [c.idCategoria, c.nombre]));
    const filtrados = this.productos.filter((p) =>
      p.nombre.toLowerCase().includes(this.textoBusqueda)
    );
    this.vista.mostrarProductos(filtrados, nombresCategoria);
  }

  /**
   * Crea o actualiza según datos.idProducto (null = crear).
   * @param {Object} datos  Lo que entrega la vista al enviar el formulario.
   */
  async guardar(datos) {
    const esNuevo = datos.idProducto === null;

    const producto = new Producto(
      datos.idProducto,
      datos.nombre,
      datos.descripcion,
      numero(datos.precio),
      numero(datos.cantidad),
      Number(datos.idCategoria)
    );

    const errores = producto.validar(esNuevo);
    if (errores.length > 0) {
      this.vista.mostrarMensaje(errores.join(' '), 'error');
      return;
    }

    this.vista.bloquearFormulario(true);
    try {
      if (esNuevo) {
        await this.modelo.insertar(producto);
        this.vista.mostrarMensaje(`Se creó ${producto.nombre}.`);
      } else {
        await this.modelo.actualizar(producto);
        this.vista.mostrarMensaje(`Se actualizó ${producto.nombre}.`);
      }
      this.vista.cerrarPanel();
      await this.cargarProductos();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquearFormulario(false);
    }
  }

  /** Abre el panel en modo edición con el producto seleccionado. */
  editar(id) {
    const producto = this.productos.find((p) => p.idProducto === id);
    if (!producto) return;
    this.vista.activarModoEdicion(producto);
  }

  /** La vista ya pidió confirmación antes de llamar aquí. */
  async eliminar(id) {
    const producto = this.productos.find((p) => p.idProducto === id);
    const nombre = producto ? producto.nombre : `el producto ${id}`;

    try {
      await this.modelo.eliminar(id);
      this.vista.mostrarMensaje(`Se eliminó ${nombre}.`);
      this.vista.cerrarPanel();
      await this.cargarProductos();
    } catch (error) {
      // Si el producto ya está en un pedido, el backend responde 409.
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}