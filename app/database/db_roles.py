try:
    import os
    import logging
    from sqlalchemy.sql import text
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)
_logger = logging.getLogger(__name__)


def execute_sql_file(engine, file_path):
    """
        Lê o arquivo init.sql e executa as instruções contidas nele.

        Args:
            engine (sqlalchemy.Engine): Conexão com o banco de dados.
            file_path (str): Caminho para o arquivo SQL.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("O arquivo %s não foi encontrado." % file_path)

    with open(file_path, 'r') as file:
        sql_content = file.read()

    with engine.begin() as connection:  # Gerencia a transação
        try:
            connection.execute(text(sql_content))
            _logger.info(f"Arquivo SQL %s executado com sucesso!" % file_path)
        except Exception as e:
            _logger.error(f"Erro ao executar o arquivo %s: %s" % (file_path, e))
            raise