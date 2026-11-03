# ============================================================
# SeguimientoRoutes.py  (Daniela)
# HU-05 Consultar estado del pedido     (Mesero)
# HU-06 Entregar pedido                 (Mesero / Repartidor)
# HU-07 Cancelar pedido                 (Mesero)
# HU-15 Consultar trazabilidad          (Administrador)
# + pantallas de Cajero (caja y pagos) y Repartidor (entregas)
#
# Entidades: Pedido, Mesero, Usuario, Repartidor, Cliente, Cajero, Caja, Pago
# Este archivo se registra solo (mainService.py carga todos los *Routes.py).
# ============================================================

from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import Schema, ValidationError, fields, validate
from sqlalchemy import func

from rest import db
from rest.modelos.CajaModel import Caja
from rest.modelos.CajeroModel import Cajero
from rest.modelos.ClienteModel import Cliente
from rest.modelos.DetallePedidoModel import DetallePedido
from rest.modelos.MesaModel import Mesa
from rest.modelos.MeseroModel import Mesero
from rest.modelos.PagoModel import Pago
from rest.modelos.PedidoMesaModel import PedidoMesa
from rest.modelos.PedidoModel import Pedido
from rest.modelos.ProductoModel import Producto
from rest.modelos.RepartidorModel import Repartidor
from rest.modelos.UsuarioModel import Usuario
from rest.utils import guardar_cambios, no_encontrada, siguiente_id

bp = Blueprint('seguimiento', __name__)

ESTADOS_ACTIVOS = ['PENDIENTE', 'EN PREPARACION', 'LISTO']
METODOS_PAGO = ['Efectivo', 'Tarjeta', 'Transferencia']


def _error(mensaje, codigo):
    return jsonify({'error': mensaje}), codigo


def _fecha(valor):
    return valor.strftime('%Y-%m-%d %H:%M:%S') if valor else None


def _minutos(desde, hasta):
    if not desde or not hasta:
        return None
    return round((hasta - desde).total_seconds() / 60)


def _total_pedido(id_pedido):
    """Suma cantidad x precio de los renglones del pedido."""
    total = (db.session.query(func.sum(DetallePedido.cantidad * Producto.precio))
             .join(Producto, Producto.idProducto == DetallePedido.Producto_idProducto)
             .filter(DetallePedido.Pedido_id_pedido == id_pedido)
             .scalar())
    return float(total or 0)


def _pedido_completo(p):
    """Pedido + mesa + mesero + repartidor + cliente + total + pago, listo para el cliente web."""
    mesa = (db.session.query(Mesa)
            .join(PedidoMesa, PedidoMesa.Mesa_id_mesa == Mesa.id_mesa)
            .filter(PedidoMesa.Pedido_id_pedido == p.id_pedido)
            .first())

    nombre_mesero = None
    if p.Mesero_id_mesero is not None:
        fila = (db.session.query(Usuario.nombre)
                .join(Mesero, Mesero.Usuario_idUsuario == Usuario.idUsuario)
                .filter(Mesero.id_mesero == p.Mesero_id_mesero).first())
        nombre_mesero = fila[0] if fila else None

    nombre_repartidor = None
    if p.Repartidor_id_repartidor is not None:
        fila = (db.session.query(Usuario.nombre)
                .join(Repartidor, Repartidor.Usuario_idUsuario == Usuario.idUsuario)
                .filter(Repartidor.id_repartidor == p.Repartidor_id_repartidor).first())
        nombre_repartidor = fila[0] if fila else None

    cliente = db.session.get(Cliente, p.Cliente_id_cliente) if p.Cliente_id_cliente else None
    pago = db.session.query(Pago).filter(Pago.Pedido_id_pedido == p.id_pedido).first()

    return {**p.toDict(),
            'estado': (p.estado or '').upper(),
            'id_mesa': mesa.id_mesa if mesa else None,
            'numero_mesa': mesa.numero if mesa else None,
            'nombre_mesero': nombre_mesero,
            'nombre_repartidor': nombre_repartidor,
            'cliente_nombre': cliente.nombre if cliente else None,
            'cliente_direccion': cliente.direccion if cliente else None,
            'cliente_telefono': cliente.telefono if cliente else None,
            'total': _total_pedido(p.id_pedido),
            'pagado': pago is not None,
            'fecha_pago': _fecha(pago.fecha_pago) if pago else None,
            'metodo_pago': pago.metodo_pago if pago else None,
            'minutos_transcurridos': _minutos(p.fecha_creacion, p.fecha_ultima_actualizacion)}


# ---------- HU-05 / HU-15 / Cajero / Repartidor: PEDIDOS CON TODOS SUS DATOS ----------
# /getPedidosDetallados                     -> todos (más reciente primero)
#   ?estado=LISTO        ?activos=1          ?mesero=9101
#   ?repartidor=9101     ?tipo=domicilio     ?sinPago=1
@bp.route('/getPedidosDetallados', methods=['GET'])
def pedidos_detallados():
    consulta = db.session.query(Pedido)
    estado = request.args.get('estado')
    if estado:
        consulta = consulta.filter(func.upper(Pedido.estado) == estado.upper())
    if request.args.get('activos') in ('1', 'true', 'si'):
        consulta = consulta.filter(func.upper(Pedido.estado).in_(ESTADOS_ACTIVOS))
    idmesero = request.args.get('mesero', type=int)
    if idmesero is not None:
        consulta = consulta.filter(Pedido.Mesero_id_mesero == idmesero)
    idrepartidor = request.args.get('repartidor', type=int)
    if idrepartidor is not None:
        consulta = consulta.filter(Pedido.Repartidor_id_repartidor == idrepartidor)
    tipo = request.args.get('tipo')
    if tipo:
        consulta = consulta.filter(func.lower(Pedido.tipo_pedido) == tipo.lower())

    resultado = [_pedido_completo(p) for p in
                 consulta.order_by(Pedido.fecha_creacion.desc(), Pedido.id_pedido.desc()).all()]
    if request.args.get('sinPago') in ('1', 'true', 'si'):
        resultado = [r for r in resultado if not r['pagado']]
    return jsonify(resultado)


# ---------- HU-05: ESTADO DE UN PEDIDO ----------
@bp.route('/getEstadoPedido/<int:idpedido>', methods=['GET'])
def estado_pedido(idpedido):
    p = db.session.get(Pedido, idpedido)
    if p is None:
        return no_encontrada('un pedido', idpedido)
    return jsonify(_pedido_completo(p))


# ---------- HU-15: TRAZABILIDAD DE UN PEDIDO ----------
# Estado actual, fechas (creación, última actualización, pago) y tiempos.
@bp.route('/getTrazabilidadPedido/<int:idpedido>', methods=['GET'])
def trazabilidad_pedido(idpedido):
    p = db.session.get(Pedido, idpedido)
    if p is None:
        return no_encontrada('un pedido', idpedido)
    datos = _pedido_completo(p)
    estado = datos['estado']

    eventos = [{'evento': 'Pedido creado (PENDIENTE)', 'fecha': _fecha(p.fecha_creacion)}]
    if estado != 'PENDIENTE' and p.fecha_ultima_actualizacion:
        eventos.append({'evento': f'Último cambio de estado: {estado}',
                        'fecha': _fecha(p.fecha_ultima_actualizacion)})
    if datos['pagado']:
        eventos.append({'evento': f"Pago registrado ({datos['metodo_pago']})",
                        'fecha': datos['fecha_pago']})

    fin = p.fecha_ultima_actualizacion if estado in ('ENTREGADO', 'CANCELADO') else datetime.now()
    datos['eventos'] = eventos
    datos['minutos_abierto'] = _minutos(p.fecha_creacion, fin)
    return jsonify(datos)


# ---------- HU-06 y HU-07: ENTREGAR Y CANCELAR ----------
def _cambiar(idpedido, nuevo, permitidos_desde):
    p = db.session.get(Pedido, idpedido)
    if p is None:
        return no_encontrada('un pedido', idpedido)
    actual = (p.estado or '').upper()
    if actual not in permitidos_desde:
        return _error(f'El pedido {idpedido} está {actual}: solo se puede pasar a {nuevo} '
                      f'desde {" o ".join(permitidos_desde)}.', 409)
    p.estado = nuevo
    p.fecha_ultima_actualizacion = datetime.now()
    error = guardar_cambios()
    if error:
        return error
    return jsonify(_pedido_completo(p))


@bp.route('/entregarPedido/<int:idpedido>', methods=['PUT'])
def entregar_pedido(idpedido):
    # HU-06: solo un pedido LISTO (ya preparado por cocina) se puede entregar
    return _cambiar(idpedido, 'ENTREGADO', ['LISTO'])


@bp.route('/cancelarPedido/<int:idpedido>', methods=['PUT'])
def cancelar_pedido(idpedido):
    # HU-07: se puede anular mientras no esté listo ni entregado
    return _cambiar(idpedido, 'CANCELADO', ['PENDIENTE', 'EN PREPARACION'])


# ---------- CAJERO: CAJA ----------
class AbrirCajaSchema(Schema):
    Cajero_id_cajero = fields.Integer(required=True)
    monto_inicial = fields.Float(required=True, validate=validate.Range(min=0))


def _caja_abierta(idcajero):
    return (db.session.query(Caja)
            .filter(Caja.Cajero_id_cajero == idcajero, Caja.fecha_cierre.is_(None))
            .order_by(Caja.id_caja.desc()).first())


def _resumen_caja(c):
    pagos = db.session.query(Pago).filter(Pago.Caja_id_caja == c.id_caja).order_by(Pago.fecha_pago).all()
    recaudado = sum(float(x.monto or 0) for x in pagos)
    return {**c.toDict(),
            'abierta': c.fecha_cierre is None,
            'recaudado': recaudado,
            'esperado': float(c.monto_inicial or 0) + recaudado,
            'pagos': [x.toDict() for x in pagos]}


@bp.route('/getCajaAbierta', methods=['GET'])
def caja_abierta():
    # /getCajaAbierta?cajero=9101  -> la caja sin cerrar de ese cajero (o null)
    idcajero = request.args.get('cajero', type=int)
    if idcajero is None:
        return _error('Indique el cajero: /getCajaAbierta?cajero=<id>', 400)
    c = _caja_abierta(idcajero)
    return jsonify(_resumen_caja(c) if c else None)


@bp.route('/abrirCaja', methods=['POST'])
def abrir_caja():
    try:
        datos = AbrirCajaSchema().load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400
    idcajero = datos['Cajero_id_cajero']
    if db.session.get(Cajero, idcajero) is None:
        return no_encontrada('un cajero', idcajero)
    if _caja_abierta(idcajero) is not None:
        return _error('Este cajero ya tiene una caja abierta. Ciérrela antes de abrir otra.', 409)

    c = Caja(id_caja=siguiente_id(Caja.id_caja), fecha_apertura=datetime.now(),
             monto_inicial=datos['monto_inicial'], Cajero_id_cajero=idcajero)
    db.session.add(c)
    error = guardar_cambios()
    if error:
        return error
    return jsonify(_resumen_caja(c)), 201


# ---------- CAJERO: REGISTRAR PAGO ----------
class RegistrarPagoSchema(Schema):
    Pedido_id_pedido = fields.Integer(required=True)
    Cajero_id_cajero = fields.Integer(required=True)
    metodo_pago = fields.String(required=True, validate=validate.OneOf(METODOS_PAGO))


@bp.route('/registrarPagoPedido', methods=['POST'])
def registrar_pago():
    # El monto lo calcula el servidor con el detalle del pedido (no se confía en el navegador)
    try:
        datos = RegistrarPagoSchema().load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    idpedido = datos['Pedido_id_pedido']
    p = db.session.get(Pedido, idpedido)
    if p is None:
        return no_encontrada('un pedido', idpedido)
    if (p.estado or '').upper() != 'ENTREGADO':
        return _error(f'Solo se cobran pedidos ENTREGADOS (el pedido {idpedido} está {p.estado}).', 409)
    if db.session.query(Pago).filter(Pago.Pedido_id_pedido == idpedido).first():
        return _error(f'El pedido {idpedido} ya tiene un pago registrado.', 409)

    caja = _caja_abierta(datos['Cajero_id_cajero'])
    if caja is None:
        return _error('No tiene una caja abierta. Abra la caja antes de registrar pagos.', 409)

    monto = _total_pedido(idpedido)
    if monto <= 0:
        return _error(f'El pedido {idpedido} no tiene productos: no hay nada que cobrar.', 409)

    pago = Pago(id_pago=siguiente_id(Pago.id_pago), monto=monto, metodo_pago=datos['metodo_pago'],
                fecha_pago=datetime.now(), Pedido_id_pedido=idpedido, Caja_id_caja=caja.id_caja)
    db.session.add(pago)
    error = guardar_cambios()
    if error:
        return error
    return jsonify(pago.toDict()), 201
