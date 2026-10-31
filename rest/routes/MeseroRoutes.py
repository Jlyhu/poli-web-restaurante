from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.MeseroModel import Mesero
from rest.schemas.MeseroSchema import MeseroSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('mesero', __name__)
mesero_schema = MeseroSchema()


# ---------- CONSULTAR ----------
@bp.route('/getMeseros', methods=['GET'])
def meseros():
    consulta = db.session.query(Mesero)
    # opcional: /getMeseros?usuario=5
    idusuario = request.args.get('usuario', type=int)
    if idusuario is not None:
        consulta = consulta.filter(Mesero.Usuario_idUsuario == idusuario)
    mis = consulta.order_by(Mesero.id_mesero).all()
    return jsonify([x.toDict() for x in mis])


@bp.route('/getMesero/<int:idmesero>', methods=['GET'])
def mesero(idmesero):
    x = db.session.get(Mesero, idmesero)
    if x is None:
        return no_encontrada('un mesero', idmesero)
    return jsonify(x.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertMesero', methods=['POST'])
def insertMesero():
    try:
        datos = mesero_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idmesero = datos.get('id_mesero')
    if idmesero is None:
        idmesero = siguiente_id(Mesero.id_mesero)

    x = Mesero(id_mesero=idmesero,
               zona_asignada=datos.get('zona_asignada'),
               Usuario_idUsuario=datos.get('Usuario_idUsuario'))
    db.session.add(x)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateMesero/<int:idmesero>', methods=['PUT'])
def updateMesero(idmesero):
    x = db.session.get(Mesero, idmesero)
    if x is None:
        return no_encontrada('un mesero', idmesero)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = mesero_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_mesero', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(x, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(x.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteMesero/<int:idmesero>', methods=['DELETE'])
def deleteMesero(idmesero):
    x = db.session.get(Mesero, idmesero)
    if x is None:
        return no_encontrada('un mesero', idmesero)

    db.session.delete(x)

    # Si un mesero ya tiene registros relacionados la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Mesero {idmesero} eliminado'})
