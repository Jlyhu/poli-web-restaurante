/** ProductosPedidoView.js (VISTA). HU-03 y HU-04: productos y observaciones de un pedido. */
import { BaseView } from './BaseView.js';

export class ProductosPedidoView extends BaseView {
  constructor() {
    super();
    this.selectPedido = document.querySelector('#select-pedido');
    this.selectProducto = document.querySelector('#select-producto');
    this.inputCantidad = document.querySelector('#input-cantidad');
    this.inputNotas = document.querySelector('#input-notas');
    this.btnAgregar = document.querySelector('#btn-agregar');
    this.aviso = document.querySelector('#aviso-estado');
    this.tbody = document.querySelector('#tabla-detalle tbody');
    this.total = document.querySelector('#total-pedido');
  }

  // ----- eventos -----
  alElegirPedido(cb) { this.selectPedido.addEventListener('change', () => cb(this.pedidoSeleccionado())); }

  alAgregar(cb) {
    this.btnAgregar.addEventListener('click', () => cb({
      idProducto: this.selectProducto.value ? Number(this.selectProducto.value) : null,
      cantidad: Number(this.inputCantidad.value),
      notas: this.inputNotas.value.trim(),
    }));
  }

  alCambiarCantidad(cb) {
    this.tbody.addEventListener('change', (e) => {
      const input = e.target.closest('input[data-id]');
      if (input) cb(Number(input.dataset.id), Number(input.value));
    });
  }

  alQuitar(cb) {
    this.tbody.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-quitar]');
      if (b) cb(Number(b.dataset.quitar));
    });
  }

  // ----- lectura -----
  pedidoSeleccionado() {
    return this.selectPedido.value ? Number(this.selectPedido.value) : null;
  }

  // ----- pintado -----
  mostrarPedidos(pedidos, elegido) {
    this.selectPedido.innerHTML = '<option value="">Seleccione un pedido</option>';
    for (const p of pedidos) {
      const op = document.createElement('option');
      op.value = p.idPedido;
      op.textContent = `Pedido ${p.idPedido} · Mesa ${p.numeroMesa ?? '—'} · ${p.estado}`;
      this.selectPedido.appendChild(op);
    }
    if (elegido) this.selectPedido.value = String(elegido);
  }

  mostrarProductos(productos) {
    this.selectProducto.innerHTML = '<option value="">Seleccione un producto</option>';
    for (const p of productos) {
      const op = document.createElement('option');
      op.value = p.idProducto;
      op.textContent = `${p.nombre} — ${this.dinero(p.precio)} (${p.cantidad} disp.)`;
      this.selectProducto.appendChild(op);
    }
  }

  /** Aviso fijo (p. ej. "el pedido ya no está pendiente"). Con null se oculta. */
  mostrarAviso(texto) {
    this.aviso.textContent = texto ?? '';
    this.aviso.classList.toggle('oculto', !texto);
  }

  /** Habilita o bloquea el formulario y las acciones según el estado del pedido. */
  permitirEdicion(permitir) {
    [this.selectProducto, this.inputCantidad, this.inputNotas, this.btnAgregar]
      .forEach((el) => { el.disabled = !permitir; });
  }

  limpiarFormulario() {
    this.selectProducto.value = '';
    this.inputCantidad.value = 1;
    this.inputNotas.value = '';
  }

  mostrarDetalle(detalle, editable) {
    this.tbody.innerHTML = '';
    if (!detalle || detalle.renglones.length === 0) {
      this.filaVacia(this.tbody, 6, detalle ? 'El pedido aún no tiene productos.' : 'Seleccione un pedido.');
      this.total.textContent = '';
      return;
    }
    for (const r of detalle.renglones) {
      const tr = document.createElement('tr');
      const cantidad = document.createElement('input');
      cantidad.type = 'number';
      cantidad.min = 1;
      cantidad.step = 1;
      cantidad.value = r.cantidad;
      cantidad.dataset.id = r.idDetalle;
      cantidad.disabled = !editable;
      const quitar = this.boton('Quitar', 'btn-editar', { quitar: r.idDetalle });
      quitar.disabled = !editable;
      tr.append(this.celda(r.nombre), this.celda(cantidad), this.celda(r.notas || '—'),
        this.celda(this.dinero(r.precio)), this.celda(this.dinero(r.subtotal)), this.celda(quitar));
      this.tbody.appendChild(tr);
    }
    this.total.textContent = `Total: ${this.dinero(detalle.total)}`;
  }
}
