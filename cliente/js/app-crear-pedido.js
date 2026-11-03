/**
 * app-crear-pedido.js
 * Punto de arranque de HU-02: ensambla Modelo + Vista + Controlador.
 */
import { PedidoModel } from './models/PedidoModel.js';
import { CrearPedidoView } from './views/CrearPedidoView.js';
import { CrearPedidoController } from './controllers/CrearPedidoController.js';

new CrearPedidoController(new PedidoModel(), new CrearPedidoView()).iniciar();
