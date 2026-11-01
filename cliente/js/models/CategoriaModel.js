/**
 * ProductoModel.js  (MODELO - Acceso a datos)
 * Encapsula la comunicación con el servicio REST en Flask para la entidad Producto.
 */
import { API_URL, ENDPOINTS } from '../config.js';
import { Categoria } from './Categoria.js';

export class CategoriaModel {
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
    * @param {string} ruta              Ruta relativa, p. ej. '/getProductos'.
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
    
    /** Consulta todas las categorías.  →  GET /getCategorias */
    async listar() {
        const datos = await this.#peticion(ENDPOINTS.listarCategorias);
        return (datos ?? []).map(Categoria.desdeJSON);
    }
    
    /** Consulta una categoría.  →  GET /getCategoria/<id> */
    async obtener(idCategoria) {
        const dato = await this.#peticion(`${ENDPOINTS.obtenerCategoria}/${idCategoria}`);
        return Categoria.desdeJSON(dato);
    }
    
    /** Inserta una categoría nueva.  →  POST /insertCategoria */
    insertar(categoria) {
        return this.#peticion(ENDPOINTS.insertarCategoria, 'POST', categoria.aJSON());
    }
    
    /** Actualiza una categoría.  →  PUT /updateCategoria/<id> */
    actualizar(categoria) {
        return this.#peticion(
            `${ENDPOINTS.actualizarCategoria}/${categoria.idCategoria}`, 'PUT', categoria.aJSON()
        );
    }
    
    /** Elimina una categoría.  →  DELETE /deleteCategoria/<id> (409 si tiene productos) */
    eliminar(idCategoria) {
        return this.#peticion(`${ENDPOINTS.eliminarCategoria}/${idCategoria}`, 'DELETE');
    }
}