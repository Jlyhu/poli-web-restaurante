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

