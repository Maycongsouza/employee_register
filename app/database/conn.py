try:
    import os
    import logging
    from app.database.base import Base
    from app.database.demo_data import seed_data
    from app.database.db_roles import execute_sql_file
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_utils import database_exists, create_database
    from sqlalchemy.orm import configure_mappers
    from sqlalchemy.sql import text
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

_logger = logging.getLogger(__name__)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    raise ValueError("As variáveis de ambiente POSTGRES_USER, POSTGRES_PASSWORD ou POSTGRES_DB não estão definidas.")

DB_URL = "postgresql://%s:%s@%s:%s/%s" % (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
configure_mappers() # Configura os listens no banco de dados

if not database_exists(engine.url): # Faz a verificação se a DB já existe no banco.
    create_database(engine.url) # Se não existe, a DB é criada.
    _logger.info("Banco de dados criado com sucesso!")

    Base.metadata.create_all(bind=engine)
    _logger.info("Tabelas criadas com sucesso!")

    # Adiciona regras ao banco à partir do arquivo init.sql
    sql_file_path = os.path.join(os.path.dirname(__file__), "init.sql")
    try:
        execute_sql_file(engine, sql_file_path)
    except Exception as e:
        _logger.error(f"Erro ao executar o arquivo SQL: %s" % e)
        raise

    # Inserir dados de demonstração
    with SessionLocal() as db:
        seed_data(db)
        _logger.info("Dados de demonstração inseridos com sucesso!")
else:
    _logger.info("Banco de dados já existe!")

def get_db():
    """
    Cria uma sessão do banco de dados.

    Yields:
        db: Sessão que foi criada do banco de dados.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()