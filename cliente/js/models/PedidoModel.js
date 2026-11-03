/** PedidoModel.js (MODELO). HU-02 crear pedido, HU-08 pendientes, HU-09 cambio de estado. */
import { ENDPOINTS } from '../config.js';
import { peticion } from './Http.js';
import { Pedido } from './Pedido.js';

export class PedidoModel {
  /** Mesas con `disponible` (false si tienen un pedido activo). → GET /getMesasDisponibilidad */
  mesasDisponibilidad() {
    return peticion(ENDPOINTS.listarMesasDisponibilidad);
  }

  /** @param {{estado?: string, activos?: boolean}} filtros  → GET /getPedidosConMesa */
  async listar({ estado, activos } = {}) {
    const parametros = new URLSearchParams();
    if (estado) parametros.set('estado', estado);
    if (activos) parametros.set('activos', '1');
    const consulta = parametros.toString() ? `?${parametros}` : '';
    const datos = await peticion(ENDPOINTS.listarPedidosConMesa + consulta);
    return (datos ?? []).map(Pedido.desdeJSON);
  }

  /** Crea el pedido PENDIENTE de una mesa. → POST /crearPedidoMesa */
  async crear(idMesa, idMesero = null) {
    const cuerpo = { Mesa_id_mesa: idMesa };
    if (idMesero) cuerpo.Mesero_id_mesero = idMesero;
    return Pedido.desdeJSON(await peticion(ENDPOINTS.crearPedidoMesa, 'POST', cuerpo));
  }

  /** PENDIENTE → EN PREPARACION → LISTO → ENTREGADO. → PUT /cambiarEstadoPedido/<id> */
  cambiarEstado(idPedido, estado) {
    return peticion(`${ENDPOINTS.cambiarEstadoPedido}/${idPedido}`, 'PUT', { estado });
  }
}
