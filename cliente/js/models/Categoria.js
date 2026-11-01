/**
 * Categoria.js  (MODELO - Entidad)
 * Representa una categoría del menú. Equivale a la tabla Categoria.
 * No sabe nada de HTML ni de peticiones HTTP.
 */
export class Categoria {
    /**
    * @param {number|null} idCategoria  null mientras la categoría no existe.
    * @param {string} nombre
    */
    constructor(idCategoria, nombre) {
        this.idCategoria = idCategoria;
        this.nombre = nombre;
    }
    
    /** Crea una Categoria desde un objeto de GET /getCategorias. */
    static desdeJSON(obj) {
        return new Categoria(
            Number(obj.id_categoria),   // el backend la llama id_categoria
            obj.nombre ?? ''
        );
    }

    /**
    * Cuerpo de POST y PUT. El id no se envía: al crear lo asigna el backend
    * y al editar va en la URL.
    */
    aJSON() {
        return { nombre: this.nombre };
    }

    /** @returns {string[]} Errores de validación. Vacía si todo es válido. */
    validar(esNuevo) {
        const errores = [];
        if (!esNuevo && (!Number.isInteger(this.idCategoria) || this.idCategoria <= 0)) {
            errores.push('El id de la categoría no es válido.');
        }
        if (!this.nombre.trim()) {
            errores.push('El nombre es obligatorio.');
        }
        if (this.nombre.length > 100) {
            errores.push('El nombre no puede pasar de 100 caracteres.');
        }
        return errores;
    }
}