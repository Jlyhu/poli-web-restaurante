from marshmallow import fields, validate
from rest.ext import ma


class CajaSchema(ma.Schema):
    id_caja = fields.Integer()             # opcional: si no se envía, el servicio asigna el siguiente
    monto_inicial = fields.Float(required=True, validate=validate.Range(min=0))
    Cajero_id_cajero = fields.Integer(required=True)    # el cajero debe existir

    # las fechas y el monto final NO se pueden enviar aquí:
    # la apertura se pone sola y el cierre se hace con /cerrarCaja
    fecha_apertura = fields.DateTime(dump_only=True)
    fecha_cierre = fields.DateTime(dump_only=True)
    monto_final = fields.Float(dump_only=True)


class CerrarCajaSchema(ma.Schema):
    monto_final = fields.Float(required=True, validate=validate.Range(min=0))
