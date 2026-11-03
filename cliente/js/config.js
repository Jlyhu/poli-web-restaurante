/**
 * config.js
 * ---------
 * Configuración global del cliente.
 *
 * Centralizar la URL del servicio aquí evita tener direcciones "quemadas"
 * en varios archivos: si el backend cambia de máquina o de puerto,
 * solo se modifica esta constante.
 */

/**
 * URL base del servicio REST en Flask.
 * Corresponde a app.run("0.0.0.0", 5000, ...) en mainService.py.
 * Si el servidor corre en otro equipo, reemplace "localhost" por su IP.
 * @type {string}
 */
export const API_URL = 'http://127.0.0.1:5000'; 

export const ENDPOINTS = {
    // --- USUARIOS ---
    listarUsuarios: '/getUsuarios',
    obtenerUsuario: '/getUsuario',
    insertarUsuario: '/insertUsuario',
    actualizarUsuario: '/updateUsuario',
    desactivarUsuario: '/desactivarUsuario',
    activarUsuario: '/activarUsuario',
    eliminarUsuario: '/deleteUsuario',

    // --- LOGIN ---
    iniciarSesion: '/loginUsuario',

    // --- CLIENTES ---
    listarClientes: '/getClientes',
    obtenerCliente: '/getCliente',
    insertarCliente: '/insertCliente',
    actualizarCliente: '/updateCliente',
    eliminarCliente: '/deleteCliente',
    
    // --- CATEGORÍAS ---
    listarCategorias: '/getCategorias',
    obtenerCategoria: '/getCategoria',
    insertarCategoria: '/insertCategoria',
    actualizarCategoria: '/updateCategoria',
    eliminarCategoria: '/deleteCategoria',

    // --- PRODUCTOS ---
    listarProductos: '/getProductos',
    listarProductosDisponibles: '/getProductosDisponibles',
    insertarProducto: '/insertProducto',
    actualizarProducto: '/updateProducto',
    agotarProducto: '/agotarProducto',
    eliminarProducto: '/deleteProducto',

    // --- MESAS ---
    listarMesas: '/getMesas',
    obtenerMesa: '/getMesa',
    insertarMesa: '/insertMesa',
    actualizarMesa: '/updateMesa',
    eliminarMesa: '/deleteMesa',


    // --- PEDIDOS (HU-02, HU-08, HU-09) ---
    listarPedidos: '/getPedidos',
    listarMesasDisponibilidad: '/getMesasDisponibilidad',
    listarPedidosConMesa: '/getPedidosConMesa',
    crearPedidoMesa: '/crearPedidoMesa',
    cambiarEstadoPedido: '/cambiarEstadoPedido',

    // --- DETALLE DEL PEDIDO (HU-03, HU-04, HU-08) ---
    detallePedidoConProducto: '/getDetallePedidoConProducto',
    insertarDetallePedido: '/insertDetallePedido',
    actualizarDetallePedido: '/updateDetallePedido',
    eliminarDetallePedido: '/deleteDetallePedido',

    // --- COCINEROS Y ADMINISTRADORES ---
    listarCocineros: '/getCocineros',
    listarAdministradores: '/getAdministradores',

    // --- REPORTES (HU-14) ---
    reporteVentas: '/reporteVentas',
    reporteTiempos: '/reporteTiempos',

    // ... y así sucesivamente
};