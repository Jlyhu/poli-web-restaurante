/** app-mesas.js — Punto de arranque de "Ver mesas" (Mesero). */
import { PedidoModel } from './models/PedidoModel.js';
import { MesasView } from './views/MesasView.js';
import { MesasController } from './controllers/MesasController.js';

new MesasController(new PedidoModel(), new MesasView()).iniciar();
