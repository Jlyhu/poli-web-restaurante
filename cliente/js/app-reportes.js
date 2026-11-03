/**
 * app-reportes.js
 * Punto de arranque de HU-14.
 */
import { ReporteModel } from './models/ReporteModel.js';
import { PersonalModel } from './models/PersonalModel.js';
import { ReportesView } from './views/ReportesView.js';
import { ReportesController } from './controllers/ReportesController.js';

new ReportesController(new ReporteModel(), new PersonalModel(), new ReportesView()).iniciar();
