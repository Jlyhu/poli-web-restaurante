# ============================================================
# db.py
# Conexión a la base de datos (MySQL en Clever Cloud) para el servicio REST
# Los datos de conexión salen del archivo .env
# ============================================================

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# Lee los datos de conexión del archivo .env (así la clave no queda escrita en el código)
load_dotenv()

# Dirección de conexión (equivale a: mysql+mysqlconnector://usuario:clave@host:puerto/nombre_bd)
connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    database=os.getenv("DB_NAME"),
)

# Motor de conexión
#   echo=True          -> imprime en consola el SQL generado
#   pool_size=1 y max_overflow=1 -> máximo 2 conexiones abiertas (Clever Cloud limita las conexiones)
#   pool_pre_ping=True -> prueba la conexión antes de usarla, por si la nube la cerró
engine = create_engine(connection_url, echo=True, pool_size=1, max_overflow=1, pool_pre_ping=True)

Session = sessionmaker(bind=engine)

# scoped_session: se usa igual que una sesión normal (session.add, session.commit...),
# pero cada petición HTTP trabaja con la suya y al terminar se cierra (ver mainService.py).
session = scoped_session(Session)

# Base declarativa de SQLAlchemy — las clases modelo heredan de aquí
Base = declarative_base()
