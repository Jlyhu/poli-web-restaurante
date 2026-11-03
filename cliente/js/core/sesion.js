/**
 * sesion.js
 * ---------
 * Guarda en sessionStorage quién inició sesión (se borra al cerrar la pestaña).
 * Estructura: { idUsuario, nombre, rol, idRol }
 */
const CLAVE = 'poli_sesion';

export function guardarSesion(datos) {
  sessionStorage.setItem(CLAVE, JSON.stringify({
    idUsuario: datos.idUsuario,
    nombre: datos.nombre,
    rol: datos.rol,
    idRol: datos.idRol,
  }));
}

export function obtenerSesion() {
  try {
    return JSON.parse(sessionStorage.getItem(CLAVE));
  } catch {
    return null;
  }
}

export function cerrarSesion() {
  sessionStorage.removeItem(CLAVE);
  window.location.href = 'login.html';
}
