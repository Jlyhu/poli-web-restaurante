"""Inicialización de la capa REST de PoliRestaurante."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

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
Session = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True))


class _DatabaseFacade:
    """Facade pequeña compatible con db.session y db.Base usados por los módulos."""
    Base = Base
    session = Session


db = _DatabaseFacade()
