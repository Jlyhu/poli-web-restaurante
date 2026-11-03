/**
 * permisos.js
 * -----------
 * Traduce el DIAGRAMA DE NAVEGACIÓN a datos: qué botones ve cada rol y a qué
 * pantalla lleva cada uno.
 *
 *   pagina: 'archivo.html'  -> botón activo.
 *   pagina: null            -> la pantalla aún no existe: se muestra el botón
 *                              deshabilitado ("pendiente") para respetar el diagrama.
 *
 * Para activar un botón cuando su pantalla esté lista, solo se cambia el null
 * por el nombre del archivo; el control de acceso se ajusta solo.
 */
export const MENU_POR_ROL = {
  Administrador: [
    { texto: 'Gestionar usuarios',               pagina: 'usuarios.html' },
    { texto: 'Gestionar productos y categorías', pagina: 'productos.html' },
    { texto: 'Gestionar mesas',                  pagina: 'catalogos.html' },
    { texto: 'Consultar reservas',               pagina: null },
    { texto: 'Reportes',                         pagina: 'reportes.html' },            // HU-14
    { texto: 'Consultar pedidos (trazabilidad)', pagina: 'trazabilidad.html' },      // HU-15
  ],
  Mesero: [
    { texto: 'Crear pedido',                         pagina: 'crear-pedido.html' },     // HU-02
    { texto: 'Ver mesas',                            pagina: 'mesas.html' },
    { texto: 'Agregar/modificar detalles del pedido', pagina: 'productos-pedido.html' }, // HU-03
    { texto: 'Consultar estado del pedido',          pagina: 'estado-pedido.html' },   // HU-05
    { texto: 'Entregar pedido',                      pagina: 'estado-pedido.html' },   // HU-06
    { texto: 'Cancelar pedido',                      pagina: 'estado-pedido.html' },   // HU-07
    { texto: 'Gestionar reservas',                   pagina: null },
  ],
  Cocinero: [
    { texto: 'Ver pedidos pendientes',   pagina: 'pedidos-pendientes.html' },          // HU-08
    { texto: 'Ver detalle del pedido',   pagina: 'pedidos-pendientes.html' },          // HU-08 (el detalle vive en la misma pantalla)
    { texto: 'Cambiar estado del pedido', pagina: 'estado-preparacion.html' },         // HU-09
  ],
  Cajero: [
    { texto: 'Ver pedidos',    pagina: 'pagos.html' },
    { texto: 'Registrar pago', pagina: 'pagos.html' },
    { texto: 'Gestionar caja', pagina: 'caja.html' },
  ],
  Repartidor: [
    { texto: 'Ver pedidos asignados',        pagina: 'entregas.html' },
    { texto: 'Ver datos de entrega',         pagina: 'entregas.html' },
    { texto: 'Actualizar estado de entrega', pagina: 'entregas.html' },
  ],
};

/** Pantallas que no son un botón del diagrama pero pertenecen a un rol. */
const EXTRAS_POR_ROL = {
  Mesero: ['observaciones.html'],        // redirige a productos-pedido.html (HU-04)
  Administrador: ['disponibilidad.html'], // HU-12, parte de la gestión de productos
};

export const PAGINA_INICIO = 'index.html';
export const PAGINAS_PUBLICAS = ['login.html'];

/** Botones del rol (o [] si el rol no existe). */
export function menuDelRol(rol) {
  return MENU_POR_ROL[rol] ?? [];
}

/** ¿Puede este rol abrir esta pantalla? */
export function puedeAcceder(rol, pagina) {
  if (pagina === PAGINA_INICIO) return true;
  const permitidas = [
    ...menuDelRol(rol).map((b) => b.pagina).filter(Boolean),
    ...(EXTRAS_POR_ROL[rol] ?? []),
  ];
  return permitidas.includes(pagina);
}
