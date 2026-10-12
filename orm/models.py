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
