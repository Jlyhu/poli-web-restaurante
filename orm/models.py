"""Configuración común de SQLAlchemy para la capa ORM/DAO.

Define la conexión a la base de datos (MySQL en Clever Cloud).
Configura la conexión mediante las variables DB_HOST, DB_USER, DB_PASS,
DB_NAME y DB_PORT (o DATABASE_URL).
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

# Lee los datos de conexión del archivo .env
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

# Base declarativa de SQLAlchemy — todas las clases modelo heredan de aquí
Base = declarative_base()

# Motor de conexión con ajustes para Clever Cloud (limita conexiones)
engine = create_engine(
    _crear_url(),
    echo=True,
    pool_size=1,
    max_overflow=1,
    pool_pre_ping=True,
    future=True
)

# Cada llamada a SessionLocal() crea una nueva sesión
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)