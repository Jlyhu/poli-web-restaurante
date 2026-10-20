# ============================================================
# models.py
# Modelo Usuario, mapeado a la tabla 'Usuario' que YA existe
# en la base de datos (no se crea ni se modifica ninguna tabla)
# ============================================================

from rest import db
from sqlalchemy import Column, Integer, String


# ------------------------------------------------------------
# Clase: Usuario
# Atributos:
#   idUsuario    (int)  -- Clave primaria
#   nombre       (str)  -- Nombre de usuario
#   credenciales (str)  -- Credenciales de acceso (NUNCA se devuelven en las respuestas)
#   estado       (str)  -- 'activo' o 'inactivo'
# ------------------------------------------------------------
class Usuario(db.Base):
    __tablename__ = 'Usuario'  
    idUsuario    = Column(Integer, primary_key=True, autoincrement=False)
    nombre       = Column(String(100), nullable=True)
    credenciales = Column(String(255), nullable=True)
    estado       = Column(String(20), nullable=False, default='activo')

# Valores por defecto para los atributos, para poder crear instancias sin pasar todos los parámetros.
    def __init__(self, idUsuario=None, nombre=None, credenciales=None, estado='activo'):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.credenciales = credenciales
        self.estado = estado

    def __repr__(self):
        return f'Usuario({self.idUsuario}, {self.nombre}, {self.estado})'

    # Convierte el objeto en un diccionario para devolverlo como JSON.
    # Se omiten las credenciales para no exponer la clave por la API.
    def toDict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns if c.name != 'credenciales'}
