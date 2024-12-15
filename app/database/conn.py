try:
    from app.database.base import Base
    from app.database.demo_data import seed_data
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_utils import database_exists, create_database
    import os
    from dotenv import load_dotenv
    from sqlalchemy.orm import configure_mappers
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)

load_dotenv("/home/mindcode/Aquarela/aquarela_employee_register/example.env")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DB_URL = "postgresql://%s:%s@%s:%s/%s" % (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
configure_mappers()

if not database_exists(engine.url):
    create_database(engine.url)
    print("Banco de dados criado com sucesso!")

    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

    # Inserir dados de demonstração
    with SessionLocal() as db:
        seed_data(db)
        print("Dados de demonstração inseridos com sucesso!")
else:
    print("Banco de dados já existe!")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()