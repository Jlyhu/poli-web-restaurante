from marshmallow import Schema, fields, validate


class AdministradorSchema(Schema):
    # El id es opcional: si no se envía, el servicio asigna el siguiente
    id_administrador = fields.Integer()
    Usuario_idUsuario = fields.Integer(required=True)
