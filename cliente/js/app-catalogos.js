/**
 * app-catalogos.js
 * Punto de arranque de HU-10. Ensambla los Modelos, la Vista y el Controlador.
 */
import { CategoriaModel } from './models/CategoriaModel.js';
import { MesaModel } from './models/MesaModel.js';
import { CatalogosView } from './views/CatalogosView.js';
import { CatalogosController } from './controllers/CatalogosController.js';

const controlador = new CatalogosController(
    new CategoriaModel(),
    new MesaModel(),
    new CatalogosView()
);

controlador.iniciar();