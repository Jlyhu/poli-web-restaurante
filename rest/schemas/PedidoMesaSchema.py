from marshmallow import Schema, fields, validate


class PedidoMesaSchema(Schema):
    # El id es opcional: si no se envía, el servicio asigna el siguiente
    id_pedido_mesa = fields.Integer()
    Mesa_id_mesa = fields.Integer(required=True)
    Pedido_id_pedido = fields.Integer(required=True)
