from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.ReservacionMesaModel import ReservacionMesa
from rest.schemas.ReservacionMesaSchema import ReservacionMesaSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('reservacion_mesa', __name__)
reservacion_mesa_schema = ReservacionMesaSchema()


# ---------- CONSULTAR ----------
@bp.route('/getReservacionesMesa', methods=['GET'])
def reservacionesMesa():
    # opcional: /getReservacionesMesa?reservacion=20
    consulta = db.session.query(ReservacionMesa)
    idreservacion = request.args.get('reservacion', type=int)
    if idreservacion is not None:
        consulta = consulta.filter(ReservacionMesa.Reservacion_id_reservacion == idreservacion)
    misRM = consulta.order_by(ReservacionMesa.id_reservacion_mesa).all()
    return jsonify([rm.toDict() for rm in misRM])


@bp.route('/getReservacionMesa/<int:idreservacionmesa>', methods=['GET'])
def reservacionMesa(idreservacionmesa):
    rm = db.session.get(ReservacionMesa, idreservacionmesa)
    if rm is None:
        return no_encontrada('un registro de reservación-mesa', idreservacionmesa)
    return jsonify(rm.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertReservacionMesa', methods=['POST'])
def insertReservacionMesa():
    try:
        datos = reservacion_mesa_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idreservacionmesa = datos.get('id_reservacion_mesa')
    if idreservacionmesa is None:
        idreservacionmesa = siguiente_id(ReservacionMesa.id_reservacion_mesa)

    rm = ReservacionMesa(id_reservacion_mesa=idreservacionmesa,
                         Mesa_id_mesa=datos.get('Mesa_id_mesa'),
                         Reservacion_id_reservacion=datos.get('Reservacion_id_reservacion'))
    db.session.add(rm)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(rm.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateReservacionMesa/<int:idreservacionmesa>', methods=['PUT'])
def updateReservacionMesa(idreservacionmesa):
    rm = db.session.get(ReservacionMesa, idreservacionmesa)
    if rm is None:
        return no_encontrada('un registro de reservación-mesa', idreservacionmesa)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = reservacion_mesa_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_reservacion_mesa', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(rm, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(rm.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteReservacionMesa/<int:idreservacionmesa>', methods=['DELETE'])
def deleteReservacionMesa(idreservacionmesa):
    rm = db.session.get(ReservacionMesa, idreservacionmesa)
    if rm is None:
        return no_encontrada('un registro de reservación-mesa', idreservacionmesa)

    db.session.delete(rm)

    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Registro {idreservacionmesa} eliminado'})
