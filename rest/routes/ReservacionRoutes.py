from datetime import datetime, time

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.ReservacionModel import Reservacion
from rest.schemas.ReservacionSchema import ReservacionSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('reservacion', __name__)
reservacion_schema = ReservacionSchema()


# ---------- CONSULTAR ----------
@bp.route('/getReservaciones', methods=['GET'])
def reservaciones():
    # opcional: /getReservaciones?cliente=20
    consulta = db.session.query(Reservacion)
    idcliente = request.args.get('cliente', type=int)
    if idcliente is not None:
        consulta = consulta.filter(Reservacion.Cliente_id_cliente == idcliente)
    misR = consulta.order_by(Reservacion.id_reservacion).all()
    return jsonify([r.toDict() for r in misR])


@bp.route('/getReservacion/<int:idreservacion>', methods=['GET'])
def reservacion(idreservacion):
    r = db.session.get(Reservacion, idreservacion)
    if r is None:
        return no_encontrada('una reservación', idreservacion)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertReservacion', methods=['POST'])
def insertReservacion():
    try:
        datos = reservacion_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idreservacion = datos.get('id_reservacion')
    if idreservacion is None:
        idreservacion = siguiente_id(Reservacion.id_reservacion)

    # fecha y hora son columnas DATETIME: la hora se guarda junto con la fecha
    r = Reservacion(id_reservacion=idreservacion,
                    fecha=datetime.combine(datos['fecha'], time.min),
                    hora=datetime.combine(datos['fecha'], datos['hora']),
                    numero_personas=datos.get('numero_personas'),
                    estado=datos.get('estado', 'Pendiente'),
                    Cliente_id_cliente=datos.get('Cliente_id_cliente'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateReservacion/<int:idreservacion>', methods=['PUT'])
def updateReservacion(idreservacion):
    r = db.session.get(Reservacion, idreservacion)
    if r is None:
        return no_encontrada('una reservación', idreservacion)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = reservacion_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_reservacion', None)   # la llave primaria no se modifica

    # si cambia la fecha o la hora, se vuelven a armar las dos columnas DATETIME
    fecha_nueva = datos.pop('fecha', None)
    hora_nueva = datos.pop('hora', None)
    if fecha_nueva or hora_nueva:
        fecha_base = fecha_nueva or (r.fecha.date() if r.fecha else None)
        hora_base = hora_nueva or (r.hora.time() if r.hora else time.min)
        if fecha_base is None:
            return jsonify({'error': 'La reservación no tiene fecha: envía también la fecha'}), 400
        r.fecha = datetime.combine(fecha_base, time.min)
        r.hora = datetime.combine(fecha_base, hora_base)

    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteReservacion/<int:idreservacion>', methods=['DELETE'])
def deleteReservacion(idreservacion):
    r = db.session.get(Reservacion, idreservacion)
    if r is None:
        return no_encontrada('una reservación', idreservacion)

    db.session.delete(r)

    # Si la reservación ya tiene mesas asignadas la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Reservación {idreservacion} eliminada'})
