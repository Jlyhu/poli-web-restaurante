# ============================================================
# mainService.py
# Servicio REST de Usuario (Flask)
# Registra automáticamente todos los archivos de rest/routes/ que terminen en
# 'Routes.py'
# ============================================================

import importlib
import pkgutil

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from rest import db, routes


app = Flask(__name__)

# Al terminar cada petición se cierra su sesión: así se libera la conexión
@app.teardown_appcontext
def cerrar_sesion(exception=None):
    db.session.remove()

# Errores de Flask
@app.errorhandler(HTTPException)
def manejar_excepcion(e):
    return jsonify({'error': e.description}), e.code

for modulo in pkgutil.iter_modules(routes.__path__):
    if modulo.name.endswith('Routes'):
        app.register_blueprint(importlib.import_module(f'rest.routes.{modulo.name}').bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

"""Punto de entrada de la API REST Flask.

Ejecutar desde la raíz del repositorio: python -m rest.mainService
"""
from flask import Flask, jsonify
from rest import db


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Importar aquí evita ciclos de importación y registra todos los modelos.
    from rest.modelos.AdministradorModel import Administrador  # noqa: F401
    from rest.modelos.CocineroModel import Cocinero  # noqa: F401
    from rest.modelos.DetallePedidoModel import DetallePedido  # noqa: F401
    from rest.modelos.PagoModel import Pago  # noqa: F401
    from rest.modelos.PedidoMesaModel import PedidoMesa  # noqa: F401

    from rest.routes.AdministradorRoutes import bp as administrador_bp
    from rest.routes.CocineroRoutes import bp as cocinero_bp
    from rest.routes.DetallePedidoRoutes import bp as detalle_pedido_bp
    from rest.routes.PagoRoutes import bp as pago_bp
    from rest.routes.PedidoMesaRoutes import bp as pedido_mesa_bp

    for blueprint in (administrador_bp, cocinero_bp, detalle_pedido_bp, pago_bp, pedido_mesa_bp):
        app.register_blueprint(blueprint)

    @app.get("/")
    def inicio():
        return jsonify({"servicio": "PoliRestaurante API", "estado": "activo"})

    @app.get("/health")
    def health():
        try:
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            return jsonify({"estado": "ok", "base_datos": "conectada"})
        except Exception:
            db.session.rollback()
            return jsonify({"estado": "error", "base_datos": "no disponible"}), 503

    @app.teardown_appcontext
    def cerrar_sesion(_exception=None):
        db.session.remove()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(__import__("os").getenv("PORT", "5000")), debug=False)
