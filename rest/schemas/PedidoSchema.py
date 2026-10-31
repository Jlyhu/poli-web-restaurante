from marshmallow import fields, validate
from rest.ext import ma


ESTADOS = ['PENDIENTE', 'EN PREPARACION', 'LISTO', 'ENTREGADO', 'CANCELADO']


class PedidoSchema(ma.Schema):
    id_pedido = fields.Integer()           # opcional: si no se envía, el servicio asigna el siguiente
    tipo_pedido = fields.String(required=True, validate=validate.Length(min=1, max=45))

    # opcionales: no todo pedido tiene mesero, repartidor y cliente (si se envían, deben existir)
    Mesero_id_mesero = fields.Integer(allow_none=True)
    Repartidor_id_repartidor = fields.Integer(allow_none=True)
    Cliente_id_cliente = fields.Integer(allow_none=True)

    # el estado y las fechas NO se pueden enviar aquí:
    # el pedido nace PENDIENTE y el estado solo cambia con /cambiarEstadoPedido
    estado = fields.String(dump_only=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_ultima_actualizacion = fields.DateTime(dump_only=True)


class CambiarEstadoPedidoSchema(ma.Schema):
    estado = fields.String(required=True, validate=validate.OneOf(ESTADOS))
