/**
 * DisponibilidadController.js  (CONTROLADOR)
 * Coordina ProductoModel y DisponibilidadView.
 */
import { Producto } from '../models/Producto.js';

export class DisponibilidadController {
  /**
   * @param {import('../models/ProductoModel.js').ProductoModel} modelo
   * @param {import('../views/DisponibilidadView.js').DisponibilidadView} vista
   */
  constructor(modelo, vista) {
    this.modelo = modelo;
    this.vista = vista;

    /** Copia local de los productos que se están mostrando. */
    this.productos = [];
    this.textoBusqueda = '';
    this.filtro = 'todos';    // 'todos' | 'disponibles' | 'agotados'

    this.vista.alGuardarCantidad((id, texto) => this.cambiarCantidad(id, texto));
    this.vista.alAgotar((id) => this.agotar(id));
    this.vista.alBuscar((texto) => this.buscar(texto));
    this.vista.alCambiarFiltro((filtro) => this.cambiarFiltro(filtro));
  
        this.vista.alEliminar((id) => this.eliminar(id));
  }

  iniciar() {
    this.cargarProductos();
  }

  async cargarProductos() {
    this.vista.mostrarCargando();
    try {
      if (this.filtro === 'disponibles') {
        // Usa el servicio específico de HU-12
        this.productos = await this.modelo.listarDisponibles();
      } else {
        const todos = await this.modelo.listar();
        this.productos = this.filtro === 'agotados'
          ? todos.filter((p) => !p.disponible)
          : todos;
      }
      this.mostrarFiltrados();
    } catch (error) {
      this.vista.mostrarProductos([]);
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  cambiarFiltro(filtro) {
    this.filtro = filtro;
    this.cargarProductos();
  }

  buscar(texto) {
    this.textoBusqueda = texto.toLowerCase();
    this.mostrarFiltrados();
  }

  mostrarFiltrados() {
    const filtrados = this.productos.filter((p) =>
      p.nombre.toLowerCase().includes(this.textoBusqueda)
    );
    this.vista.mostrarProductos(filtrados);
  }

  /** Cambia las unidades de un producto.  →  PUT /updateProducto/<id> */
  async cambiarCantidad(id, texto) {
    const original = this.productos.find((p) => p.idProducto === id);
    if (!original) return;

    const cantidad = texto === '' ? NaN : Number(texto);

    // Copia del producto con la nueva cantidad; el resto de campos no cambia.
    const producto = new Producto(
      original.idProducto, original.nombre, original.descripcion,
      original.precio, cantidad, original.idCategoria
    );

    const errores = producto.validar(false);
    if (errores.length > 0) {
      this.vista.mostrarMensaje(errores.join(' '), 'error');
      return;
    }

    try {
      await this.modelo.actualizar(producto);
      this.vista.mostrarMensaje(`Se actualizó la disponibilidad de ${producto.nombre}.`);
      await this.cargarProductos();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  /** La vista ya pidió confirmación.  →  PUT /agotarProducto/<id> */
  async agotar(id) {
    const producto = this.productos.find((p) => p.idProducto === id);
    const nombre = producto ? producto.nombre : `el producto ${id}`;

    try {
      await this.modelo.agotar(id);
      this.vista.mostrarMensaje(`${nombre} quedó agotado.`);
      await this.cargarProductos();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  /** La vista ya pidió confirmación.  →  DELETE /deleteProducto/<id> */
  async eliminar(id) {
    const producto = this.productos.find((p) => p.idProducto === id);
    const nombre = producto ? producto.nombre : `el producto ${id}`;

    try {
      await this.modelo.eliminar(id);
      this.vista.mostrarMensaje(`Se eliminó ${nombre}.`);
      await this.cargarProductos();
    } catch (error) {
      // Si el producto ya está en un pedido, el backend responde 409: en ese caso, usar Agotar.
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}