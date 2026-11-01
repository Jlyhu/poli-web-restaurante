/**
 * MesaModel.js  (MODELO - Acceso a datos)
 * Encapsula la comunicación con el servicio REST en Flask para la entidad Mesa.
 */
import { API_URL, ENDPOINTS } from '../config.js';
import { Mesa } from './Mesa.js';

export class MesaModel {
  /** Saca el mensaje de error de lo que respondió el servidor. */
  #mensajeDeError(datos, estado) {
    if (datos?.message) return datos.message;
    if (typeof datos?.error === 'string') return datos.error;
    if (datos && typeof datos === 'object') {
      const textos = Object.entries(datos)
        .map(([campo, msg]) => `${campo}: ${[].concat(msg).join(' ')}`);
      if (textos.length > 0) return textos.join(' ');
    }
    return `Error HTTP ${estado}`;
  }

  /**
   * Método privado que centraliza la lógica común a todas las peticiones.
   * @param {string} ruta              Ruta relativa, p. ej. '/getMesas'.
   * @param {string} [metodo='GET']    Método HTTP.
   * @param {Object} [cuerpo]          Datos a enviar como JSON (opcional).
   * @returns {Promise<any>}
   * @throws {Error} Si hay error de red o el servidor reporta error.
   */
  async #peticion(ruta, metodo = 'GET', cuerpo) {
    const opciones = { method: metodo, headers: {} };
    if (cuerpo !== undefined) {
      opciones.headers['Content-Type'] = 'application/json';
      opciones.body = JSON.stringify(cuerpo);
    }

    let respuesta;
    try {
      respuesta = await fetch(API_URL + ruta, opciones);
    } catch {
      throw new Error(
        `No se pudo conectar con el servidor (${API_URL}). ` +
        'Verifique que Flask esté corriendo y que tenga CORS habilitado.'
      );
    }

    const datos = await respuesta.json().catch(() => null);

    if (!respuesta.ok) {
      throw new Error(this.#mensajeDeError(datos, respuesta.status));
    }
    if (datos && datos.err) {
      throw new Error(datos.message ?? 'El servidor reportó un error.');
    }
    return datos;
  }

  /** Consulta todas las mesas.  →  GET /getMesas */
  async listar() {
    const datos = await this.#peticion(ENDPOINTS.listarMesas);
    return (datos ?? []).map(Mesa.desdeJSON);
  }

  /** Consulta una mesa.  →  GET /getMesa/<id> */
  async obtener(idMesa) {
    const dato = await this.#peticion(`${ENDPOINTS.obtenerMesa}/${idMesa}`);
    return Mesa.desdeJSON(dato);
  }

  /** Inserta una mesa nueva.  →  POST /insertMesa */
  insertar(mesa) {
    return this.#peticion(ENDPOINTS.insertarMesa, 'POST', mesa.aJSON());
  }

  /** Actualiza una mesa.  →  PUT /updateMesa/<id> */
  actualizar(mesa) {
    return this.#peticion(`${ENDPOINTS.actualizarMesa}/${mesa.idMesa}`, 'PUT', mesa.aJSON());
  }

  /** Elimina una mesa.  →  DELETE /deleteMesa/<id> (409 si está en un pedido o reservación) */
  eliminar(idMesa) {
    return this.#peticion(`${ENDPOINTS.eliminarMesa}/${idMesa}`, 'DELETE');
  }
}