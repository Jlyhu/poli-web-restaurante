/**
 * Mesa.js  (MODELO - Entidad)
 * Representa una mesa del restaurante. Equivale a la tabla Mesa.
 * No sabe nada de HTML ni de peticiones HTTP.
 */
export class Mesa {
  /**
   * @param {number|null} idMesa  null mientras la mesa no existe.
   * @param {number} numero       Número visible de la mesa.
   * @param {string} estado       'Disponible' u 'Ocupada'.
   */
  constructor(idMesa, numero, estado) {
    this.idMesa = idMesa;
    this.numero = numero;
    this.estado = estado;
  }

  /** Crea una Mesa desde un objeto de GET /getMesas. */
  static desdeJSON(obj) {
    return new Mesa(
      Number(obj.id_mesa),           // el backend la llama id_mesa
      Number(obj.numero),
      obj.estado ?? 'Disponible'
    );
  }

  /** Cuerpo de POST y PUT. El id no se envía: lo asigna el backend o va en la URL. */
  aJSON() {
    return {
      numero: this.numero,
      estado: this.estado
    };
  }

  /** @returns {string[]} Errores de validación. Vacía si todo es válido. */
  validar(esNuevo) {
    const errores = [];
    if (!esNuevo && (!Number.isInteger(this.idMesa) || this.idMesa <= 0)) {
      errores.push('El id de la mesa no es válido.');
    }
    if (!Number.isInteger(this.numero) || this.numero < 1) {
      errores.push('El número de mesa debe ser un entero mayor o igual a 1.');
    }
    if (!this.estado.trim()) {
      errores.push('El estado es obligatorio.');
    }
    if (this.estado.length > 45) {
      errores.push('El estado no puede pasar de 45 caracteres.');
    }
    return errores;
  }

  /** @returns {boolean} true si la mesa está libre. */
  get disponible() {
    return this.estado === 'Disponible';
  }
}