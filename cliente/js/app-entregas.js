/** app-entregas.js — Punto de arranque de las pantallas del Repartidor. */
import { SeguimientoModel } from './models/SeguimientoModel.js';
import { DetallePedidoModel } from './models/DetallePedidoModel.js';
import { EntregasView } from './views/EntregasView.js';
import { DetallePanelView } from './views/DetallePanelView.js';
import { EntregasController } from './controllers/EntregasController.js';

new EntregasController(
  new SeguimientoModel(),
  new DetallePedidoModel(),
  new EntregasView(),
  new DetallePanelView()
).iniciar();
