/**
 * app-index.js
 * Pantalla de inicio: muestra únicamente los botones del rol de la sesión,
 * tal como los define el diagrama de navegación (core/permisos.js).
 */
import { obtenerSesion, cerrarSesion } from './core/sesion.js';
import { menuDelRol } from './core/permisos.js';

const sesion = obtenerSesion();
if (sesion) {
  document.querySelector('#saludo').textContent = `Sesión iniciada como ${sesion.nombre} · ${sesion.rol}`;
  const contenedor = document.querySelector('#botones-rol');

  for (const boton of menuDelRol(sesion.rol)) {
    const el = document.createElement(boton.pagina ? 'a' : 'span');
    el.className = 'tarjeta-acceso';
    if (boton.pagina) {
      el.href = boton.pagina;
      el.textContent = boton.texto;
    } else {
      el.classList.add('tarjeta-pendiente');
      el.textContent = `${boton.texto} (pendiente)`;
      el.title = 'Esta pantalla aún no está implementada';
    }
    contenedor.appendChild(el);
  }
  document.querySelector('#btn-cerrar-sesion').addEventListener('click', cerrarSesion);
}
