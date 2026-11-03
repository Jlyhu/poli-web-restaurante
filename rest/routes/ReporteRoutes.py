"""HU-14: reportes administrativos (ventas y tiempos de preparación).

Solo los puede consultar un administrador: el servicio exige el parámetro
`administrador=<id_administrador>` y comprueba que exista en la tabla Administrador.
(Cuando el login guarde la sesión, el cliente enviará ese id automáticamente.)

    GET /reporteVentas?administrador=1&desde=2026-11-01&hasta=2026-11-30
    GET /reporteTiempos?administrador=1&desde=2026-11-01&hasta=2026-11-30

Las fechas son opcionales y se escriben AAAA-MM-DD (ambas inclusive).
"""
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from rest import db
from rest.modelos.AdministradorModel import Administrador
from rest.modelos.PagoModel import Pago
from rest.modelos.PedidoModel import Pedido

bp = Blueprint('reporte', __name__)


def _error(mensaje, codigo):
    return jsonify({'error': mensaje}), codigo


def _validar_administrador():
    """None si quien consulta es un administrador existente; si no, la respuesta de error."""
    id_admin = request.args.get('administrador', type=int)
    if id_admin is None:
        return _error('Indique el administrador que consulta el reporte (parámetro administrador).', 400)
    if db.session.get(Administrador, id_admin) is None:
        return _error('Solo un administrador puede consultar los reportes.', 403)
    return None


def _leer_rango():
    """Devuelve (desde, hasta_exclusivo, error). Las fechas son opcionales."""
    def leer(nombre):
        texto = request.args.get(nombre)
        if not texto:
            return None, None
        try:
            return datetime.strptime(texto, '%Y-%m-%d'), None
        except ValueError:
            return None, _error(f'La fecha "{nombre}" debe tener el formato AAAA-MM-DD.', 400)

    desde, err = leer('desde')
    if err:
        return None, None, err
    hasta, err = leer('hasta')
    if err:
        return None, None, err
    if desde and hasta and desde > hasta:
        return None, None, _error('La fecha inicial no puede ser mayor que la final.', 400)
    # "hasta" es inclusivo: se compara contra el inicio del día siguiente
    return desde, (hasta + timedelta(days=1)) if hasta else None, None


# ---------- REPORTE DE VENTAS ----------
# Suma los pagos de pedidos ENTREGADOS cuya fecha de pago cae en el rango.
@bp.route('/reporteVentas', methods=['GET'])
def reporte_ventas():
    error = _validar_administrador()
    if error:
        return error
    desde, hasta_excl, error = _leer_rango()
    if error:
        return error

    consulta = (db.session.query(Pago, Pedido)
                .select_from(Pago)
                .join(Pedido, Pedido.id_pedido == Pago.Pedido_id_pedido)
                .filter(Pedido.estado == 'ENTREGADO'))
    if desde:
        consulta = consulta.filter(Pago.fecha_pago >= desde)
    if hasta_excl:
        consulta = consulta.filter(Pago.fecha_pago < hasta_excl)

    pagos, total, por_metodo = [], 0.0, {}
    for pago, pedido in consulta.order_by(Pago.fecha_pago, Pago.id_pago).all():
        monto = pago.monto or 0
        total += monto
        metodo = pago.metodo_pago or 'Sin método'
        por_metodo[metodo] = por_metodo.get(metodo, 0) + monto
        pagos.append({**pago.toDict(), 'estado_pedido': pedido.estado})

    return jsonify({'total': total,
                    'cantidad_pagos': len(pagos),
                    'por_metodo': [{'metodo': m, 'total': t} for m, t in sorted(por_metodo.items())],
                    'pagos': pagos})


# ---------- REPORTE DE TIEMPOS DE PREPARACIÓN ----------
# Tiempo = fecha_ultima_actualizacion - fecha_creacion de los pedidos LISTO o ENTREGADO.
# Aviso: la base solo guarda la última actualización. Para un pedido LISTO eso es el
# momento exacto en que cocina lo terminó; para uno ENTREGADO es el de la entrega, así
# que incluye el tiempo de servicio. Con un historial de estados (HU-15) se podría
# medir cada tramo por separado.
@bp.route('/reporteTiempos', methods=['GET'])
def reporte_tiempos():
    error = _validar_administrador()
    if error:
        return error
    desde, hasta_excl, error = _leer_rango()
    if error:
        return error

    consulta = db.session.query(Pedido).filter(Pedido.estado.in_(['LISTO', 'ENTREGADO']),
                                               Pedido.fecha_creacion.is_not(None),
                                               Pedido.fecha_ultima_actualizacion.is_not(None))
    if desde:
        consulta = consulta.filter(Pedido.fecha_creacion >= desde)
    if hasta_excl:
        consulta = consulta.filter(Pedido.fecha_creacion < hasta_excl)

    pedidos = []
    for p in consulta.order_by(Pedido.fecha_creacion, Pedido.id_pedido).all():
        minutos = round((p.fecha_ultima_actualizacion - p.fecha_creacion).total_seconds() / 60, 1)
        pedidos.append({'id_pedido': p.id_pedido,
                        'estado': p.estado,
                        'fecha_creacion': p.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                        'fecha_ultima_actualizacion': p.fecha_ultima_actualizacion.strftime('%Y-%m-%d %H:%M:%S'),
                        'minutos': max(minutos, 0)})

    promedio = round(sum(x['minutos'] for x in pedidos) / len(pedidos), 1) if pedidos else None
    return jsonify({'promedio_minutos': promedio,
                    'cantidad_pedidos': len(pedidos),
                    'pedidos': pedidos})
