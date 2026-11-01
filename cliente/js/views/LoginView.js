/**
 * LoginView.js (VISTA)
 * Único archivo que toca el DOM en el inicio de sesión.
 */
export class LoginView {
  constructor() {
    this.inputNombre = document.querySelector('#input-nombre');
    this.inputContrasena = document.querySelector('#input-contrasena');
    this.btnIniciar = document.querySelector('#btn-iniciar-sesion');
  }

  /** Aviso flotante que desaparece solo. tipo: 'exito' | 'error' */
  mostrarMensaje(texto, tipo = 'exito') {
    const aviso = document.createElement('div');
    aviso.className = `mensaje mensaje-${tipo}`;
    aviso.textContent = texto;
    document.body.appendChild(aviso);
    setTimeout(() => aviso.remove(), 4000);
  }

  /** Bloquea el botón mientras se espera al servidor. */
  bloquearFormulario(bloquear) {
    this.btnIniciar.disabled = bloquear;
  }

  /** Redirige a otra página. */
  irA(pagina) {
    window.location.href = pagina;
  }

  alIniciarSesion(callback) {
    const enviar = () => callback({
      nombre: this.inputNombre.value.trim(),
      credenciales: this.inputContrasena.value
    });
    this.btnIniciar.addEventListener('click', enviar);
    // Enter dentro de los campos también envía
    [this.inputNombre, this.inputContrasena].forEach((input) =>
      input.addEventListener('keydown', (evento) => {
        if (evento.key === 'Enter') enviar();
      })
    );
  }
}