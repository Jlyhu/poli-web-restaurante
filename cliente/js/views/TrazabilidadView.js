/** TrazabilidadView.js (VISTA) - HU-15. Tabla de pedidos con fechas y línea de tiempo del pedido elegido. */
import { BaseView } from './BaseView.js';

export class TrazabilidadView extends BaseView {
  constructor() {
    super();
    this.inputBuscar = document.querySelector('#buscar-pedido');
    this.selectEstado = document.querySelector('#filtro-estado');
    this.selectTipo = document.querySelector('#filtro-tipo');
    this.btnActualizar = document.querySelector('#btn-actualizar');
    this.resumen = document.querySelector('#resumen');
    this.tbody = document.querySelector('#tabla-pedidos tbody');
    this.listaEventos = document.querySelector('#panel-eventos');
    this.datos = document.querySelector('#panel-datos');
  }

  alFiltrar(cb) {
    this.btnActualizar.addEventListener('click', cb);
    this.selectEstado.addEventListener('change', cb);
    this.selectTipo.addEventListener('change', cb);
    this.inputBuscar.addEventListener('input', cb);
  }

  alVerTrazabilidad(cb) {
    this.tbody.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-id]');
      if (b) cb(Number(b.dataset.id));
    });
  }

  filtros() {
    return { estado: this.selectEstado.value, tipo: this.selectTipo.value, numero: this.inputBuscar.value.trim() };
  }

  mostrarResumen(pedidos) {
    const contar = (e) => pedidos.filter((p) => p.estado === e).length;
    const datos = [
      ['Pedidos', pedidos.length],
      ['Activos', contar('PENDIENTE') + contar('EN PREPARACION') + contar('LISTO')],
      ['Entregados', contar('ENTREGADO')],
      ['Cancelados', contar('CANCELADO')],
    ];
    this.resumen.innerHTML = '';
    for (const [texto, valor] of datos) {
      const div = document.createElement('div');
      div.className = 'tarjeta-dato';
      div.innerHTML = '<span></span><strong></strong>';
      div.querySelector('span').textContent = texto;
      div.querySelector('strong').textContent = valor;
      this.resumen.appendChild(div);
    }
  }

  mostrarPedidos(pedidos) {
    this.tbody.innerHTML = '';
    if (pedidos.length === 0) { this.filaVacia(this.tbody, 9, 'No hay pedidos con ese filtro.'); return; }
    for (const p of pedidos) {
      const tr = document.createElement('tr');
      const atiende = p.nombreMesero ?? p.nombreRepartidor ?? 'Sin asignar';
      tr.append(this.celda(p.idPedido), this.celda(p.destino()), this.celda(atiende),
        this.celda(this.badge(p.estado)), this.celda(this.fecha(p.creado)),
        this.celda(this.fecha(p.actualizado)), this.celda(p.minutos ?? '—'),
        this.celda(p.pagado ? this.badge('PAGADO') : '—'),
        this.celda(this.boton('Ver trazabilidad', 'btn-editar', { id: p.idPedido })));
      this.tbody.appendChild(tr);
    }
  }

  /** Llena la parte del panel propia de HU-15 (el resto lo llena DetallePanelView). */
  mostrarTrazabilidad(p) {
    this.listaEventos.innerHTML = '';
    for (const ev of p.eventos) {
      const li = document.createElement('li');
      li.innerHTML = '<strong></strong><span></span>';
      li.querySelector('strong').textContent = ev.evento;
      li.querySelector('span').textContent = this.fecha(ev.fecha);
      this.listaEventos.appendChild(li);
    }
    const filas = [
      ['Estado actual', p.estado],
      ['Tipo', p.tipo],
      ['Mesero', p.nombreMesero ?? '—'],
      ['Repartidor', p.nombreRepartidor ?? '—'],
      ['Cliente', p.cliente.nombre ?? '—'],
      ['Tiempo abierto', p.minutos != null ? `${p.minutos} min` : '—'],
      ['Pago', p.pagado ? `${p.metodoPago} · ${this.fecha(p.fechaPago)}` : 'Sin pago'],
    ];
    this.datos.innerHTML = '';
    for (const [k, v] of filas) {
      const dt = document.createElement('dt'); dt.textContent = k;
      const dd = document.createElement('dd'); dd.textContent = v;
      this.datos.append(dt, dd);
    }
  }
}
