/**
 * UsuarioView.js (VISTA)
 * Único archivo que toca el DOM: dibuja la tabla y captura los clics.
 */

// Qué campo extra necesita cada rol (según tus tablas Mesero, Repartidor, Cocinero...)
const CONFIG_ROL = {
  Mesero:        { etiqueta: 'Zona asignada' },
  Repartidor:    { etiqueta: 'Placa del vehículo' },
  Cocinero:      { etiqueta: 'Estación' },
  Cajero:        null,
  Administrador: null
};

export class UsuarioView {
  constructor() {
    // Tabla
    this.tablaBody = document.querySelector('#tabla-usuarios tbody');

    // Panel lateral
    this.panelLateral = document.querySelector('#panel-lateral-formulario');
    this.tituloPanel = document.querySelector('#titulo-panel');
    this.formulario = document.querySelector('#form-usuario');
    this.btnGuardar = document.querySelector('#btn-guardar');
    this.btnCancelar = document.querySelector('#btn-cancelar');
    this.btnEliminar = document.querySelector('#btn-eliminar');


    // Campos del formulario
    this.inputNombre = document.querySelector('#input-nombre');
    this.inputCredenciales = document.querySelector('#input-credenciales');
    this.selectRol = document.querySelector('#select-rol');
    this.inputDinamico = document.querySelector('#input-dinamico');
    this.labelDinamico = document.querySelector('#label-dinamico');
    this.grupoDinamico = this.inputDinamico.closest('.grupo-input');
    this.selectEstado = document.querySelector('#select-estado');

    // Otros
    this.btnCrearUsuario = document.querySelector('#btn-crear-usuario');
    this.buscador = document.querySelector('#buscar');
    this.sidebarMenu = document.querySelector('#sidebar-menu');
    this.btnToggleMenu = document.querySelector('#btn-toggle-menu');

    // null = estamos creando; con número = estamos editando ese usuario
    this.idEditando = null;

    this.configurarEventosVisuales();
  }

  // --- MÉTODOS VISUALES ---

  configurarEventosVisuales() {
    this.btnCrearUsuario.addEventListener('click', () => this.activarModoCreacion());
    this.btnCancelar.addEventListener('click', () => this.cerrarPanel());

    // Al cambiar el rol, cambia la etiqueta del campo extra
    this.selectRol.addEventListener('change', () => this.actualizarCampoDinamico());

    if (this.btnToggleMenu) {
      this.btnToggleMenu.addEventListener('click', () => {
        this.sidebarMenu.classList.toggle('menu-colapsado');
      });
    }
  }

  // Muestra/oculta el campo extra y cambia su etiqueta según el rol
  actualizarCampoDinamico() {
    const config = CONFIG_ROL[this.selectRol.value];

    if (config) {
      this.labelDinamico.textContent = config.etiqueta;
      this.grupoDinamico.classList.remove('oculto');
    } else {
      this.grupoDinamico.classList.add('oculto');
      this.inputDinamico.value = '';
    }
  }

  activarModoCreacion() {
    this.idEditando = null;
    this.formulario.reset();
    this.actualizarCampoDinamico();

    this.inputCredenciales.required = true;
    this.inputCredenciales.placeholder = '';

    this.tituloPanel.textContent = 'Crear usuario';
    this.btnGuardar.textContent = 'Guardar cambios';
    this.btnEliminar.classList.add('oculto');
    this.panelLateral.classList.add('panel-abierto');
  }

  activarModoEdicion(usuario) {
    this.idEditando = usuario.idUsuario;

    this.inputNombre.value = usuario.nombre;
    this.selectRol.value = usuario.rol ?? 'Mesero';
    this.selectEstado.value = usuario.estado;
    this.actualizarCampoDinamico();
    this.inputDinamico.value = usuario.datoRol ?? '';

    // La contraseña NO se muestra: si se deja vacía, no se cambia
    this.inputCredenciales.value = '';
    this.inputCredenciales.required = false;
    this.inputCredenciales.placeholder = 'Dejar vacío para no cambiarla';

    this.tituloPanel.textContent = 'Editar usuario';
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
    this.tablaBody.innerHTML = '<tr><td colspan="4">Cargando usuarios...</td></tr>';
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

  mostrarUsuarios(usuarios) {
    this.tablaBody.innerHTML = '';

    if (usuarios.length === 0) {
      this.tablaBody.innerHTML = '<tr><td colspan="4">No hay usuarios para mostrar.</td></tr>';
      return;
    }

    usuarios.forEach(usuario => {
      const fila = document.createElement('tr');

      // textContent evita que un nombre con "<" rompa el HTML
      const tdNombre = document.createElement('td');
      tdNombre.textContent = usuario.nombre;

      const tdRol = document.createElement('td');
      tdRol.textContent = usuario.rol ?? 'Sin rol';

      const activo = usuario.estado === 'activo';
      const tdEstado = document.createElement('td');
      const badge = document.createElement('span');
      badge.className = `badge ${activo ? 'badge-verde' : 'badge-gris'}`;
      badge.textContent = activo ? 'Activo' : 'Inactivo';
      tdEstado.appendChild(badge);

      const tdAccion = document.createElement('td');
      const btnEditar = document.createElement('button');
      btnEditar.className = 'btn-editar';
      btnEditar.dataset.id = usuario.idUsuario;
      btnEditar.textContent = 'Editar';
      tdAccion.appendChild(btnEditar);

      fila.append(tdNombre, tdRol, tdEstado, tdAccion);
      this.tablaBody.appendChild(fila);
    });
  }

  // --- ENLACES CON EL CONTROLADOR ---

  alEnviarFormulario(callback) {
    this.formulario.addEventListener('submit', (evento) => {
      evento.preventDefault();

      const rol = this.selectRol.value;
      callback({
        idUsuario: this.idEditando,                 // null = crear, número = actualizar
        nombre: this.inputNombre.value.trim(),
        credenciales: this.inputCredenciales.value, // '' al editar = no cambiar
        estado: this.selectEstado.value,
        rol: rol,
        datoRol: CONFIG_ROL[rol] ? this.inputDinamico.value.trim() : null
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
      if (confirm('¿Seguro que quieres eliminar este usuario?')) {
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