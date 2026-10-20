from marshmallow import fields, validate
from rest.ext import ma


class ProductoSchema(ma.Schema):
    idProducto = fields.Integer()          # opcional: si no se envía, el servicio asigna el siguiente
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    descripcion = fields.String(allow_none=True, validate=validate.Length(max=100))
    precio = fields.Float(required=True, validate=validate.Range(min=0))
    cantidad_disponible = fields.Integer(validate=validate.Range(min=0))
    Categoria_id_categoria = fields.Integer(required=True)   # la categoría debe existir
