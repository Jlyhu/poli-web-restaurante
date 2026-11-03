/**
 * ProductosPedidoController.js (CONTROLADOR) - HU-03 y HU-04.
 * Agregar / quitar productos y registrar observaciones, solo en pedidos PENDIENTES.
 * Acepta ?pedido=<id> en la URL (así llega desde "Crear pedido").
 */
export class ProductosPedidoController {
  constructor(pedidoModel, detalleModel, productoModel, vista) {
    this.pedidoModel = pedidoModel;
    this.detalleModel = detalleModel;
    this.productoModel = productoModel;
    this.vista = vista;
    this.pedidos = [];

    this.vista.alElegirPedido((id) => this.elegirPedido(id));
    this.vista.alAgregar((datos) => this.agregar(datos));
    this.vista.alCambiarCantidad((id, cantidad) => this.cambiarCantidad(id, cantidad));
    this.vista.alQuitar((id) => this.quitar(id));
  }

  async iniciar() {
    try {
      this.pedidos = await this.pedidoModel.listar({ activos: true });
      const deUrl = Number(new URLSearchParams(window.location.search).get('pedido')) || null;
      this.vista.mostrarPedidos(this.pedidos, deUrl);
      this.vista.mostrarProductos(await this.productoModel.listarDisponibles());   // solo los disponibles (HU-12)
      await this.elegirPedido(deUrl);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  #pedido(id) {
    return this.pedidos.find((p) => p.idPedido === id) ?? null;
  }

  async elegirPedido(id) {
    const pedido = this.#pedido(id);
    if (!pedido) {
      this.vista.mostrarAviso(null);
      this.vista.permitirEdicion(false);
      this.vista.mostrarDetalle(null, false);
      return;
    }
    const editable = pedido.estado === 'PENDIENTE';
    this.vista.mostrarAviso(editable ? null :
      `El pedido ${pedido.idPedido} está ${pedido.estado}: solo se pueden agregar o quitar productos de un pedido PENDIENTE.`);
    this.vista.permitirEdicion(editable);
    await this.#recargarDetalle(id, editable);
  }

  async #recargarDetalle(id, editable) {
    try {
      this.vista.mostrarDetalle(await this.detalleModel.listar(id), editable);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async agregar({ idProducto, cantidad, notas }) {
    const id = this.vista.pedidoSeleccionado();
    if (!id) return this.vista.mostrarMensaje('Seleccione un pedido.', 'error');
    if (!idProducto) return this.vista.mostrarMensaje('Seleccione un producto.', 'error');
    if (!Number.isInteger(cantidad) || cantidad < 1) {
      return this.vista.mostrarMensaje('La cantidad debe ser un número entero mayor a cero.', 'error');
    }
    try {
      await this.detalleModel.agregar(id, idProducto, cantidad, notas);
      this.vista.mostrarMensaje('Producto agregado al pedido.');
      this.vista.limpiarFormulario();
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');   // pedido no pendiente, agotado, sin unidades...
    }
    await this.#recargarDetalle(id, true);
  }

  async cambiarCantidad(idDetalle, cantidad) {
    const id = this.vista.pedidoSeleccionado();
    if (!Number.isInteger(cantidad) || cantidad < 1) {
      this.vista.mostrarMensaje('La cantidad debe ser un número entero mayor a cero.', 'error');
    } else {
      try {
        await this.detalleModel.cambiarCantidad(idDetalle, cantidad);
      } catch (error) {
        this.vista.mostrarMensaje(error.message, 'error');
      }
    }
    await this.#recargarDetalle(id, true);
  }

  async quitar(idDetalle) {
    const id = this.vista.pedidoSeleccionado();
    try {
      await this.detalleModel.quitar(idDetalle);
      this.vista.mostrarMensaje('Producto quitado del pedido.');
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
    await this.#recargarDetalle(id, true);
  }
}
