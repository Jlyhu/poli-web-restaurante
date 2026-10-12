from marshmallow import fields, validate
from rest.ext import ma


class ReservacionSchema(ma.Schema):
    id_reservacion = fields.Integer()          # opcional: si no se envía, el servicio asigna el siguiente
    fecha = fields.Date(required=True)          # formato AAAA-MM-DD
    hora = fields.Time(required=True)           # formato HH:MM
    numero_personas = fields.Integer(required=True, validate=validate.Range(min=1))
    estado = fields.String(validate=validate.Length(min=1, max=45))
    Cliente_id_cliente = fields.Integer(required=True)   # el cliente debe existir
