/**
 * ProductoView.js (VISTA)
 * Único archivo que toca el DOM en la gestión de productos.
 */
const formatoPrecio = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  minimumFractionDigits: 0,
  maximumFractionDigits: 2
});

export class ProductoView {
  constructor() {
    // Tabla
    this.tablaBody = document.querySelector('#tabla-productos tbody');

    // Panel lateral
    this.panelLateral = document.querySelector('#panel-lateral-formulario');
    this.tituloPanel = document.querySelector('#titulo-panel');
    this.formulario = document.querySelector('#form-producto');
    this.btnGuardar = document.querySelector('#btn-guardar');
    this.btnCancelar = document.querySelector('#btn-cancelar');
    this.btnEliminar = document.querySelector('#btn-eliminar');

    // Campos del formulario
    this.inputNombre = document.querySelector('#input-nombre');
    this.inputDescripcion = document.querySelector('#input-descripcion');
    this.inputPrecio = document.querySelector('#input-precio');
    this.inputCantidad = document.querySelector('#input-cantidad');
    this.selectCategoria = document.querySelector('#select-categoria');

    // Otros
    this.btnCrear = document.querySelector('#btn-crear-producto');
    this.buscador = document.querySelector('#buscar');

    // null = estamos creando; con número = estamos editando ese producto
    this.idEditando = null;

    this.configurarEventosVisuales();
  }

  configurarEventosVisuales() {
    this.btnCrear.addEventListener('click', () => this.activarModoCreacion());
    this.btnCancelar.addEventListener('click', () => this.cerrarPanel());
  }

  // --- MODOS DEL PANEL ---

  activarModoCreacion() {
    this.idEditando = null;
    this.formulario.reset();

    this.tituloPanel.textContent = 'Crear producto';
    this.btnGuardar.textContent = 'Crear';
    this.btnEliminar.classList.add('oculto');
    this.panelLateral.classList.add('panel-abierto');
  }

  activarModoEdicion(producto) {
    this.idEditando = producto.idProducto;

    this.inputNombre.value = producto.nombre;
    this.inputDescripcion.value = producto.descripcion;
    this.inputPrecio.value = producto.precio;
    this.inputCantidad.value = producto.cantidad;
    this.selectCategoria.value = producto.idCategoria;

    this.tituloPanel.textContent = 'Editar producto';
    this.btnGuardar.textContent = 'Actualizar';
    this.btnEliminar.classList.remove('oculto');
    this.panelLateral.classList.add('panel-abierto');
  }

  cerrarPanel() {
    this.panelLateral.classList.remove('panel-abierto');
    this.formulario.reset();
    this.idEditando = null;
  }

  // --- ESTADOS DE LA PANTALLA ---

  mostrarCargando() {
    this.tablaBody.innerHTML = '<tr><td colspan="5">Cargando productos...</td></tr>';
  }

  /** Aviso flotante que desaparece solo. tipo: 'exito' | 'error' */
  mostrarMensaje(texto, tipo = 'exito') {
    const aviso = document.createElement('div');
    aviso.className = `mensaje mensaje-${tipo}`;
    aviso.textContent = texto;
    document.body.appendChild(aviso);
    setTimeout(() => aviso.remove(), 4000);
  }

  /** Bloquea el botón de guardar mientras se espera al servidor. */
  bloquearFormulario(bloquear) {
    this.btnGuardar.disabled = bloquear;
  }

  // --- DIBUJAR DATOS ---

  /** Llena la lista desplegable del formulario con las categorías. */
  cargarCategorias(categorias) {
    this.selectCategoria.innerHTML = '';
    categorias.forEach((categoria) => {
      const opcion = document.createElement('option');
      opcion.value = categoria.idCategoria;
      opcion.textContent = categoria.nombre;
      this.selectCategoria.appendChild(opcion);
    });
  }

  /**
   * @param {import('../models/Producto.js').Producto[]} productos
   * @param {Map<number,string>} nombresCategoria  id de categoría → nombre
   */
  mostrarProductos(productos, nombresCategoria) {
    this.tablaBody.innerHTML = '';

    if (productos.length === 0) {
      this.tablaBody.innerHTML = '<tr><td colspan="5">No hay productos para mostrar.</td></tr>';
      return;
    }

    productos.forEach((producto) => {
      const fila = document.createElement('tr');

      // textContent evita que un nombre con "<" rompa el HTML
      const tdNombre = document.createElement('td');
      tdNombre.textContent = producto.nombre;

      const tdCategoria = document.createElement('td');
      tdCategoria.textContent = nombresCategoria.get(producto.idCategoria) ?? 'Sin categoría';

      const tdPrecio = document.createElement('td');
      tdPrecio.textContent = formatoPrecio.format(producto.precio);

      const tdCantidad = document.createElement('td');
      const badge = document.createElement('span');
      badge.className = `badge ${producto.disponible ? 'badge-verde' : 'badge-gris'}`;
      badge.textContent = producto.disponible ? `${producto.cantidad} disp.` : 'Agotado';
      tdCantidad.appendChild(badge);

      const tdAccion = document.createElement('td');
      const btnEditar = document.createElement('button');
      btnEditar.className = 'btn-editar';
      btnEditar.dataset.id = producto.idProducto;
      btnEditar.textContent = 'Editar';
      tdAccion.appendChild(btnEditar);

      fila.append(tdNombre, tdCategoria, tdPrecio, tdCantidad, tdAccion);
      this.tablaBody.appendChild(fila);
    });
  }

  // --- ENLACES CON EL CONTROLADOR ---

  alEnviarFormulario(callback) {
    this.formulario.addEventListener('submit', (evento) => {
      evento.preventDefault();
      callback({
        idProducto: this.idEditando,               // null = crear, número = actualizar
        nombre: this.inputNombre.value.trim(),
        descripcion: this.inputDescripcion.value.trim(),
        precio: this.inputPrecio.value,            // texto: el Controlador lo convierte
        cantidad: this.inputCantidad.value,
        idCategoria: this.selectCategoria.value
      });
    });
  }

  alClicEditar(callback) {
    this.tablaBody.addEventListener('click', (evento) => {
      const boton = evento.target.closest('.btn-editar');
      if (boton) {
        callback(Number(boton.dataset.id));
      }
    });
  }

  alEliminar(callback) {
    this.btnEliminar.addEventListener('click', () => {
      if (this.idEditando === null) return;
      if (confirm('¿Seguro que quieres eliminar este producto?')) {
        callback(this.idEditando);
      }
    });
  }

  alBuscar(callback) {
    this.buscador.addEventListener('input', () => {
      callback(this.buscador.value.trim());
    });
  }
}