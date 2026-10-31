/**
 * app-usuarios.js
 * ---------------
 * Punto de arranque para la gestión de usuarios. Ensambla las tres
 * piezas del patrón MVC y pone la aplicación en marcha.
 */
import { UsuarioModel } from './models/UsuarioModel.js';
import { UsuarioView } from './views/UsuarioView.js';
import { UsuarioController } from './controllers/UsuarioController.js';

const modelo = new UsuarioModel();
const vista = new UsuarioView();
const controlador = new UsuarioController(modelo, vista);

// Arranca la ejecución llamando a la API y renderizando la tabla
controlador.iniciar();