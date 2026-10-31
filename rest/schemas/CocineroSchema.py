from marshmallow import Schema, fields, validate


class CocineroSchema(Schema):
    # El id es opcional: si no se envía, el servicio asigna el siguiente
    id_cocinero = fields.Integer()
    estacion = fields.String(validate=validate.Length(max=45))
    Usuario_idUsuario = fields.Integer(required=True)
