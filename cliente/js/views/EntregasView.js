/** EntregasView.js (VISTA) - Repartidor: una tarjeta por pedido con los datos de entrega. */
import { BaseView } from './BaseView.js';

export class EntregasView extends BaseView {
  constructor() {
    super();
    this.lista = document.querySelector('#lista-entregas');
    this.checkEntregados = document.querySelector('#ver-entregados');
    this.btnActualizar = document.querySelector('#btn-actualizar');
  }

  alActualizar(cb) {
    this.btnActualizar.addEventListener('click', cb);
    this.checkEntregados.addEventListener('change', cb);
  }

  /** cb(accion, idPedido) con accion = 'detalle' | 'entregar' */
  alAccionar(cb) {
    this.lista.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-accion]');
      if (b) cb(b.dataset.accion, Number(b.dataset.id));
    });
  }

  verEntregados() { return this.checkEntregados.checked; }

  mostrarEntregas(pedidos) {
    this.lista.innerHTML = '';
    if (pedidos.length === 0) {
      const p = document.createElement('p');
      p.className = 'contador';
      p.textContent = 'No tiene pedidos asignados por ahora.';
      this.lista.appendChild(p);
      return;
    }
    for (const p of pedidos) {
      const art = document.createElement('article');
      art.className = 'tarjeta-entrega';
      art.innerHTML = `
        <header><strong></strong></header>
        <dl class="datos-pedido">
          <dt>Cliente</dt><dd data-campo="nombre"></dd>
          <dt>Dirección</dt><dd data-campo="direccion"></dd>
          <dt>Teléfono</dt><dd data-campo="telefono"></dd>
          <dt>Total a cobrar</dt><dd data-campo="total"></dd>
          <dt>Creado</dt><dd data-campo="creado"></dd>
        </dl>
        <div class="acciones-fila"></div>`;
      art.querySelector('strong').textContent = `Pedido ${p.idPedido} `;
      art.querySelector('header').appendChild(this.badge(p.estado));
      art.querySelector('[data-campo="nombre"]').textContent = p.cliente.nombre ?? '—';
      art.querySelector('[data-campo="direccion"]').textContent = p.cliente.direccion ?? '—';
      art.querySelector('[data-campo="telefono"]').textContent = p.cliente.telefono ?? '—';
      art.querySelector('[data-campo="total"]').textContent = this.dinero(p.total);
      art.querySelector('[data-campo="creado"]').textContent = this.fecha(p.creado);

      const acciones = art.querySelector('.acciones-fila');
      acciones.appendChild(this.boton('Ver productos', 'btn-editar', { accion: 'detalle', id: p.idPedido }));
      if (p.sePuedeEntregar()) {
        acciones.appendChild(this.boton('Marcar entregado', 'btn-primario', { accion: 'entregar', id: p.idPedido }));
      } else if (p.estado !== 'ENTREGADO' && p.estado !== 'CANCELADO') {
        const espera = document.createElement('span');
        espera.className = 'nota-pie';
        espera.textContent = 'Esperando a que cocina lo marque LISTO';
        acciones.appendChild(espera);
      }
      this.lista.appendChild(art);
    }
  }
}
