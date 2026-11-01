/**
 * CatalogosView.js (VISTA)
 * Único archivo que toca el DOM en la gestión de categorías y mesas.
 * Hay un solo panel lateral con dos formularios; se muestra uno u otro.
 */
export class CatalogosView {
  constructor() {
    // Tablas
    this.tablaCategorias = document.querySelector('#tabla-categorias tbody');
    this.tablaMesas = document.querySelector('#tabla-mesas tbody');

    // Panel lateral (compartido)
    this.panelLateral = document.querySelector('#panel-lateral-formulario');
    this.tituloPanel = document.querySelector('#titulo-panel');

    // Formulario de categoría
    this.formCategoria = document.querySelector('#form-categoria');
    this.inputNombreCategoria = document.querySelector('#input-nombre-categoria');
    this.btnGuardarCategoria = document.querySelector('#btn-guardar-categoria');
    this.btnCancelarCategoria = document.querySelector('#btn-cancelar-categoria');
    this.btnEliminarCategoria = document.querySelector('#btn-eliminar-categoria');

    // Formulario de mesa
    this.formMesa = document.querySelector('#form-mesa');
    this.inputNumeroMesa = document.querySelector('#input-numero-mesa');
    this.selectEstadoMesa = document.querySelector('#select-estado-mesa');
    this.btnGuardarMesa = document.querySelector('#btn-guardar-mesa');
    this.btnCancelarMesa = document.querySelector('#btn-cancelar-mesa');
    this.btnEliminarMesa = document.querySelector('#btn-eliminar-mesa');

    // Barras de herramientas
    this.btnCrearCategoria = document.querySelector('#btn-crear-categoria');
    this.buscarCategoria = document.querySelector('#buscar-categoria');
    this.btnCrearMesa = document.querySelector('#btn-crear-mesa');
    this.buscarMesa = document.querySelector('#buscar-mesa');

    // null = estamos creando; con número = estamos editando ese registro
    this.idEditandoCategoria = null;
    this.idEditandoMesa = null;

    this.configurarEventosVisuales();
  }

  configurarEventosVisuales() {
    this.btnCrearCategoria.addEventListener('click', () => this.activarModoCreacionCategoria());
    this.btnCrearMesa.addEventListener('click', () => this.activarModoCreacionMesa());
    this.btnCancelarCategoria.addEventListener('click', () => this.cerrarPanel());
    this.btnCancelarMesa.addEventListener('click', () => this.cerrarPanel());
  }

  // --- PANEL LATERAL ---

  /** Muestra el formulario que corresponde y abre el panel. tipo: 'categoria' | 'mesa' */
  #abrirPanel(tipo) {
    const esCategoria = tipo === 'categoria';
    this.formCategoria.classList.toggle('oculto', !esCategoria);
    this.formMesa.classList.toggle('oculto', esCategoria);
    this.panelLateral.classList.add('panel-abierto');
  }

  cerrarPanel() {
    this.panelLateral.classList.remove('panel-abierto');
    this.formCategoria.reset();
    this.formMesa.reset();
    this.idEditandoCategoria = null;
    this.idEditandoMesa = null;
  }

  activarModoCreacionCategoria() {
    this.idEditandoCategoria = null;
    this.formCategoria.reset();

    this.tituloPanel.textContent = 'Crear categoría';
    this.btnGuardarCategoria.textContent = 'Crear';
    this.btnEliminarCategoria.classList.add('oculto');
    this.#abrirPanel('categoria');
  }

  activarModoEdicionCategoria(categoria) {
    this.idEditandoCategoria = categoria.idCategoria;
    this.inputNombreCategoria.value = categoria.nombre;

    this.tituloPanel.textContent = 'Editar categoría';
    this.btnGuardarCategoria.textContent = 'Actualizar';
    this.btnEliminarCategoria.classList.remove('oculto');
    this.#abrirPanel('categoria');
  }

  activarModoCreacionMesa() {
    this.idEditandoMesa = null;
    this.formMesa.reset();

    this.tituloPanel.textContent = 'Crear mesa';
    this.btnGuardarMesa.textContent = 'Crear';
    this.btnEliminarMesa.classList.add('oculto');
    this.#abrirPanel('mesa');
  }

  activarModoEdicionMesa(mesa) {
    this.idEditandoMesa = mesa.idMesa;
    this.inputNumeroMesa.value = mesa.numero;
    this.selectEstadoMesa.value = mesa.estado;

    this.tituloPanel.textContent = 'Editar mesa';
    this.btnGuardarMesa.textContent = 'Actualizar';
    this.btnEliminarMesa.classList.remove('oculto');
    this.#abrirPanel('mesa');
  }

  // --- ESTADOS DE LA PANTALLA ---

  mostrarCargando() {
    this.tablaCategorias.innerHTML = '<tr><td colspan="2">Cargando categorías...</td></tr>';
    this.tablaMesas.innerHTML = '<tr><td colspan="3">Cargando mesas...</td></tr>';
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
  bloquearFormularioCategoria(bloquear) {
    this.btnGuardarCategoria.disabled = bloquear;
  }

  bloquearFormularioMesa(bloquear) {
    this.btnGuardarMesa.disabled = bloquear;
  }

  // --- DIBUJAR DATOS ---

  /** @param {import('../models/Categoria.js').Categoria[]} categorias */
  mostrarCategorias(categorias) {
    this.tablaCategorias.innerHTML = '';

    if (categorias.length === 0) {
      this.tablaCategorias.innerHTML = '<tr><td colspan="2">No hay categorías para mostrar.</td></tr>';
      return;
    }

    categorias.forEach((categoria) => {
      const fila = document.createElement('tr');

      // textContent evita que un nombre con "<" rompa el HTML
      const tdNombre = document.createElement('td');
      tdNombre.textContent = categoria.nombre;

      const tdAccion = document.createElement('td');
      const btnEditar = document.createElement('button');
      btnEditar.className = 'btn-editar';
      btnEditar.dataset.id = categoria.idCategoria;
      btnEditar.textContent = 'Editar';
      tdAccion.appendChild(btnEditar);

      fila.append(tdNombre, tdAccion);
      this.tablaCategorias.appendChild(fila);
    });
  }

  /** @param {import('../models/Mesa.js').Mesa[]} mesas */
  mostrarMesas(mesas) {
    this.tablaMesas.innerHTML = '';

    if (mesas.length === 0) {
      this.tablaMesas.innerHTML = '<tr><td colspan="3">No hay mesas para mostrar.</td></tr>';
      return;
    }

    mesas.forEach((mesa) => {
      const fila = document.createElement('tr');

      const tdNumero = document.createElement('td');
      tdNumero.textContent = mesa.numero;

      const tdEstado = document.createElement('td');
      const badge = document.createElement('span');
      badge.className = `badge ${mesa.disponible ? 'badge-verde' : 'badge-gris'}`;
      badge.textContent = mesa.estado;
      tdEstado.appendChild(badge);

      const tdAccion = document.createElement('td');
      const btnEditar = document.createElement('button');
      btnEditar.className = 'btn-editar';
      btnEditar.dataset.id = mesa.idMesa;
      btnEditar.textContent = 'Editar';
      tdAccion.appendChild(btnEditar);

      fila.append(tdNumero, tdEstado, tdAccion);
      this.tablaMesas.appendChild(fila);
    });
  }

  // --- ENLACES CON EL CONTROLADOR: CATEGORÍAS ---

  alEnviarFormularioCategoria(callback) {
    this.formCategoria.addEventListener('submit', (evento) => {
      evento.preventDefault();
      callback({
        idCategoria: this.idEditandoCategoria,   // null = crear, número = actualizar
        nombre: this.inputNombreCategoria.value.trim()
      });
    });
  }

  alClicEditarCategoria(callback) {
    this.tablaCategorias.addEventListener('click', (evento) => {
      const boton = evento.target.closest('.btn-editar');
      if (boton) callback(Number(boton.dataset.id));
    });
  }

  alEliminarCategoria(callback) {
    this.btnEliminarCategoria.addEventListener('click', () => {
      if (this.idEditandoCategoria === null) return;
      if (confirm('¿Seguro que quieres eliminar esta categoría?')) {
        callback(this.idEditandoCategoria);
      }
    });
  }

  alBuscarCategoria(callback) {
    this.buscarCategoria.addEventListener('input', () => {
      callback(this.buscarCategoria.value.trim());
    });
  }

  // --- ENLACES CON EL CONTROLADOR: MESAS ---

  alEnviarFormularioMesa(callback) {
    this.formMesa.addEventListener('submit', (evento) => {
      evento.preventDefault();
      callback({
        idMesa: this.idEditandoMesa,             // null = crear, número = actualizar
        numero: this.inputNumeroMesa.value,      // texto: el Controlador lo convierte
        estado: this.selectEstadoMesa.value
      });
    });
  }

  alClicEditarMesa(callback) {
    this.tablaMesas.addEventListener('click', (evento) => {
      const boton = evento.target.closest('.btn-editar');
      if (boton) callback(Number(boton.dataset.id));
    });
  }

  alEliminarMesa(callback) {
    this.btnEliminarMesa.addEventListener('click', () => {
      if (this.idEditandoMesa === null) return;
      if (confirm('¿Seguro que quieres eliminar esta mesa?')) {
        callback(this.idEditandoMesa);
      }
    });
  }

  alBuscarMesa(callback) {
    this.buscarMesa.addEventListener('input', () => {
      callback(this.buscarMesa.value.trim());
    });
  }
}