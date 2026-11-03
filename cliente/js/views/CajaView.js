/** CajaView.js (VISTA) - Cajero: abrir caja, ver lo recaudado y cerrarla. */
import { BaseView } from './BaseView.js';

export class CajaView extends BaseView {
  constructor() {
    super();
    this.seccionAbrir = document.querySelector('#seccion-abrir');
    this.seccionAbierta = document.querySelector('#seccion-abierta');
    this.formAbrir = document.querySelector('#form-abrir');
    this.formCerrar = document.querySelector('#form-cerrar');
    this.inputInicial = document.querySelector('#input-monto-inicial');
    this.inputFinal = document.querySelector('#input-monto-final');
    this.textoCaja = document.querySelector('#texto-caja');
    this.resumen = document.querySelector('#resumen-caja');
    this.tbodyPagos = document.querySelector('#tabla-pagos tbody');
    this.diferencia = document.querySelector('#diferencia');
    this.esperado = 0;
    this.inputFinal.addEventListener('input', () => this.#mostrarDiferencia());
  }

  alAbrir(cb) {
    this.formAbrir.addEventListener('submit', (e) => { e.preventDefault(); cb(Number(this.inputInicial.value)); });
  }

  alCerrar(cb) {
    this.formCerrar.addEventListener('submit', (e) => { e.preventDefault(); cb(Number(this.inputFinal.value)); });
  }

  mostrarSinCaja() {
    this.seccionAbierta.classList.add('oculto');
    this.seccionAbrir.classList.remove('oculto');
    this.formAbrir.reset();
  }

  mostrarCaja(caja) {
    this.seccionAbrir.classList.add('oculto');
    this.seccionAbierta.classList.remove('oculto');
    this.esperado = caja.esperado;
    this.textoCaja.textContent = `Caja ${caja.id_caja} abierta desde ${this.fecha(caja.fecha_apertura)}`;

    this.resumen.innerHTML = '';
    for (const [texto, valor] of [['Base inicial', caja.monto_inicial], ['Recaudado', caja.recaudado],
      ['Debe haber en caja', caja.esperado], ['Pagos', caja.pagos.length]]) {
      const div = document.createElement('div');
      div.className = 'tarjeta-dato';
      div.innerHTML = '<span></span><strong></strong>';
      div.querySelector('span').textContent = texto;
      div.querySelector('strong').textContent = texto === 'Pagos' ? valor : this.dinero(valor);
      this.resumen.appendChild(div);
    }

    this.tbodyPagos.innerHTML = '';
    if (caja.pagos.length === 0) this.filaVacia(this.tbodyPagos, 5, 'Aún no hay pagos en esta caja.');
    for (const p of caja.pagos) {
      const tr = document.createElement('tr');
      tr.append(this.celda(p.id_pago), this.celda(p.Pedido_id_pedido), this.celda(p.metodo_pago),
        this.celda(this.fecha(p.fecha_pago)), this.celda(this.dinero(p.monto)));
      this.tbodyPagos.appendChild(tr);
    }
    this.inputFinal.value = '';
    this.#mostrarDiferencia();
  }

  #mostrarDiferencia() {
    if (this.inputFinal.value === '') {
      this.diferencia.textContent = `Debería contar ${this.dinero(this.esperado)}.`;
      return;
    }
    const dif = Number(this.inputFinal.value) - this.esperado;
    this.diferencia.textContent = dif === 0 ? 'La caja cuadra exacto.'
      : dif > 0 ? `Sobran ${this.dinero(dif)}.` : `Faltan ${this.dinero(-dif)}.`;
  }
}
