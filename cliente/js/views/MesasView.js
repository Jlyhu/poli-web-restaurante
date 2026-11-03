/** MesasView.js (VISTA) - Mesero: mapa de mesas libres y ocupadas. */
import { BaseView } from './BaseView.js';

export class MesasView extends BaseView {
  constructor() {
    super();
    this.grilla = document.querySelector('#grilla-mesas');
    this.contador = document.querySelector('#contador');
    this.btnActualizar = document.querySelector('#btn-actualizar');
  }

  alActualizar(cb) { this.btnActualizar.addEventListener('click', cb); }

  mostrarMesas(mesas) {
    const libres = mesas.filter((m) => m.disponible).length;
    this.contador.textContent = `${libres} libre(s) de ${mesas.length}`;
    this.grilla.innerHTML = '';
    for (const m of mesas) {
      const div = document.createElement('div');
      div.className = `tarjeta-mesa ${m.disponible ? 'mesa-libre' : 'mesa-ocupada'}`;
      div.innerHTML = '<strong></strong><span></span>';
      div.querySelector('strong').textContent = `Mesa ${m.numero}`;
      div.querySelector('span').textContent = m.disponible ? 'Libre' : `Ocupada · pedido ${m.id_pedido_activo}`;
      this.grilla.appendChild(div);
    }
  }
}
