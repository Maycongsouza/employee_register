try:
    from app.database.base import Base
    from sqlalchemy.event import listens_for
    from app.models.employee import Employee
    from app.models.job import Job
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

@listens_for(Employee, "before_insert")
def validate_job_before_insert(mapper, connection, target: Employee):
    """
        Verifica se o cargo de um colaborador é válido antes de inserir o registro no banco de dados.

        O evento é acionado automaticamente antes de um novo colaborador ser inserido.
        Ele verifica se o job_id associado ao colaborador é válido e atribui automaticamente
        o department_id com base no cargo que está sendo atribuido.

        Args:
            mapper: Mapeamento associado ao modelo.
            connection: Conexão ativa com o banco.
            target: Instância de modelo que será inserida.

        Raises:
            ValueError: Se o cargo associado (job_id) não existir.
    """
    job = connection.execute(
        Job.__table__.select().where(Job.id == target.job_id)
    ).fetchone()
    if not job:
        raise ValueError("Cargo inválido.")
    target.department_id = job.department_id

@listens_for(Employee, "before_update")
def validate_job_before_insert(mapper, connection, target: Employee):
    """
        Verifica se o cargo de um colaborador é válido antes de inserir o registro no banco de dados.

        O evento é acionado automaticamente antes de atualizar os dados de um colaborador que já existe no banco.
        Ele verifica se o job_id associado e atribui automaticamente  o department_id com base no cargo que está
        sendo atribuido.

        Args:
            mapper: Mapeamento associado ao modelo.
            connection: Conexão ativa com o banco.
            target: Instância de modelo que será inserida.

        Raises:
            ValueError: Se o cargo associado (job_id) não existir.
    """
    job = connection.execute(
        Job.__table__.select().where(Job.id == target.job_id)
    ).fetchone()
    if not job:
        raise ValueError("Cargo inválido.")
    target.department_id = job.department_id