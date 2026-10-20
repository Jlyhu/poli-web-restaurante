from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from rest import db
from rest.modelos.ClienteModel import Cliente
from rest.schemas.ClienteSchema import ClienteSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('cliente', __name__)
cliente_schema = ClienteSchema()


# ---------- CONSULTAR ----------
@bp.route('/getClientes', methods=['GET'])
def clientes():
    misC = db.session.query(Cliente).order_by(Cliente.id_cliente).all()
    return jsonify([c.toDict() for c in misC])


@bp.route('/getCliente/<int:idcliente>', methods=['GET'])
def cliente(idcliente):
    c = db.session.get(Cliente, idcliente)
    if c is None:
        return no_encontrada('un cliente', idcliente)
    return jsonify(c.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertCliente', methods=['POST'])
def insertCliente():
    try:
        datos = cliente_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    idcliente = datos.get('id_cliente')
    if idcliente is None:
        idcliente = siguiente_id(Cliente.id_cliente)

    c = Cliente(id_cliente=idcliente,
                nombre=datos.get('nombre'),
                direccion=datos.get('direccion'),
                telefono=datos.get('telefono'))
    db.session.add(c)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(c.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updateCliente/<int:idcliente>', methods=['PUT'])
def updateCliente(idcliente):
    c = db.session.get(Cliente, idcliente)
    if c is None:
        return no_encontrada('un cliente', idcliente)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = cliente_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_cliente', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(c, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(c.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deleteCliente/<int:idcliente>', methods=['DELETE'])
def deleteCliente(idcliente):
    c = db.session.get(Cliente, idcliente)
    if c is None:
        return no_encontrada('un cliente', idcliente)

    db.session.delete(c)

    # Si el cliente ya tiene reservaciones o pedidos la base lo impide (409)
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'Cliente {idcliente} eliminado'})
