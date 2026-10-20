# ============================================================
# models.py
# Define la conexión a la base de datos (MySQL en Clever Cloud)
# ============================================================

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

# Lee los datos de conexión del archivo .env
load_dotenv()

# Base declarativa de SQLAlchemy — todas las clases modelo heredan de aquí
Base = declarative_base()

# Dirección de conexión a la base de datos MySQL
connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    database=os.getenv("DB_NAME"),
)

# Motor de conexión
#   echo=True -> imprime en consola las sentencias SQL generadas
#   pool_size=1 y max_overflow=1 -> máximo 2 conexiones abiertas (Clever Cloud limita las conexiones)
#   pool_pre_ping=True -> prueba la conexión antes de usarla, por si la nube la cerró
engine = create_engine(
    connection_url,
    echo=True,
    pool_size=1,
    max_overflow=1,
    pool_pre_ping=True,
)

# Cada llamada a SessionLocal() crea una nueva sesión
SessionLocal = sessionmaker(bind=engine)
"""Configuración común de SQLAlchemy para la capa ORM/DAO.

Usa las tablas existentes de MySQL; no ejecuta create_all automáticamente.
Configura la conexión mediante las variables DB_HOST, DB_USER, DB_PASS,
DB_NAME y DB_PORT (o DATABASE_URL).
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()


def _crear_url():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    required = ("DB_HOST", "DB_USER", "DB_NAME")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Faltan variables de conexión en .env: " + ", ".join(missing)
            + ". Copia .env.example a .env y completa los datos."
        )
    return URL.create(
        "mysql+mysqlconnector",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS", ""),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        query={"charset": "utf8mb4"},
    )


engine = create_engine(_crear_url(), pool_pre_ping=True, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
