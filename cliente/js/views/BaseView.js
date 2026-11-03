/** BaseView.js (VISTA base). Avisos, fechas, dinero y estados: lo comparten todas las vistas de pedidos. */
const DINERO = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 });

const CLASE_ESTADO = {
  'PENDIENTE': 'badge-amarillo',
  'EN PREPARACION': 'badge-azul',
  'LISTO': 'badge-verde',
  'ENTREGADO': 'badge-gris',
  'CANCELADO': 'badge-rojo',
  'PAGADO': 'badge-verde',
};

export class BaseView {
  /** Aviso flotante que desaparece solo. tipo: 'exito' | 'error' */
  mostrarMensaje(texto, tipo = 'exito') {
    const aviso = document.createElement('div');
    aviso.className = `mensaje mensaje-${tipo}`;
    aviso.textContent = texto;
    document.body.appendChild(aviso);
    setTimeout(() => aviso.remove(), 4000);
  }

  dinero(valor) {
    return DINERO.format(valor ?? 0);
  }

  /** '2026-11-02 18:35:00' → '02/11/2026 18:35' */
  fecha(texto) {
    if (!texto) return '—';
    const [dia, hora] = texto.replace('T', ' ').split(' ');
    const [a, m, d] = dia.split('-');
    return `${d}/${m}/${a}${hora ? ' ' + hora.slice(0, 5) : ''}`;
  }

  /** Etiqueta de color para un estado de pedido. */
  badge(estado) {
    const span = document.createElement('span');
    span.className = `badge ${CLASE_ESTADO[estado] ?? 'badge-gris'}`;
    span.textContent = estado;
    return span;
  }

  celda(contenido) {
    const td = document.createElement('td');
    if (contenido instanceof Node) td.appendChild(contenido);
    else td.textContent = contenido ?? '';
    return td;
  }

  boton(texto, clase, datos = {}) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = clase;
    b.textContent = texto;
    Object.entries(datos).forEach(([k, v]) => { b.dataset[k] = v; });
    return b;
  }

  filaVacia(tbody, columnas, texto) {
    tbody.innerHTML = '';
    const tr = document.createElement('tr');
    const td = this.celda(texto);
    td.colSpan = columnas;
    td.className = 'fila-vacia';
    tr.appendChild(td);
    tbody.appendChild(tr);
  }
}
