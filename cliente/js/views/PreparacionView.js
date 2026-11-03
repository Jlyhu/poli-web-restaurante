/** PreparacionView.js (VISTA). HU-09: pedidos pendientes y en preparación con sus botones de avance. */
import { BaseView } from './BaseView.js';

export class PreparacionView extends BaseView {
  constructor() {
    super();
    this.selectCocinero = document.querySelector('#select-cocinero');
    this.btnActualizar = document.querySelector('#btn-actualizar');
    this.tbodyPendientes = document.querySelector('#tabla-pendientes tbody');
    this.tbodyPreparacion = document.querySelector('#tabla-preparacion tbody');
  }

  alActualizar(cb) { this.btnActualizar.addEventListener('click', cb); }

  /** cb(accion, idPedido) con accion = 'detalle' | 'iniciar' | 'listo' */
  alAccionar(cb) {
    for (const tbody of [this.tbodyPendientes, this.tbodyPreparacion]) {
      tbody.addEventListener('click', (e) => {
        const b = e.target.closest('button[data-accion]');
        if (b) cb(b.dataset.accion, Number(b.dataset.id));
      });
    }
  }

  cocineroSeleccionado() {
    return this.selectCocinero.value ? Number(this.selectCocinero.value) : null;
  }

  mostrarCocineros(cocineros, fijo) {
    this.selectCocinero.innerHTML = '<option value="">Seleccione el cocinero responsable</option>';
    for (const c of cocineros) {
      const op = document.createElement('option');
      op.value = c.id;
      op.textContent = c.nombre;
      this.selectCocinero.appendChild(op);
    }
    if (fijo) {                       // el cocinero que inició sesión: queda elegido y bloqueado
      this.selectCocinero.value = String(fijo);
      this.selectCocinero.disabled = true;
    }
  }

  #pintar(tbody, pedidos, textoBoton, accion, vacio) {
    tbody.innerHTML = '';
    if (pedidos.length === 0) { this.filaVacia(tbody, 4, vacio); return; }
    for (const p of pedidos) {
      const tr = document.createElement('tr');
      const acciones = document.createElement('div');
      acciones.append(
        this.boton('Ver detalle', 'btn-editar', { accion: 'detalle', id: p.idPedido }),
        ' ',
        this.boton(textoBoton, 'btn-primario', { accion, id: p.idPedido })
      );
      tr.append(this.celda(p.idPedido), this.celda(`Mesa ${p.numeroMesa ?? '—'}`),
        this.celda(this.fecha(p.creado)), this.celda(acciones));
      tbody.appendChild(tr);
    }
  }

  mostrarPendientes(pedidos) {
    this.#pintar(this.tbodyPendientes, pedidos, 'Iniciar preparación', 'iniciar', 'No hay pedidos pendientes.');
  }

  mostrarEnPreparacion(pedidos) {
    this.#pintar(this.tbodyPreparacion, pedidos, 'Marcar listo', 'listo', 'No hay pedidos en preparación.');
  }
}
