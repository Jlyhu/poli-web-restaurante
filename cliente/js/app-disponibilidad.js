/**
 * app-disponibilidad.js
 * Punto de arranque de HU-12. Reutiliza ProductoModel.
 */
import { ProductoModel } from './models/ProductoModel.js';
import { DisponibilidadView } from './views/DisponibilidadView.js';
import { DisponibilidadController } from './controllers/DisponibilidadController.js';

const controlador = new DisponibilidadController(
    new ProductoModel(),
    new DisponibilidadView()
);

controlador.iniciar();