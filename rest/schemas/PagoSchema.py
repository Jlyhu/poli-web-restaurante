from marshmallow import Schema, fields, validate


class PagoSchema(Schema):
    # El id es opcional: si no se envía, el servicio asigna el siguiente
    id_pago = fields.Integer()
    monto = fields.Float(required=True, validate=validate.Range(min=0))
    metodo_pago = fields.String(required=True, validate=validate.Length(max=45))
    fecha_pago = fields.DateTime()
    Pedido_id_pedido = fields.Integer(required=True)
    Caja_id_caja = fields.Integer(required=True)
