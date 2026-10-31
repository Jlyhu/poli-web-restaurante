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
export const API_URL = 'http://localhost:5000'; 

export const ENDPOINTS = {
    // --- USUARIOS ---
    listarUsuarios: '/getUsuarios',
    obtenerUsuario: '/getUsuario',
    insertarUsuario: '/insertUsuario',
    actualizarUsuario: '/updateUsuario',
    desactivarUsuario: '/desactivarUsuario',
    activarUsuario: '/activarUsuario',
    eliminarUsuario: '/deleteUsuario',

    // --- CLIENTES ---
    listarClientes: '/getClientes',
    obtenerCliente: '/getCliente',
    insertarCliente: '/insertCliente',
    
    // --- PEDIDOS ---
    listarPedidos: '/getPedidos',
    // ... y así sucesivamente
};