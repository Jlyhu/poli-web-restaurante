/**
 * EstadoPedidoView.js (VISTA) - HU-05, HU-06, HU-07.
 * Dibuja la tabla de pedidos con su estado y los botones Entregar / Cancelar.
 * No decide nada: avisa al Controlador con callbacks.
 */
import { BaseView } from './BaseView.js';

export class EstadoPedidoView extends BaseView {
  constructor() {
    super();
    this.inputBuscar = document.querySelector('#buscar-pedido');
    this.selectEstado = document.querySelector('#filtro-estado');
    this.checkMios = document.querySelector('#solo-mios');
    this.btnActualizar = document.querySelector('#btn-actualizar');
    this.contador = document.querySelector('#contador');
    this.tbody = document.querySelector('#tabla-pedidos tbody');
  }

  /** cb() cuando cambia cualquier filtro o se pulsa Actualizar */
  alFiltrar(cb) {
    this.btnActualizar.addEventListener('click', cb);
    this.selectEstado.addEventListener('change', cb);
    this.checkMios.addEventListener('change', cb);
    this.inputBuscar.addEventListener('input', cb);
  }

  /** cb(accion, idPedido) con accion = 'detalle' | 'entregar' | 'cancelar' */
  alAccionar(cb) {
    // Delegación de eventos: un solo listener en el tbody atiende todos los botones
    this.tbody.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-accion]');
      if (!b) return;
      // Cancelar pide una segunda pulsación para confirmar (sin ventanas emergentes)
      if (b.dataset.accion === 'cancelar' && b.dataset.confirmar !== 'si') {
        b.dataset.confirmar = 'si';
        b.textContent = '¿Confirmar cancelación?';
        setTimeout(() => { b.dataset.confirmar = ''; b.textContent = 'Cancelar'; }, 4000);
        return;
      }
      cb(b.dataset.accion, Number(b.dataset.id));
    });
  }

  filtros() {
    const estado = this.selectEstado.value;
    return {
      estado: estado === 'activos' ? '' : estado,
      activos: estado === 'activos',
      soloMios: this.checkMios.checked,
      numero: this.inputBuscar.value.trim(),
    };
  }

  /** Si quien inició sesión no es mesero, la casilla "Solo mis pedidos" no aplica. */
  habilitarSoloMios(habilitar) {
    this.checkMios.disabled = !habilitar;
    this.checkMios.parentElement.classList.toggle('oculto', !habilitar);
  }

  mostrarPedidos(pedidos) {
    this.contador.textContent = `${pedidos.length} pedido(s)`;
    this.tbody.innerHTML = '';
    if (pedidos.length === 0) { this.filaVacia(this.tbody, 7, 'No hay pedidos con ese filtro.'); return; }
    for (const p of pedidos) {
      const acciones = document.createElement('div');
      acciones.className = 'acciones-fila';
      acciones.append(this.boton('Ver detalle', 'btn-editar', { accion: 'detalle', id: p.idPedido }));
      if (p.sePuedeEntregar()) {
        acciones.append(this.boton('Entregar', 'btn-primario', { accion: 'entregar', id: p.idPedido }));
      }
      if (p.sePuedeCancelar()) {
        acciones.append(this.boton('Cancelar', 'btn-cancelar', { accion: 'cancelar', id: p.idPedido }));
      }
      const tr = document.createElement('tr');
      tr.append(this.celda(p.idPedido), this.celda(p.destino()), this.celda(this.badge(p.estado)),
        this.celda(this.fecha(p.creado)), this.celda(this.fecha(p.actualizado)),
        this.celda(this.dinero(p.total)), this.celda(acciones));
      this.tbody.appendChild(tr);
    }
  }
}
