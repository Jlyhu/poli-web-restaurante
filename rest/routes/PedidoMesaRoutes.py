from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError, Schema, fields

from rest import db
from rest.modelos.MesaModel import Mesa
from rest.modelos.PedidoMesaModel import PedidoMesa
from rest.modelos.PedidoModel import Pedido
from rest.schemas.PedidoMesaSchema import PedidoMesaSchema
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('pedidomesa', __name__)
esquema = PedidoMesaSchema()

# Un pedido sigue "activo" (ocupa su mesa) hasta que se entrega o se cancela
ESTADOS_ACTIVOS = ['PENDIENTE', 'EN PREPARACION', 'LISTO']


class CrearPedidoMesaSchema(Schema):
    Mesa_id_mesa = fields.Integer(required=True)
    Mesero_id_mesero = fields.Integer(allow_none=True)


def _pedido_activo_de_mesa(id_mesa):
    """Devuelve el pedido activo de la mesa o None."""
    return (db.session.query(Pedido)
            .join(PedidoMesa, PedidoMesa.Pedido_id_pedido == Pedido.id_pedido)
            .filter(PedidoMesa.Mesa_id_mesa == id_mesa, Pedido.estado.in_(ESTADOS_ACTIVOS))
            .first())


# ---------- HU-02: MESAS CON SU DISPONIBILIDAD ----------
# Una mesa está ocupada si tiene un pedido activo (no entregado ni cancelado).
@bp.route('/getMesasDisponibilidad', methods=['GET'])
def mesas_disponibilidad():
    resultado = []
    for m in db.session.query(Mesa).order_by(Mesa.numero, Mesa.id_mesa).all():
        activo = _pedido_activo_de_mesa(m.id_mesa)
        resultado.append({'id_mesa': m.id_mesa,
                          'numero': m.numero,
                          'disponible': activo is None,
                          'id_pedido_activo': activo.id_pedido if activo else None})
    return jsonify(resultado)


# ---------- HU-02 / HU-08 / HU-09: PEDIDOS CON EL NÚMERO DE SU MESA ----------
# /getPedidosConMesa                      -> todos
# /getPedidosConMesa?estado=PENDIENTE     -> filtrados por estado
# /getPedidosConMesa?activos=1            -> PENDIENTE, EN PREPARACION y LISTO
# Siempre se devuelven del más antiguo al más reciente.
@bp.route('/getPedidosConMesa', methods=['GET'])
def pedidos_con_mesa():
    consulta = (db.session.query(Pedido, Mesa)
                .select_from(Pedido)
                .outerjoin(PedidoMesa, PedidoMesa.Pedido_id_pedido == Pedido.id_pedido)
                .outerjoin(Mesa, Mesa.id_mesa == PedidoMesa.Mesa_id_mesa))
    estado = request.args.get('estado')
    if estado:
        consulta = consulta.filter(Pedido.estado == estado)
    if request.args.get('activos') in ('1', 'true', 'si'):
        consulta = consulta.filter(Pedido.estado.in_(ESTADOS_ACTIVOS))
    filas = consulta.order_by(Pedido.fecha_creacion, Pedido.id_pedido).all()
    return jsonify([{**p.toDict(),
                     'id_mesa': m.id_mesa if m else None,
                     'numero_mesa': m.numero if m else None} for p, m in filas])


# ---------- HU-02: CREAR PEDIDO PARA UNA MESA ----------
# Crea el Pedido (PENDIENTE) y su PedidoMesa en una sola transacción:
# o se guardan los dos o no se guarda ninguno.
@bp.route('/crearPedidoMesa', methods=['POST'])
def crear_pedido_mesa():
    try:
        datos = CrearPedidoMesaSchema().load(request.get_json(silent=True) or {})
    except ValidationError as err:
        # Mesa sin seleccionar -> mensaje claro (criterio de aceptación de HU-02)
        if 'Mesa_id_mesa' in err.messages:
            return jsonify({'error': 'Debe seleccionar una mesa antes de continuar.'}), 400
        return jsonify(err.messages), 400

    id_mesa = datos['Mesa_id_mesa']
    mesa = db.session.get(Mesa, id_mesa)
    if mesa is None:
        return no_encontrada('una mesa', id_mesa)

    activo = _pedido_activo_de_mesa(id_mesa)
    if activo is not None:
        return jsonify({'error': f'La mesa {mesa.numero} ya tiene un pedido activo '
                                 f'(pedido {activo.id_pedido}, {activo.estado}).'}), 409

    ahora = datetime.now()
    id_pedido = siguiente_id(Pedido.id_pedido)
    pedido = Pedido(id_pedido=id_pedido,
                    estado='PENDIENTE',
                    fecha_creacion=ahora,
                    fecha_ultima_actualizacion=ahora,
                    tipo_pedido='mesa',
                    Mesero_id_mesero=datos.get('Mesero_id_mesero'))
    db.session.add(pedido)
    db.session.flush()   # el pedido debe existir antes de enlazarlo con la mesa (llave foránea)

    db.session.add(PedidoMesa(id_pedido_mesa=siguiente_id(PedidoMesa.id_pedido_mesa),
                              Mesa_id_mesa=id_mesa,
                              Pedido_id_pedido=id_pedido))

    error = guardar_cambios()
    if error:
        return error
    return jsonify({**pedido.toDict(), 'id_mesa': id_mesa, 'numero_mesa': mesa.numero}), 201


# ---------- CONSULTAR ----------
@bp.route('/getPedidosMesa', methods=['GET'])
def listar():
    registros = db.session.query(PedidoMesa).order_by(PedidoMesa.id_pedido_mesa).all()
    return jsonify([r.toDict() for r in registros])


@bp.route('/getPedidoMesa/<int:id_pedido_mesa>', methods=['GET'])
def obtener(id_pedido_mesa):
    r = db.session.get(PedidoMesa, id_pedido_mesa)
    if r is None:
        return no_encontrada('un pedido de mesa', id_pedido_mesa)
    return jsonify(r.toDict())


# ---------- INSERTAR ----------
@bp.route('/insertPedidoMesa', methods=['POST'])
def insertar():
    try:
        datos = esquema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    nuevo_id = datos.get('id_pedido_mesa')
    if nuevo_id is None:
        nuevo_id = siguiente_id(PedidoMesa.id_pedido_mesa)

    r = PedidoMesa(id_pedido_mesa=nuevo_id,
            Mesa_id_mesa=datos.get('Mesa_id_mesa'),
            Pedido_id_pedido=datos.get('Pedido_id_pedido'))
    db.session.add(r)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict()), 201


# ---------- ACTUALIZAR ----------
@bp.route('/updatePedidoMesa/<int:id_pedido_mesa>', methods=['PUT'])
def actualizar(id_pedido_mesa):
    r = db.session.get(PedidoMesa, id_pedido_mesa)
    if r is None:
        return no_encontrada('un pedido de mesa', id_pedido_mesa)

    try:
        # partial=True: basta con enviar los campos que se quieren cambiar
        datos = esquema.load(request.get_json(silent=True) or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    datos.pop('id_pedido_mesa', None)   # la llave primaria no se modifica
    for campo, valor in datos.items():
        setattr(r, campo, valor)

    error = guardar_cambios()
    if error:
        return error
    return jsonify(r.toDict())


# ---------- ELIMINAR ----------
@bp.route('/deletePedidoMesa/<int:id_pedido_mesa>', methods=['DELETE'])
def eliminar(id_pedido_mesa):
    r = db.session.get(PedidoMesa, id_pedido_mesa)
    if r is None:
        return no_encontrada('un pedido de mesa', id_pedido_mesa)

    db.session.delete(r)

    # Si otros registros dependen de este, la base lo impide
    error = guardar_cambios()
    if error:
        return error
    return jsonify({'mensaje': f'PedidoMesa {id_pedido_mesa} eliminado'})
