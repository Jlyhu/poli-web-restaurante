import { UsuarioModel } from './models/UsuarioModel.js';
import { LoginView } from './views/LoginView.js';
import { LoginController } from './controllers/LoginController.js';
import { obtenerSesion } from './core/sesion.js';

// Si ya hay una sesión abierta no tiene sentido ver el login
if (obtenerSesion()) window.location.replace('index.html');
else new LoginController(new UsuarioModel(), new LoginView());
