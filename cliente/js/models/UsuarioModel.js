/**
 * UsuarioModel.js  (MODELO - Acceso a datos)
 * ------------------------------------------
 * Encapsula la comunicación con el servicio REST en Flask para la entidad Usuario.
 *
 * En MVC el Modelo es la fuente de los datos. En una aplicación web cliente,
 * los datos viven en el servidor, así que este Modelo:
 *   1. Hace las peticiones HTTP con fetch().
 *   2. Convierte las respuestas en objetos Usuario.
 *   3. Traduce los errores del servidor en excepciones de JavaScript.
 *
 * El Controlador usa estos métodos sin saber nada de URLs, headers ni JSON.
 */
import { API_URL, ENDPOINTS } from '../config.js';
import { Usuario } from './Usuario.js';

export class UsuarioModel {
    /**
    * saca el mensaje de error de lo que respondió el servidor.
    * Flask responde {"error": "..."}; los errores de validación (marshmallow)
    * llegan como {"campo": ["mensaje"]}.
    */
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
    * Método privado (el # lo hace inaccesible desde fuera de la clase) que
    * centraliza la lógica común a todas las peticiones.
    *
    * @param {string} ruta              Ruta relativa, p. ej. '/getUsuarios'.
    * @param {string} [metodo='GET']    Método HTTP.
    * @param {Object} [cuerpo]          Datos a enviar como JSON (opcional).
    * @returns {Promise<any>}           El JSON de la respuesta ya interpretado.
    * @throws {Error}                   Si hay error de red o el servidor reporta error.
    */
    async #peticion(ruta, metodo = 'GET', cuerpo) {
        const opciones = { method: metodo, headers: {} };
        if (cuerpo !== undefined) {
            // Este header es indispensable: sin él, request.get_json() en Flask
            // no reconoce el body y responde 415 (Unsupported Media Type).
            opciones.headers['Content-Type'] = 'application/json';
            opciones.body = JSON.stringify(cuerpo);
        }
        let respuesta;
        try {
            respuesta = await fetch(API_URL + ruta, opciones);
        } catch {
            // fetch solo falla aquí cuando no hay comunicación: servidor apagado,
            // URL equivocada o petición bloqueada por CORS.
            throw new Error(
                `No se pudo conectar con el servidor (${API_URL}). ` + 'Verifique que Flask esté corriendo y que tenga CORS habilitado.'
            );
        }
        
        // Se intenta leer el JSON; si el servidor devolvió HTML (p. ej. la página de error de Flask), se deja en null.
        const datos = await respuesta.json().catch(() => null);

        // Error HTTP real (400, 404, 409, 500...).
        if (!respuesta.ok) {
            // backend responde con "error"
            throw new Error(this.#mensajeDeError(datos, respuesta.status));
        }

        // Se deja por si algún endpoint responde errores con código 200 y err: true.
        if (datos && datos.err) {
            throw new Error(datos.message ?? 'El servidor reportó un error.');
        }
        return datos;
    }

    /**
    * Consulta todos los usuarios.  →  GET /getUsuarios
    * @returns {Promise<Usuario[]>}
    */
    async listar() {
        const datos = await this.#peticion(ENDPOINTS.listarUsuarios);

        // El backend devuelve un arreglo de objetos planos; se convierte cada uno en una instancia de Usuario.
        return (datos ?? []).map(Usuario.desdeJSON);
    }

    /**
    * Inserta un usuario nuevo.  →  POST /insertUsuario
    * CAMBIO: el POST no recibe el estado (nace 'activo'). Si en el formulario
    * se eligió 'inactivo', se llama después a /desactivarUsuario.
    * @param {Usuario} usuario
    * @returns {Promise<Object>} El usuario creado.
    */
    async insertar(usuario) {
        const creado = await this.#peticion(ENDPOINTS.insertarUsuario, 'POST', usuario.aJSON());
        if (usuario.estado === 'inactivo') {
            await this.#peticion(`${ENDPOINTS.desactivarUsuario}/${creado.idUsuario}`, 'PUT');
        }
        return creado;
    }

    /**
    * Actualiza un usuario existente.  →  PUT /updateUsuario/<id>
    * CAMBIO: el id va en la URL (no en el body) y el estado se cambia con
    * /activarUsuario o /desactivarUsuario según lo elegido.
    * @param {Usuario} usuario
    * @returns {Promise<Object>}
    */
    async actualizar(usuario) {
        const actualizado = await this.#peticion(
        `${ENDPOINTS.actualizarUsuario}/${usuario.idUsuario}`, 'PUT', usuario.aJSON()
        );
        const ruta = usuario.estado === 'inactivo'
        ? ENDPOINTS.desactivarUsuario
        : ENDPOINTS.activarUsuario;
        await this.#peticion(`${ruta}/${usuario.idUsuario}`, 'PUT');
        return actualizado;
    }

    /**
    * Elimina un usuario por su id.  →  DELETE /deleteUsuario/<id>
    * @param {number} idUsuario
    * @returns {Promise<Object>}
    */
    eliminar(idUsuario) {
        return this.#peticion(`${ENDPOINTS.eliminarUsuario}/${idUsuario}`, 'DELETE');
    }
}