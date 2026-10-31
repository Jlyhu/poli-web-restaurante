from marshmallow import fields, validate
from rest.ext import ma


class CategoriaSchema(ma.Schema):
    id_categoria = fields.Integer()        # opcional: si no se envía, el servicio asigna el siguiente
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
