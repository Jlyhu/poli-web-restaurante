/** ReportesView.js (VISTA). HU-14: filtros por fecha, resumen de ventas y tiempos de preparación. */
import { BaseView } from './BaseView.js';

export class ReportesView extends BaseView {
  constructor() {
    super();
    this.selectAdmin = document.querySelector('#select-administrador');
    this.desde = document.querySelector('#fecha-desde');
    this.hasta = document.querySelector('#fecha-hasta');
    this.btnConsultar = document.querySelector('#btn-consultar');
    this.btnLimpiar = document.querySelector('#btn-limpiar');
    this.resultados = document.querySelector('#resultados');
  }

  alConsultar(cb) { this.btnConsultar.addEventListener('click', cb); }
  alLimpiar(cb) { this.btnLimpiar.addEventListener('click', cb); }

  filtros() {
    return {
      administrador: this.selectAdmin.value ? Number(this.selectAdmin.value) : null,
      desde: this.desde.value,
      hasta: this.hasta.value,
    };
  }

  mostrarAdministradores(admins, fijo) {
    this.selectAdmin.innerHTML = '<option value="">Seleccione el administrador</option>';
    for (const a of admins) {
      const op = document.createElement('option');
      op.value = a.id;
      op.textContent = a.nombre;
      this.selectAdmin.appendChild(op);
    }
    if (fijo) {                       // el administrador que inició sesión: queda elegido y bloqueado
      this.selectAdmin.value = String(fijo);
      this.selectAdmin.disabled = true;
    }
  }

  limpiar() {
    this.desde.value = '';
    this.hasta.value = '';
    this.resultados.classList.add('oculto');
  }

  #llenar(selector, filas) {
    const tbody = document.querySelector(`${selector} tbody`);
    tbody.innerHTML = '';
    if (filas.length === 0) { this.filaVacia(tbody, document.querySelectorAll(`${selector} th`).length, 'Sin datos para el rango elegido.'); return; }
    for (const celdas of filas) {
      const tr = document.createElement('tr');
      tr.append(...celdas.map((c) => this.celda(c)));
      tbody.appendChild(tr);
    }
  }

  mostrar(ventas, tiempos) {
    this.resultados.classList.remove('oculto');

    document.querySelector('#kpi-total').textContent = this.dinero(ventas.total);
    document.querySelector('#kpi-pagos').textContent = ventas.cantidad_pagos;
    this.#llenar('#tabla-metodos', ventas.por_metodo.map((m) => [m.metodo, this.dinero(m.total)]));
    this.#llenar('#tabla-pagos', ventas.pagos.map((p) =>
      [p.id_pago, p.Pedido_id_pedido, p.metodo_pago ?? '—', this.fecha(p.fecha_pago), this.dinero(p.monto)]));

    document.querySelector('#kpi-promedio').textContent =
      tiempos.promedio_minutos === null ? '—' : `${tiempos.promedio_minutos} min`;
    document.querySelector('#kpi-pedidos').textContent = tiempos.cantidad_pedidos;
    this.#llenar('#tabla-tiempos', tiempos.pedidos.map((p) =>
      [p.id_pedido, p.estado, this.fecha(p.fecha_creacion), this.fecha(p.fecha_ultima_actualizacion), `${p.minutos} min`]));
  }
}
