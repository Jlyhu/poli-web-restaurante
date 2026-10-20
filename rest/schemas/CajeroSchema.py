from marshmallow import fields, validate
from rest.ext import ma


class CajeroSchema(ma.Schema):
    id_cajero = fields.Integer()           # opcional: si no se envía, el servicio asigna el siguiente
    Usuario_idUsuario = fields.Integer(required=True)   # el usuario debe existir
