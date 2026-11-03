/**
 * app-preparacion.js
 * Punto de arranque de HU-09.
 */
import { PedidoModel } from './models/PedidoModel.js';
import { DetallePedidoModel } from './models/DetallePedidoModel.js';
import { PersonalModel } from './models/PersonalModel.js';
import { PreparacionView } from './views/PreparacionView.js';
import { DetallePanelView } from './views/DetallePanelView.js';
import { PreparacionController } from './controllers/PreparacionController.js';

new PreparacionController(
  new PedidoModel(),
  new DetallePedidoModel(),
  new PersonalModel(),
  new PreparacionView(),
  new DetallePanelView()
).iniciar();
