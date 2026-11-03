/**
 * Http.js
 * Petición fetch compartida por los modelos de pedidos, detalle, personal y reportes.
 * Traduce los errores del servidor Flask ({"error": "..."}) en excepciones de JavaScript.
 */
import { API_URL } from '../config.js';

function mensajeDeError(datos, estado) {
  if (typeof datos?.error === 'string') return datos.error;
  if (datos?.message) return datos.message;
  if (datos && typeof datos === 'object') {
    const textos = Object.entries(datos).map(([campo, msg]) => `${campo}: ${[].concat(msg).join(' ')}`);
    if (textos.length > 0) return textos.join(' ');
  }
  return `Error HTTP ${estado}`;
}

export async function peticion(ruta, metodo = 'GET', cuerpo) {
  const opciones = { method: metodo, headers: {} };
  if (cuerpo !== undefined) {
    opciones.headers['Content-Type'] = 'application/json';
    opciones.body = JSON.stringify(cuerpo);
  }
  let respuesta;
  try {
    respuesta = await fetch(API_URL + ruta, opciones);
  } catch {
    throw new Error(`No se pudo conectar con el servidor (${API_URL}). Verifique que Flask esté corriendo.`);
  }
  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) throw new Error(mensajeDeError(datos, respuesta.status));
  return datos;
}
