# ============================================================
# mainService.py
# Servicio REST de PoliRestaurante (Flask)
# Registra automáticamente todos los archivos de rest/routes/ que terminen en 'Routes.py'
# Ejecutar desde la RAÍZ del repo:  python -m rest.mainService
# ============================================================

import importlib
import os
import pkgutil

from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text
from werkzeug.exceptions import HTTPException

from rest import db, routes


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    CORS(app)  # permite llamadas desde el cliente (Live Server, puerto 5500)

    # Al terminar cada petición se cierra su sesión: así se libera la conexión
    @app.teardown_appcontext
    def cerrar_sesion(_exception=None):
        db.session.remove()

    # Errores de Flask (404, 405, ...) siempre como JSON {"error": ...}
    @app.errorhandler(HTTPException)
    def manejar_excepcion(e):
        return jsonify({"error": e.description}), e.code

    # Registro automático: cualquier rest/routes/*Routes.py con un Blueprint llamado `bp`
    for modulo in pkgutil.iter_modules(routes.__path__):
        if modulo.name.endswith("Routes"):
            app.register_blueprint(importlib.import_module(f"rest.routes.{modulo.name}").bp)

    @app.get("/")
    def inicio():
        return jsonify({"servicio": "PoliRestaurante API", "estado": "activo"})

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"estado": "ok", "base_datos": "conectada"})
        except Exception:
            db.session.rollback()
            return jsonify({"estado": "error", "base_datos": "no disponible"}), 503

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
