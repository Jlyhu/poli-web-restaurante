/** app-trazabilidad.js — Punto de arranque de HU-15. */
import { SeguimientoModel } from './models/SeguimientoModel.js';
import { DetallePedidoModel } from './models/DetallePedidoModel.js';
import { TrazabilidadView } from './views/TrazabilidadView.js';
import { DetallePanelView } from './views/DetallePanelView.js';
import { TrazabilidadController } from './controllers/TrazabilidadController.js';

new TrazabilidadController(
  new SeguimientoModel(),
  new DetallePedidoModel(),
  new TrazabilidadView(),
  new DetallePanelView()
).iniciar();
