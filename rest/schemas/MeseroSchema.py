from marshmallow import fields, validate
from rest.ext import ma


class MeseroSchema(ma.Schema):
    id_mesero = fields.Integer()           # opcional: si no se envía, el servicio asigna el siguiente
    zona_asignada = fields.String(allow_none=True, validate=validate.Length(max=45))
    Usuario_idUsuario = fields.Integer(required=True)   # el usuario debe existir
