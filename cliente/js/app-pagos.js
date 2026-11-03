/** app-pagos.js — Punto de arranque de "Ver pedidos" y "Registrar pago" (Cajero). */
import { SeguimientoModel } from './models/SeguimientoModel.js';
import { CajaModel } from './models/CajaModel.js';
import { PagosView } from './views/PagosView.js';
import { PagosController } from './controllers/PagosController.js';

new PagosController(new SeguimientoModel(), new CajaModel(), new PagosView()).iniciar();
