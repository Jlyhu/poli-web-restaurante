/**
 * app-pendientes.js
 * Punto de arranque de HU-08.
 */
import { PedidoModel } from './models/PedidoModel.js';
import { DetallePedidoModel } from './models/DetallePedidoModel.js';
import { PendientesView } from './views/PendientesView.js';
import { DetallePanelView } from './views/DetallePanelView.js';
import { PendientesController } from './controllers/PendientesController.js';

new PendientesController(
  new PedidoModel(),
  new DetallePedidoModel(),
  new PendientesView(),
  new DetallePanelView()
).iniciar();
