/**
 * app-productos-pedido.js
 * Punto de arranque de HU-03 y HU-04. Reutiliza ProductoModel (HU-11/HU-12).
 */
import { PedidoModel } from './models/PedidoModel.js';
import { DetallePedidoModel } from './models/DetallePedidoModel.js';
import { ProductoModel } from './models/ProductoModel.js';
import { ProductosPedidoView } from './views/ProductosPedidoView.js';
import { ProductosPedidoController } from './controllers/ProductosPedidoController.js';

new ProductosPedidoController(
  new PedidoModel(),
  new DetallePedidoModel(),
  new ProductoModel(),
  new ProductosPedidoView()
).iniciar();
