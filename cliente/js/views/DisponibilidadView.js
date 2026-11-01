/**
 * DisponibilidadView.js (VISTA)
 * Único archivo que toca el DOM en la gestión de disponibilidad.
 */
export class DisponibilidadView {
  constructor() {
    this.tablaBody = document.querySelector('#tabla-disponibilidad tbody');
    this.buscador = document.querySelector('#buscar');
    this.selectFiltro = document.querySelector('#select-filtro');
  }

  // --- ESTADOS DE LA PANTALLA ---

  mostrarCargando() {
    this.tablaBody.innerHTML = '<tr><td colspan="4">Cargando productos...</td></tr>';
  }

  /** Aviso flotante que desaparece solo. tipo: 'exito' | 'error' */
  mostrarMensaje(texto, tipo = 'exito') {
    const aviso = document.createElement('div');
    aviso.className = `mensaje mensaje-${tipo}`;
    aviso.textContent = texto;
    document.body.appendChild(aviso);
    setTimeout(() => aviso.remove(), 4000);
  }

  // --- DIBUJAR DATOS ---

  /** @param {import('../models/Producto.js').Producto[]} productos */
  mostrarProductos(productos) {
    this.tablaBody.innerHTML = '';

    if (productos.length === 0) {
      this.tablaBody.innerHTML = '<tr><td colspan="4">No hay productos para mostrar.</td></tr>';
      return;
    }

    productos.forEach((producto) => {
      const fila = document.createElement('tr');

      const tdNombre = document.createElement('td');
      tdNombre.textContent = producto.nombre;

      const tdEstado = document.createElement('td');
      const badge = document.createElement('span');
      badge.className = `badge ${producto.disponible ? 'badge-verde' : 'badge-gris'}`;
      badge.textContent = producto.disponible ? 'Disponible' : 'Agotado';
      tdEstado.appendChild(badge);

      const tdCantidad = document.createElement('td');
      const inputCantidad = document.createElement('input');
      inputCantidad.type = 'number';
      inputCantidad.min = '0';
      inputCantidad.step = '1';
      inputCantidad.className = 'input-cantidad';
      inputCantidad.value = producto.cantidad;
      tdCantidad.appendChild(inputCantidad);

      const tdAccion = document.createElement('td');
      const contenedor = document.createElement('div');
      contenedor.className = 'acciones-fila';

      const btnGuardar = document.createElement('button');
      btnGuardar.className = 'btn-editar btn-guardar-cantidad';
      btnGuardar.dataset.id = producto.idProducto;
      btnGuardar.textContent = 'Guardar';

      const btnAgotar = document.createElement('button');
      btnAgotar.className = 'btn-secundario btn-agotar';
      btnAgotar.dataset.id = producto.idProducto;
      btnAgotar.textContent = 'Agotar';
      btnAgotar.disabled = !producto.disponible;   // ya está agotado

      contenedor.append(btnGuardar, btnAgotar);
      tdAccion.appendChild(contenedor);

      fila.append(tdNombre, tdEstado, tdCantidad, tdAccion);
      this.tablaBody.appendChild(fila);

      const btnEliminar = document.createElement('button');
      btnEliminar.className = 'btn-texto btn-peligro btn-eliminar';
      btnEliminar.dataset.id = producto.idProducto;
      btnEliminar.textContent = 'Eliminar';

      contenedor.append(btnGuardar, btnAgotar, btnEliminar);

});
  }

  // --- ENLACES CON EL CONTROLADOR ---

  /** callback(id, textoCantidad): el Controlador valida y convierte el texto. */
  alGuardarCantidad(callback) {
    this.tablaBody.addEventListener('click', (evento) => {
      const boton = evento.target.closest('.btn-guardar-cantidad');
      if (!boton) return;
      const input = boton.closest('tr').querySelector('.input-cantidad');
      callback(Number(boton.dataset.id), input.value);
    });
  }

  alAgotar(callback) {
    this.tablaBody.addEventListener('click', (evento) => {
      const boton = evento.target.closest('.btn-agotar');
      if (!boton) return;
      if (confirm('¿Marcar este producto como agotado?')) {
        callback(Number(boton.dataset.id));
      }
    });
  }

    alEliminar(callback) {
    this.tablaBody.addEventListener('click', (evento) => {
      const boton = evento.target.closest('.btn-eliminar');
      if (!boton) return;
      if (confirm('¿Seguro que quieres eliminar este producto?')) {
        callback(Number(boton.dataset.id));
      }
    });
  }

  alBuscar(callback) {
    this.buscador.addEventListener('input', () => {
      callback(this.buscador.value.trim());
    });
  }

  /** callback('todos' | 'disponibles' | 'agotados') */
  alCambiarFiltro(callback) {
    this.selectFiltro.addEventListener('change', () => {
      callback(this.selectFiltro.value);
    });
  }
}