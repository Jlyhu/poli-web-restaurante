/** DetallePanelView.js (VISTA). Panel lateral con productos, cantidades y observaciones de un pedido. */
import { BaseView } from './BaseView.js';

export class DetallePanelView extends BaseView {
  constructor() {
    super();
    this.panel = document.querySelector('#panel-lateral-formulario');
    this.titulo = document.querySelector('#panel-titulo');
    this.subtitulo = document.querySelector('#panel-subtitulo');
    this.tbody = document.querySelector('#panel-tabla tbody');
    this.total = document.querySelector('#panel-total');
    this.btnCerrar = document.querySelector('#btn-cerrar-panel');
    this.btnCerrar.addEventListener('click', () => this.cerrar());
  }

  abrir(pedido, detalle) {
    this.titulo.textContent = `Pedido ${pedido.idPedido}`;
    this.subtitulo.textContent = `Mesa ${pedido.numeroMesa ?? '—'} · ${pedido.estado} · ${this.fecha(pedido.creado)}`;
    this.tbody.innerHTML = '';
    if (detalle.renglones.length === 0) {
      this.filaVacia(this.tbody, 3, 'Este pedido aún no tiene productos.');
    }
    for (const r of detalle.renglones) {
      const tr = document.createElement('tr');
      tr.append(this.celda(r.nombre), this.celda(r.cantidad), this.celda(r.notas || '—'));
      this.tbody.appendChild(tr);
    }
    this.total.textContent = `Total: ${this.dinero(detalle.total)}`;
    this.panel.classList.add('panel-abierto');
  }

  cerrar() {
    this.panel.classList.remove('panel-abierto');
  }
}
