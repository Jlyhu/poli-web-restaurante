from marshmallow import fields, validate
from rest.ext import ma


class RepartidorSchema(ma.Schema):
    id_repartidor = fields.Integer()       # opcional: si no se envía, el servicio asigna el siguiente
    placa_vehiculo = fields.String(allow_none=True, validate=validate.Length(max=45))
    Usuario_idUsuario = fields.Integer(required=True)   # el usuario debe existir
