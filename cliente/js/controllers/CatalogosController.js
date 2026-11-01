/**
 * CatalogosController.js  (CONTROLADOR)
 * Coordina CategoriaModel, MesaModel y CatalogosView.
 */
import { Categoria } from '../models/Categoria.js';
import { Mesa } from '../models/Mesa.js';

export class CatalogosController {
  /**
   * @param {import('../models/CategoriaModel.js').CategoriaModel} modeloCategoria
   * @param {import('../models/MesaModel.js').MesaModel} modeloMesa
   * @param {import('../views/CatalogosView.js').CatalogosView} vista
   */
  constructor(modeloCategoria, modeloMesa, vista) {
    this.modeloCategoria = modeloCategoria;
    this.modeloMesa = modeloMesa;
    this.vista = vista;

    /** Copias locales para editar y filtrar sin volver al servidor. */
    this.categorias = [];
    this.mesas = [];
    this.busquedaCategoria = '';
    this.busquedaMesa = '';

    // Categorías
    this.vista.alEnviarFormularioCategoria((datos) => this.guardarCategoria(datos));
    this.vista.alClicEditarCategoria((id) => this.editarCategoria(id));
    this.vista.alEliminarCategoria((id) => this.eliminarCategoria(id));
    this.vista.alBuscarCategoria((texto) => this.buscarCategoria(texto));

    // Mesas
    this.vista.alEnviarFormularioMesa((datos) => this.guardarMesa(datos));
    this.vista.alClicEditarMesa((id) => this.editarMesa(id));
    this.vista.alEliminarMesa((id) => this.eliminarMesa(id));
    this.vista.alBuscarMesa((texto) => this.buscarMesa(texto));
  }

  iniciar() {
    this.vista.mostrarCargando();
    this.cargarCategorias();
    this.cargarMesas();
  }

  // ===================== CATEGORÍAS =====================

  async cargarCategorias() {
    try {
      this.categorias = await this.modeloCategoria.listar();
      this.mostrarCategoriasFiltradas();
    } catch (error) {
      this.vista.mostrarCategorias([]);
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  buscarCategoria(texto) {
    this.busquedaCategoria = texto.toLowerCase();
    this.mostrarCategoriasFiltradas();
  }

  mostrarCategoriasFiltradas() {
    const filtradas = this.categorias.filter((c) =>
      c.nombre.toLowerCase().includes(this.busquedaCategoria)
    );
    this.vista.mostrarCategorias(filtradas);
  }

  /** Crea o actualiza según datos.idCategoria (null = crear). */
  async guardarCategoria(datos) {
    const esNuevo = datos.idCategoria === null;
    const categoria = new Categoria(datos.idCategoria, datos.nombre);

    const errores = categoria.validar(esNuevo);
    if (errores.length > 0) {
      this.vista.mostrarMensaje(errores.join(' '), 'error');
      return;
    }

    this.vista.bloquearFormularioCategoria(true);
    try {
      if (esNuevo) {
        await this.modeloCategoria.insertar(categoria);
        this.vista.mostrarMensaje(`Se creó la categoría ${categoria.nombre}.`);
      } else {
        await this.modeloCategoria.actualizar(categoria);
        this.vista.mostrarMensaje(`Se actualizó la categoría ${categoria.nombre}.`);
      }
      this.vista.cerrarPanel();
      await this.cargarCategorias();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquearFormularioCategoria(false);
    }
  }

  async editarCategoria(id) {
    try {
      const categoria = await this.modeloCategoria.obtener(id);
      this.vista.activarModoEdicionCategoria(categoria);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  /** La vista ya pidió confirmación antes de llamar aquí. */
  async eliminarCategoria(id) {
    const categoria = this.categorias.find((c) => c.idCategoria === id);
    const nombre = categoria ? categoria.nombre : `la categoría ${id}`;

    try {
      await this.modeloCategoria.eliminar(id);
      this.vista.mostrarMensaje(`Se eliminó ${nombre}.`);
      this.vista.cerrarPanel();
      await this.cargarCategorias();
    } catch (error) {
      // Si la categoría ya tiene productos, el backend responde 409.
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  // ===================== MESAS =====================

  async cargarMesas() {
    try {
      this.mesas = await this.modeloMesa.listar();
      this.mostrarMesasFiltradas();
    } catch (error) {
      this.vista.mostrarMesas([]);
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  buscarMesa(texto) {
    this.busquedaMesa = texto.toLowerCase();
    this.mostrarMesasFiltradas();
  }

  mostrarMesasFiltradas() {
    const filtradas = this.mesas.filter((m) =>
      String(m.numero).includes(this.busquedaMesa)
    );
    this.vista.mostrarMesas(filtradas);
  }

  /** Crea o actualiza según datos.idMesa (null = crear). */
  async guardarMesa(datos) {
    const esNuevo = datos.idMesa === null;
    const numero = datos.numero === '' ? NaN : Number(datos.numero);
    const mesa = new Mesa(datos.idMesa, numero, datos.estado);

    const errores = mesa.validar(esNuevo);

    // Regla del cliente: no repetir el número de mesa.
    if (this.mesas.some((m) => m.numero === mesa.numero && m.idMesa !== mesa.idMesa)) {
      errores.push(`Ya existe la mesa número ${mesa.numero}.`);
    }

    if (errores.length > 0) {
      this.vista.mostrarMensaje(errores.join(' '), 'error');
      return;
    }

    this.vista.bloquearFormularioMesa(true);
    try {
      if (esNuevo) {
        await this.modeloMesa.insertar(mesa);
        this.vista.mostrarMensaje(`Se creó la mesa ${mesa.numero}.`);
      } else {
        await this.modeloMesa.actualizar(mesa);
        this.vista.mostrarMensaje(`Se actualizó la mesa ${mesa.numero}.`);
      }
      this.vista.cerrarPanel();
      await this.cargarMesas();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    } finally {
      this.vista.bloquearFormularioMesa(false);
    }
  }

  async editarMesa(id) {
    try {
      const mesa = await this.modeloMesa.obtener(id);
      this.vista.activarModoEdicionMesa(mesa);
  } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  /** La vista ya pidió confirmación antes de llamar aquí. */
  async eliminarMesa(id) {
    const mesa = this.mesas.find((m) => m.idMesa === id);
    const nombre = mesa ? `la mesa ${mesa.numero}` : `la mesa ${id}`;

    try {
      await this.modeloMesa.eliminar(id);
      this.vista.mostrarMensaje(`Se eliminó ${nombre}.`);
      this.vista.cerrarPanel();
      await this.cargarMesas();
    } catch (error) {
      // Si la mesa ya está en un pedido o reservación, el backend responde 409.
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}