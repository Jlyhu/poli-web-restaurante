/** PendientesView.js (VISTA). HU-08: lista de pedidos pendientes, del más antiguo al más reciente. */
import { BaseView } from './BaseView.js';

export class PendientesView extends BaseView {
  constructor() {
    super();
    this.tbody = document.querySelector('#tabla-pendientes tbody');
    this.contador = document.querySelector('#contador-pendientes');
    this.btnActualizar = document.querySelector('#btn-actualizar');
  }

  alActualizar(cb) { this.btnActualizar.addEventListener('click', cb); }

  alVerDetalle(cb) {
    this.tbody.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-detalle]');
      if (b) cb(Number(b.dataset.detalle));
    });
  }

  mostrarPendientes(pedidos) {
    this.tbody.innerHTML = '';
    if (pedidos.length === 0) {
      this.contador.textContent = '';
      this.filaVacia(this.tbody, 5, 'No hay pedidos por preparar.');
      return;
    }
    this.contador.textContent = pedidos.length === 1 ? '1 pedido pendiente' : `${pedidos.length} pedidos pendientes`;
    pedidos.forEach((p, i) => {
      const tr = document.createElement('tr');
      tr.append(this.celda(i + 1), this.celda(p.idPedido), this.celda(`Mesa ${p.numeroMesa ?? '—'}`),
        this.celda(this.fecha(p.creado)),
        this.celda(this.boton('Ver detalle', 'btn-editar', { detalle: p.idPedido })));
      this.tbody.appendChild(tr);
    });
  }
}
