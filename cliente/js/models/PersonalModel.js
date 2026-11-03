/** PersonalModel.js (MODELO). Cocineros (HU-09) y administradores (HU-14) con el nombre de su usuario. */
import { ENDPOINTS } from '../config.js';
import { peticion } from './Http.js';

export class PersonalModel {
  async #conNombres(ruta, campoId, etiqueta) {
    const [personal, usuarios] = await Promise.all([peticion(ruta), peticion(ENDPOINTS.listarUsuarios)]);
    const nombres = new Map((usuarios ?? []).map((u) => [u.idUsuario, u.nombre]));
    return (personal ?? []).map((p) => ({
      id: Number(p[campoId]),
      nombre: nombres.get(p.Usuario_idUsuario) ?? `${etiqueta} ${p[campoId]}`,
    }));
  }

  listarCocineros() {
    return this.#conNombres(ENDPOINTS.listarCocineros, 'id_cocinero', 'Cocinero');
  }

  listarAdministradores() {
    return this.#conNombres(ENDPOINTS.listarAdministradores, 'id_administrador', 'Administrador');
  }
}
