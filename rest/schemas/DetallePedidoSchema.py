from marshmallow import Schema, fields, validate


class DetallePedidoSchema(Schema):
    # El id es opcional: si no se envía, el servicio asigna el siguiente
    id_detalle_pedido = fields.Integer()
    cantidad = fields.Integer(required=True, validate=validate.Range(min=1))
    notas = fields.String(validate=validate.Length(max=120))
    Pedido_id_pedido = fields.Integer(required=True)
    Producto_idProducto = fields.Integer(required=True)
