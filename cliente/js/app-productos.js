/**
 * app-productos.js
 * Punto de arranque de HU-11. Ensambla Modelo, Vista y Controlador.
 */
import { ProductoModel } from './models/ProductoModel.js';
import { CategoriaModel } from './models/CategoriaModel.js';
import { ProductoView } from './views/ProductoView.js';
import { ProductoController } from './controllers/ProductoController.js';

const controlador = new ProductoController(
    new ProductoModel(),
    new CategoriaModel(),
    new ProductoView()
);

controlador.iniciar();