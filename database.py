from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Pegando a URL do banco de dados do Railway (substitua se necessário)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/seu_banco")

# Criando a conexão com o banco
engine = create_engine(DATABASE_URL, connect_args={})

# Criando a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando a base para os modelos do SQLAlchemy	
Base = declarative_base()
