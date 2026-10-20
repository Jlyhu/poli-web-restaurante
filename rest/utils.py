# ============================================================
# utils.py
# Funciones compartidas por todas las rutas del servicio REST
# ============================================================

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from rest import db


def guardar_cambios():
    """Hace commit; si falla, deshace la transacción y devuelve una respuesta de error."""
    try:
        db.session.commit()
        return None
    except IntegrityError as e:
        db.session.rollback()   # sin esto, la sesión queda inservible para las siguientes peticiones
        # La base de datos rechazó la operación por una regla de integridad
        mensajes = {1062: 'Ya existe un registro con ese id',
                    1452: 'Alguna referencia no existe (violación de clave foránea)',
                    1451: 'No se puede eliminar: otros registros dependen de este'}
        return jsonify({'error': mensajes.get(e.orig.errno, 'Violación de integridad de datos'),
                        'detalle': str(e.orig)}), 409
    except Exception as e:
        db.session.rollback()   # sin esto, la sesión queda inservible para las siguientes peticiones
        return jsonify({'error': str(e.__cause__ or e)}), 400


def no_encontrada(recurso, identificador):
    return jsonify({'error': f'No existe {recurso} con id {identificador}'}), 404


def siguiente_id(columna):
    """Las tablas no generan el id solas: si no lo envían, se usa el siguiente disponible."""
    return (db.session.query(func.max(columna)).scalar() or 0) + 1
"""Utilidades compartidas por los endpoints REST."""
from flask import jsonify
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from rest import db


def siguiente_id(columna):
    """Calcula el siguiente ID para tablas que no tienen AUTO_INCREMENT.

    Nota: MAX(id)+1 no es seguro ante inserciones concurrentes. Para un sistema
    con múltiples usuarios se recomienda migrar las claves a AUTO_INCREMENT.
    """
    maximo = db.session.query(func.max(columna)).scalar()
    return 1 if maximo is None else int(maximo) + 1


def no_encontrada(entidad, identificador):
    return jsonify({"error": f"No se encontró {entidad} con identificador {identificador}."}), 404


def guardar_cambios():
    """Confirma la transacción y revierte la sesión si la BD rechaza el cambio."""
    try:
        db.session.commit()
        return None
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error": "No se pudo guardar el cambio. Verifique las claves foráneas, "
                     "los identificadores duplicados y las restricciones de la base de datos."
        }), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Error de base de datos al guardar el cambio."}), 500
