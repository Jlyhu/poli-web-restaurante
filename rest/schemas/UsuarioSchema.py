# ============================================================
# schemas.py
# Esquema de validación del JSON que llega para un Usuario
# ============================================================

from marshmallow import fields, validate
from rest.ext import ma


class UsuarioSchema(ma.Schema):
    # opcional: si no se envía, el servicio asigna el siguiente id disponible
    idUsuario = fields.Integer()

    # obligatorios al crear (en una edición pueden omitirse)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    credenciales = fields.String(required=True, load_only=True, validate=validate.Length(min=1, max=255))

    # el estado NO se puede enviar: solo cambia con /desactivarUsuario y /activarUsuario
    estado = fields.String(dump_only=True)
