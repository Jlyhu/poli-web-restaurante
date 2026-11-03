/**
 * guard.js
 * --------
 * Se incluye en TODAS las pantallas (menos login.html). Hace tres cosas:
 *   1. Si no hay sesión          -> manda a login.html.
 *   2. Si el rol no tiene acceso -> manda a index.html.
 *   3. Dibuja en el menú lateral SOLO los botones del rol, con nombre y "Cerrar sesión".
 *
 * IMPORTANTE: esto controla la interfaz. Los endpoints del servicio Flask siguen
 * abiertos; para protegerlos de verdad habría que validar el rol también en el backend.
 */
import { obtenerSesion, cerrarSesion } from './sesion.js';
import { menuDelRol, puedeAcceder } from './permisos.js';

const pagina = window.location.pathname.split('/').pop() || 'index.html';
const sesion = obtenerSesion();

if (!sesion) {
  window.location.replace('login.html');
} else if (!puedeAcceder(sesion.rol, pagina)) {
  window.location.replace('index.html');
} else {
  document.addEventListener('DOMContentLoaded', () => pintarMenuLateral(sesion));
}

function pintarMenuLateral(s) {
  const lista = document.querySelector('.lista-menu');
  if (!lista) return;
  lista.innerHTML = '';

  const inicio = document.createElement('li');
  inicio.innerHTML = '<a href="index.html">Inicio</a>';
  lista.appendChild(inicio);

  const vistos = new Set();
  for (const boton of menuDelRol(s.rol)) {
    if (!boton.pagina || vistos.has(boton.pagina)) continue;   // duplicados y pendientes no van en el lateral
    vistos.add(boton.pagina);
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = boton.pagina;
    a.textContent = boton.texto;
    if (boton.pagina === pagina) a.classList.add('activo');
    li.appendChild(a);
    lista.appendChild(li);
  }

  const pie = document.createElement('div');
  pie.className = 'usuario-sesion';
  pie.innerHTML = `<p><strong></strong><br><span></span></p>
                   <button type="button" class="btn-secundario">Cerrar sesión</button>`;
  pie.querySelector('strong').textContent = s.nombre;
  pie.querySelector('span').textContent = s.rol;
  pie.querySelector('button').addEventListener('click', cerrarSesion);
  lista.parentElement.appendChild(pie);
}
