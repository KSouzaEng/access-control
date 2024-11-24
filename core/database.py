import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# URL do banco de dados
# if os.getenv("DEPLOYMENT_ENVIRONMENT") == 'DEV':
engine = create_engine(os.getenv("DB_URL"), connect_args={'check_same_thread': False})
# else:
#     engine = create_engine(os.getenv("DB_URL"))

# # Criar o engine SQLAlchemy
# engine = create_engine(DATABASE_URL)

# Criar uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
