from marshmallow import fields, validate
from rest.ext import ma


class ClienteSchema(ma.Schema):
    id_cliente = fields.Integer()          # opcional: si no se envía, el servicio asigna el siguiente
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=45))
    direccion = fields.String(allow_none=True, validate=validate.Length(max=45))
    telefono = fields.String(allow_none=True, validate=validate.Length(max=45))
