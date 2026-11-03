/** PagosView.js (VISTA) - Cajero: pedidos por cobrar, en curso y pagados. */
import { BaseView } from './BaseView.js';

export class PagosView extends BaseView {
  constructor() {
    super();
    this.aviso = document.querySelector('#aviso-caja');
    this.selectMetodo = document.querySelector('#select-metodo');
    this.btnActualizar = document.querySelector('#btn-actualizar');
    this.tbodyPorCobrar = document.querySelector('#tabla-por-cobrar tbody');
    this.tbodyEnCurso = document.querySelector('#tabla-en-curso tbody');
    this.tbodyPagados = document.querySelector('#tabla-pagados tbody');
  }

  alActualizar(cb) { this.btnActualizar.addEventListener('click', cb); }

  /** cb(idPedido, metodo) */
  alCobrar(cb) {
    this.tbodyPorCobrar.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-id]');
      if (b) cb(Number(b.dataset.id), this.selectMetodo.value);
    });
  }

  mostrarAvisoCaja(sinCaja) { this.aviso.classList.toggle('oculto', !sinCaja); }

  mostrarPorCobrar(pedidos, hayCaja) {
    this.tbodyPorCobrar.innerHTML = '';
    if (pedidos.length === 0) { this.filaVacia(this.tbodyPorCobrar, 5, 'No hay pedidos por cobrar.'); return; }
    for (const p of pedidos) {
      const b = this.boton('Registrar pago', 'btn-primario', { id: p.idPedido });
      b.disabled = !hayCaja;
      const tr = document.createElement('tr');
      tr.append(this.celda(p.idPedido), this.celda(p.destino()), this.celda(this.fecha(p.actualizado)),
        this.celda(this.dinero(p.total)), this.celda(b));
      this.tbodyPorCobrar.appendChild(tr);
    }
  }

  mostrarEnCurso(pedidos) {
    this.tbodyEnCurso.innerHTML = '';
    if (pedidos.length === 0) { this.filaVacia(this.tbodyEnCurso, 5, 'No hay pedidos en curso.'); return; }
    for (const p of pedidos) {
      const tr = document.createElement('tr');
      tr.append(this.celda(p.idPedido), this.celda(p.destino()), this.celda(this.badge(p.estado)),
        this.celda(this.fecha(p.creado)), this.celda(this.dinero(p.total)));
      this.tbodyEnCurso.appendChild(tr);
    }
  }

  mostrarPagados(pedidos) {
    this.tbodyPagados.innerHTML = '';
    if (pedidos.length === 0) { this.filaVacia(this.tbodyPagados, 5, 'Aún no hay pagos.'); return; }
    for (const p of pedidos) {
      const tr = document.createElement('tr');
      tr.append(this.celda(p.idPedido), this.celda(p.destino()), this.celda(p.metodoPago),
        this.celda(this.fecha(p.fechaPago)), this.celda(this.dinero(p.total)));
      this.tbodyPagados.appendChild(tr);
    }
  }
}
