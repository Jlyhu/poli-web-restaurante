/** CajaModel.js (MODELO). Cajero: abrir y cerrar caja, registrar pagos. Entidades Caja, Pago, Cajero. */
import { ENDPOINTS } from '../config.js';
import { peticion } from './Http.js';

export class CajaModel {
  /** → GET /getCajaAbierta?cajero=<id>   Devuelve la caja abierta con sus pagos, o null. */
  cajaAbierta(idCajero) {
    return peticion(`${ENDPOINTS.cajaAbierta}?cajero=${idCajero}`);
  }

  /** → POST /abrirCaja */
  abrir(idCajero, montoInicial) {
    return peticion(ENDPOINTS.abrirCaja, 'POST', { Cajero_id_cajero: idCajero, monto_inicial: montoInicial });
  }

  /** → PUT /cerrarCaja/<id>  (ya existía) */
  cerrar(idCaja, montoFinal) {
    return peticion(`${ENDPOINTS.cerrarCaja}/${idCaja}`, 'PUT', { monto_final: montoFinal });
  }

  /** → POST /registrarPagoPedido  (el servidor calcula el monto con el detalle del pedido) */
  registrarPago(idPedido, idCajero, metodo) {
    return peticion(ENDPOINTS.registrarPagoPedido, 'POST', {
      Pedido_id_pedido: idPedido,
      Cajero_id_cajero: idCajero,
      metodo_pago: metodo,
    });
  }
}
