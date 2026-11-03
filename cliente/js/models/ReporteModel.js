/** ReporteModel.js (MODELO). HU-14: reportes de ventas y de tiempos de preparación. */
import { ENDPOINTS } from '../config.js';
import { peticion } from './Http.js';

export class ReporteModel {
  #consulta({ administrador, desde, hasta }) {
    const p = new URLSearchParams({ administrador });
    if (desde) p.set('desde', desde);
    if (hasta) p.set('hasta', hasta);
    return `?${p}`;
  }

  /** → GET /reporteVentas  { total, cantidad_pagos, por_metodo[], pagos[] } */
  ventas(filtros) {
    return peticion(ENDPOINTS.reporteVentas + this.#consulta(filtros));
  }

  /** → GET /reporteTiempos  { promedio_minutos, cantidad_pedidos, pedidos[] } */
  tiempos(filtros) {
    return peticion(ENDPOINTS.reporteTiempos + this.#consulta(filtros));
  }
}
