/** TrazabilidadController.js (CONTROLADOR) - HU-15 Consultar trazabilidad del pedido (Administrador). */
export class TrazabilidadController {
  constructor(modelo, detalleModel, vista, panel) {
    this.modelo = modelo;
    this.detalleModel = detalleModel;
    this.vista = vista;
    this.panel = panel;
    this.vista.alFiltrar(() => this.cargar());
    this.vista.alVerTrazabilidad((id) => this.ver(id));
  }

  iniciar() {
    return this.cargar();
  }

  async cargar() {
    const f = this.vista.filtros();
    try {
      let pedidos = await this.modelo.listar({ estado: f.estado, tipo: f.tipo });
      if (f.numero) pedidos = pedidos.filter((p) => String(p.idPedido).includes(f.numero));
      this.vista.mostrarResumen(pedidos);
      this.vista.mostrarPedidos(pedidos);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }

  async ver(idPedido) {
    try {
      const [pedido, detalle] = await Promise.all([
        this.modelo.trazabilidad(idPedido),
        this.detalleModel.listar(idPedido),
      ]);
      this.panel.abrir(pedido, detalle);
      this.vista.mostrarTrazabilidad(pedido);
    } catch (error) {
      this.vista.mostrarMensaje(error.message, 'error');
    }
  }
}
