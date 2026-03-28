#Archivo de conexión a base de datos

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#Engine principal de SQLAlchemy conectado a PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Sesión de base de datos reutilizable en la app
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency para FastAPI: abre sesión y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()