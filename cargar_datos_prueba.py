"""Carga los datos de prueba (rest/datos_prueba.sql) en la base SIN usar Workbench.

Usa la misma conexión del proyecto (el archivo .env).
Ejecutar desde la raíz del repo (la carpeta que tiene rest, orm y DataAccess):

    python cargar_datos_prueba.py

Se puede correr varias veces: el SQL usa INSERT IGNORE, así que no duplica nada.
"""
from pathlib import Path

from sqlalchemy import text

from rest import engine

RUTA_SQL = Path(__file__).parent / "rest" / "datos_prueba.sql"


def leer_sentencias(ruta):
    """Devuelve las sentencias del .sql sin los comentarios (líneas que empiezan con --)."""
    lineas = [l for l in ruta.read_text(encoding="utf-8").splitlines()
              if not l.strip().startswith("--")]
    return [s.strip() for s in "\n".join(lineas).split(";") if s.strip()]


def main():
    if not RUTA_SQL.exists():
        print(f"No encuentro {RUTA_SQL}. Pon datos_prueba.sql dentro de la carpeta rest.")
        return

    sentencias = leer_sentencias(RUTA_SQL)
    print(f"Voy a ejecutar {len(sentencias)} sentencias...")

    with engine.begin() as conn:  # si alguna falla, no se guarda nada (todo o nada)
        for i, sql in enumerate(sentencias, start=1):
            tabla = sql.split("INTO")[1].split("(")[0].strip() if "INTO" in sql else "?"
            conn.execute(text(sql))
            print(f"  {i}. OK -> {tabla}")

    with engine.connect() as conn:
        usuarios = conn.execute(text("SELECT idUsuario FROM Usuario WHERE idUsuario >= 9001")).fetchall()
        print("Usuarios de prueba en la base:", [u[0] for u in usuarios])
    print("Listo. Ya puedes correr la colección en Postman.")


if __name__ == "__main__":
    main()