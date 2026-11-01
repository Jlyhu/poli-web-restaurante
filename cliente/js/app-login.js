import { UsuarioModel } from './models/UsuarioModel.js';
import { LoginView } from './views/LoginView.js';
import { LoginController } from './controllers/LoginController.js';

new LoginController(new UsuarioModel(), new LoginView());