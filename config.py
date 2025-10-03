import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de la base de datos
DATABASE_URL = "sqlite:///reychdb"  # Cambia según tu BD

# Crear engine y sessionmaker
engine = sa.create_engine(DATABASE_URL, echo=True)  # echo=True para ver queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()