/** CrearPedidoView.js (VISTA). HU-02: selector de mesa, botón crear y tabla de pedidos activos. */
import { BaseView } from './BaseView.js';

export class CrearPedidoView extends BaseView {
  constructor() {
    super();
    this.selectMesa = document.querySelector('#select-mesa');
    this.btnCrear = document.querySelector('#btn-crear-pedido');
    this.tbody = document.querySelector('#tabla-pedidos tbody');
  }

  alCrear(callback) {
    this.btnCrear.addEventListener('click', callback);
  }

  /** Id de la mesa elegida, o null si no eligió ninguna. */
  mesaSeleccionada() {
    return this.selectMesa.value ? Number(this.selectMesa.value) : null;
  }

  mostrarMesas(mesas) {
    this.selectMesa.innerHTML = '<option value="">Seleccione una mesa</option>';
    for (const m of mesas) {
      const op = document.createElement('option');
      op.value = m.id_mesa;
      op.textContent = m.disponible ? `Mesa ${m.numero}` : `Mesa ${m.numero} (ocupada)`;
      op.disabled = !m.disponible;
      this.selectMesa.appendChild(op);
    }
  }

  mostrarPedidos(pedidos) {
    this.tbody.innerHTML = '';
    if (pedidos.length === 0) {
      this.filaVacia(this.tbody, 5, 'No hay pedidos activos.');
      return;
    }
    for (const p of pedidos) {
      const tr = document.createElement('tr');
      let accion = '—';
      if (p.estado === 'PENDIENTE') {
        accion = document.createElement('a');
        accion.href = `productos-pedido.html?pedido=${p.idPedido}`;
        accion.textContent = 'Agregar productos';
      }
      tr.append(this.celda(p.idPedido), this.celda(`Mesa ${p.numeroMesa ?? '—'}`),
        this.celda(this.badge(p.estado)), this.celda(this.fecha(p.creado)), this.celda(accion));
      this.tbody.appendChild(tr);
    }
  }

  bloquear(bloquear) {
    this.btnCrear.disabled = bloquear;
  }
}
