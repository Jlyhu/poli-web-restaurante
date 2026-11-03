/** DetallePedidoModel.js (MODELO). HU-03 productos del pedido, HU-04 observaciones, HU-08 detalle. */
import { ENDPOINTS } from '../config.js';
import { peticion } from './Http.js';
import { DetallePedido } from './DetallePedido.js';

export class DetallePedidoModel {
  /** → GET /getDetallePedidoConProducto/<id>   Devuelve { renglones: DetallePedido[], total } */
  async listar(idPedido) {
    const datos = await peticion(`${ENDPOINTS.detallePedidoConProducto}/${idPedido}`);
    return { renglones: (datos.renglones ?? []).map(DetallePedido.desdeJSON), total: Number(datos.total ?? 0) };
  }

  /** → POST /insertDetallePedido  (el servidor valida: pedido PENDIENTE, producto disponible, unidades) */
  agregar(idPedido, idProducto, cantidad, notas) {
    return peticion(ENDPOINTS.insertarDetallePedido, 'POST', {
      Pedido_id_pedido: idPedido,
      Producto_idProducto: idProducto,
      cantidad,
      notas: notas || null,
    });
  }

  /** → PUT /updateDetallePedido/<id> */
  cambiarCantidad(idDetalle, cantidad) {
    return peticion(`${ENDPOINTS.actualizarDetallePedido}/${idDetalle}`, 'PUT', { cantidad });
  }

  /** → DELETE /deleteDetallePedido/<id> */
  quitar(idDetalle) {
    return peticion(`${ENDPOINTS.eliminarDetallePedido}/${idDetalle}`, 'DELETE');
  }
}
