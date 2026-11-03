/**
 * app-estado-pedido.js
 * Punto de arranque de HU-05, HU-06 y HU-07: crea Modelo, Vista y Controlador y los conecta.
 */
import { SeguimientoModel } from './models/SeguimientoModel.js';
import { DetallePedidoModel } from './models/DetallePedidoModel.js';
import { EstadoPedidoView } from './views/EstadoPedidoView.js';
import { DetallePanelView } from './views/DetallePanelView.js';
import { EstadoPedidoController } from './controllers/EstadoPedidoController.js';

new EstadoPedidoController(
  new SeguimientoModel(),
  new DetallePedidoModel(),
  new EstadoPedidoView(),
  new DetallePanelView()
).iniciar();
