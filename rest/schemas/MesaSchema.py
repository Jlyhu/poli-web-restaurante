from marshmallow import fields, validate
from rest.ext import ma


class MesaSchema(ma.Schema):
    id_mesa = fields.Integer()          # opcional: si no se envía, el servicio asigna el siguiente
    numero = fields.Integer(required=True, validate=validate.Range(min=1))
    estado = fields.String(validate=validate.Length(min=1, max=45))
