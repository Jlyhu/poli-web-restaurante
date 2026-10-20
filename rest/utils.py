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
