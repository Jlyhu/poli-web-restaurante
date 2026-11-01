/**
 * ProductoModel.js  (MODELO - Acceso a datos)
 * Encapsula la comunicación con el servicio REST en Flask para la entidad Producto.
 * Lo comparten HU-11 (gestionar productos) y HU-12 (disponibilidad).
 */
import { API_URL, ENDPOINTS } from '../config.js';
import { Producto } from './Producto.js';

export class ProductoModel {
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

    /** Consulta todos los productos.  →  GET /getProductos */
    async listar() {
        const datos = await this.#peticion(ENDPOINTS.listarProductos);
        return (datos ?? []).map(Producto.desdeJSON);
    }

    /** Consulta solo los que tienen unidades.  →  GET /getProductosDisponibles */
    async listarDisponibles() {
        const datos = await this.#peticion(ENDPOINTS.listarProductosDisponibles);
        return (datos ?? []).map(Producto.desdeJSON);
    }

    /** Consulta un producto.  →  GET /getProducto/<id> */
    async obtener(idProducto) {
        const dato = await this.#peticion(`${ENDPOINTS.obtenerProducto}/${idProducto}`);
        return Producto.desdeJSON(dato);
    }
    
    /** Inserta un producto nuevo.  →  POST /insertProducto */
    insertar(producto) {
        return this.#peticion(ENDPOINTS.insertarProducto, 'POST', producto.aJSON());
    }

    /** Actualiza un producto.  →  PUT /updateProducto/<id> */
    actualizar(producto) {
        return this.#peticion(`${ENDPOINTS.actualizarProducto}/${producto.idProducto}`, 'PUT', producto.aJSON()
        );
    }
    
    /** Deja la cantidad en 0.  →  PUT /agotarProducto/<id> */
    agotar(idProducto) {
        return this.#peticion(`${ENDPOINTS.agotarProducto}/${idProducto}`, 'PUT');
    }
    
    /** Elimina un producto.  →  DELETE /deleteProducto/<id> (409 si ya está en un pedido) */
    eliminar(idProducto) {
        return this.#peticion(`${ENDPOINTS.eliminarProducto}/${idProducto}`, 'DELETE');
    }
}