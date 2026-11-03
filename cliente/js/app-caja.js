/** app-caja.js — Punto de arranque de "Gestionar caja" (Cajero). */
import { CajaModel } from './models/CajaModel.js';
import { CajaView } from './views/CajaView.js';
import { CajaController } from './controllers/CajaController.js';

new CajaController(new CajaModel(), new CajaView()).iniciar();
