from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.RepartidorModel import Repartidor
from rest.schemas.RepartidorSchema import RepartidorSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('repartidor', __name__)
repartidor_schema = RepartidorSchema()


# ---------- CONSULTAR ----------
@bp.route('/getRepartidores', methods=['GET'])
def repartidores():
    consulta = db.session.query(Repartidor)
    # opcional: /getRepartidores?usuario=5
    idusuario = request.args.get('usuario', type=int)
    if idusuario is not None:
        consulta = consulta.filter(Repartidor.Usuario_idUsuario == idusuario)
    mis = consulta.order_by(Repartidor.id_repartidor).all()
    return jsonify([x.toDict() for x in mis])


@bp.route('/getRepartidor/<int:idrepartidor>', methods=['GET'])
def repartidor(idrepartidor):
    x = db.session.get(Repartidor, idrepartidor)
    if x is None:
        return no_encontrada('un repartidor', idrepartidor)
    return jsonify(x.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertRepartidor', methods=['POST'])
def insertRepartidor():
    try:
        datos = repartidor_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idrepartidor = datos.get('id_repartidor')
    if idrepartidor is None:
        idrepartidor = siguiente_id(Repartidor.id_repartidor)

    x = Repartidor(id_repartidor=idrepartidor,
                   placa_vehiculo=datos.get('placa_vehiculo'),
                   Usuario_idUsuario=datos.get('Usuario_idUsuario'))
    db.session.add(x)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateRepartidor/<int:idrepartidor>', methods=['PUT'])
def updateRepartidor(idrepartidor):
    x = db.session.get(Repartidor, idrepartidor)
    if x is None:
        return no_encontrada('un repartidor', idrepartidor)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = repartidor_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_repartidor', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(x, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteRepartidor/<int:idrepartidor>', methods=['DELETE'])
def deleteRepartidor(idrepartidor):
    x = db.session.get(Repartidor, idrepartidor)
    if x is None:
        return no_encontrada('un repartidor', idrepartidor)

    db.session.delete(x)

    # Si un repartidor ya tiene registros relacionados la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Repartidor {idrepartidor} eliminado'})
