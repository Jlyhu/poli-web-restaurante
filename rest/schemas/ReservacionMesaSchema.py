from marshmallow import fields
from rest.ext import ma


class ReservacionMesaSchema(ma.Schema):
    id_reservacion_mesa = fields.Integer()          # opcional: si no se envía, el servicio asigna el siguiente
    Mesa_id_mesa = fields.Integer(required=True)                # la mesa debe existir
    Reservacion_id_reservacion = fields.Integer(required=True)  # la reservación debe existir
