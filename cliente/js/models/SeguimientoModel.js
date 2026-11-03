/** SeguimientoModel.js (MODELO). HU-05 estado, HU-06 entregar, HU-07 cancelar, HU-15 trazabilidad. */
import { ENDPOINTS } from '../config.js';
import { peticion } from './Http.js';
import { PedidoDetallado } from './PedidoDetallado.js';

export class SeguimientoModel {
  /**
   * → GET /getPedidosDetallados
   * @param {{estado?:string, activos?:boolean, mesero?:number, repartidor?:number, tipo?:string, sinPago?:boolean}} filtros
   */
  async listar(filtros = {}) {
    const parametros = new URLSearchParams();
    for (const [clave, valor] of Object.entries(filtros)) {
      if (valor === undefined || valor === null || valor === '' || valor === false) continue;
      parametros.set(clave, valor === true ? '1' : String(valor));
    }
    const consulta = parametros.toString() ? `?${parametros}` : '';
    const datos = await peticion(ENDPOINTS.listarPedidosDetallados + consulta);
    return (datos ?? []).map(PedidoDetallado.desdeJSON);
  }

  /** HU-05 → GET /getEstadoPedido/<id> */
  async estado(idPedido) {
    return PedidoDetallado.desdeJSON(await peticion(`${ENDPOINTS.estadoPedido}/${idPedido}`));
  }

  /** HU-15 → GET /getTrazabilidadPedido/<id> (incluye la lista de eventos con fecha) */
  async trazabilidad(idPedido) {
    return PedidoDetallado.desdeJSON(await peticion(`${ENDPOINTS.trazabilidadPedido}/${idPedido}`));
  }

  /** HU-06 → PUT /entregarPedido/<id>  (LISTO → ENTREGADO) */
  async entregar(idPedido) {
    return PedidoDetallado.desdeJSON(await peticion(`${ENDPOINTS.entregarPedido}/${idPedido}`, 'PUT'));
  }

  /** HU-07 → PUT /cancelarPedido/<id>  (PENDIENTE o EN PREPARACION → CANCELADO) */
  async cancelar(idPedido) {
    return PedidoDetallado.desdeJSON(await peticion(`${ENDPOINTS.cancelarPedido}/${idPedido}`, 'PUT'));
  }
}
