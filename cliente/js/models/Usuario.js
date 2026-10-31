/**
 * Usuario.js  (MODELO - Entidad)
 * ------------------------------
 * Representa un usuario del dominio. Es el equivalente en el cliente de la
 * clase Usuario de models.py en el backend.
 *
 * Responsabilidades:
 *   - Guardar los datos de un usuario.
 *   - Validar que los datos sean correctos ANTES de enviarlos al servidor.
 *   - Convertirse desde/hacia el formato JSON que entiende el backend.
 *
 * No sabe nada de HTML ni de peticiones HTTP: eso le corresponde a la Vista
 * y a UsuarioModel respectivamente.
 */
export class Usuario {
    /**
    * @param {number|null} idUsuario   Llave primaria. null mientras el usuario no existe.
    * @param {string} nombre
    * @param {string} credenciales     Al editar, vacío = no cambiar la contraseña.
    * @param {string} estado           'activo' o 'inactivo'
    * @param {string|null} rol         NUEVO: Mesero, Cocinero, Repartidor, Cajero o Administrador
    * @param {string|null} datoRol     NUEVO: zona (Mesero), placa (Repartidor) o estación (Cocinero)
    */

    constructor(idUsuario, nombre, credenciales, estado, rol = null, datoRol = null) {
        // Los nombres de los atributos coinciden con las columnas de la tabla Usuario.
        // // rol y datoRol NO son columnas de Usuario: viven en las tablas de cada rol.
        this.idUsuario = idUsuario;
        this.nombre = nombre;
        this.credenciales = credenciales;
        this.estado = estado;
        this.rol = rol;
        this.datoRol = datoRol;
    }

    /**
    * Crea un Usuario a partir de un objeto plano, por ejemplo uno de los
    * elementos del arreglo que devuelve GET /getUsuarios.
    * Es un "método fábrica": se llama sobre la clase, no sobre una instancia.
    *
    * @param {Object} obj  Objeto con las mismas llaves que las columnas.
    * @returns {Usuario}
    */

    static desdeJSON(obj) {
        return new Usuario(
            Number(obj.idUsuario),
            obj.nombre ?? '',          // ?? : si el valor es null/undefined usa ''
            obj.credenciales ?? '',    // el backend nunca la devuelve: queda ''
            obj.estado ?? 'activo',    // en minúscula, como lo guarda la base
            obj.rol ?? null,           // si el usuario no tiene rol, queda null
            obj.datoRol ?? null        // si no hay dato del rol, queda null
        );
    }

    /**
    * Devuelve el objeto plano que se envía en el body de POST y PUT.
    * Las llaves deben llamarse igual que en el UsuarioSchema del backend.
    *
    * @returns {Object}
    */
    
    aJSON() {
        const cuerpo = {
            idUsuario: this.idUsuario,
            nombre: this.nombre,
            rol: this.rol,
            datoRol: this.datoRol,
        };
    // el estado ya no se envía (el schema no lo acepta; cambia con /activarUsuario y /desactivarUsuario) y las credenciales solo van si se escribieron (al editar, vacío = no cambiar la contraseña).
        if (this.credenciales.trim()) {
            cuerpo.credenciales = this.credenciales;
        }
        return cuerpo;
    }

    /**
    * Valida las reglas de negocio del usuario.
    *
    * @param {boolean} esNuevo  true al crear, false al editar.
    * @returns {string[]} Lista de mensajes de error. Vacía si todo es válido.
    */
    validar(esNuevo) {
        const errores = [];
        // al crear el id todavía no existe (lo asigna el backend)
        if (!esNuevo && (!Number.isInteger(this.idUsuario) || this.idUsuario <= 0)) {
            errores.push('El id de usuario no es válido.');
        }
        if (!this.nombre.trim()) {
            errores.push('El nombre es obligatorio.');
        }
        // al crear son obligatorias; al editar pueden ir vacías
        if (esNuevo && !this.credenciales.trim()) {
            errores.push('Las credenciales son obligatorias.');
        }
        if (!this.estado.trim()) {
            errores.push('El estado es obligatorio.');
        }
        if (!this.rol) {                                  
            errores.push('El rol es obligatorio.');
        }
        if (this.datoRol && this.datoRol.length > 45) {
            errores.push('El dato del rol no puede pasar de 45 caracteres.');
        }
        return errores;
    }

  /** @returns {string} Nombre y estado, útil para mensajes en la interfaz. */
    get informacionGeneral() {
        return `${this.nombre} (${this.estado})`;
    }
}