try:
    from sqlalchemy.orm import Session
    from app.models.department import Department as DepartmentModel
    from app.models.job import Job as JobModel
    from app.models.user import User as UserModel
    from app.models.employee import Employee as EmployeeModel, StateEnum
    from app.schemas.department import DepartmentCreate, DepartmentUpdate
    from app.schemas.job import JobCreate, JobUpdate
    from app.schemas.user import UserCreate, UserUpdate
    from app.schemas.employee import EmployeeCreate, EmployeeUpdate
    from typing import List
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)


# CRUD dos colaboradores
def create_employee(db: Session, employee: EmployeeCreate) -> EmployeeModel:
    """
        Cria um novo colaborador no banco de dados.

        Args:
            db: Sessão do banco de dados.
            employee: Dados do colaborador a serem inseridos.

        Returns:
            EmployeeModel: Retorna os dados do colaborador que foi criado.
    """

    db_employee = EmployeeModel(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_all_employees(db: Session) -> List[EmployeeModel]:
    """
        Faz uma busca de todos os colaboradores cadastrados no sistema.

        Args:
            db: Sessão do banco de dados.

        Returns:
            List[EmployeeModel]: Retorna a lista de todos os colaboradores.
    """

    return db.query(EmployeeModel).all()

def get_employee_by_id(db: Session, employee_id: int) -> EmployeeModel:
    """
        Faz uma busca de um colaborador pelo ID.

        Args:
            db: Sessão do banco de dados.
            employee_id: ID do colaborador.

        Returns:
            EmployeeModel: Retorna o colaborador correspondente ao ID.
    """

    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not employee:
        return None
    return employee

def promote_employee(db: Session, employee_id: int, update_data: EmployeeUpdate) -> EmployeeModel:
    """
        Promove e/ou atualiza as informações de um colaborador já cadastrado.

        Args:
            db: Sessão do banco de dados.
            employee_id: ID do colaborador.
            update_data: Dados de atualização do colaborador.

        Returns:
            EmployeeModel: Retorna o colaborador atualizado.
    """

    employee = get_employee_by_id(db, employee_id)

    if update_data.name:
        employee.name = update_data.name
    if update_data.last_name:
        employee.last_name = update_data.last_name
    if update_data.job_id:
        employee.job_id = update_data.job_id
    if update_data.salary:
        employee.salary = update_data.salary

    db.commit()
    db.refresh(employee)
    return employee

def terminate_employee(db: Session, employee_id: int) -> EmployeeModel:
    """
        Arquiva um colaborador, alterando seu status para 'arquivado'. Cadastros arquivados não são mais retornados na API
        que verifica todos os colaboradores cadastrados no sistema.

        Args:
            db: Sessão do banco de dados.
            employee_id: ID do colaborador.

        Returns:
            EmployeeModel: O colaborador com o status atualizado.
    """
    employee = get_employee_by_id(db, employee_id)

    employee.status = StateEnum.archived
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int) -> None:
    """
        Exclui um colaborador do banco de dados.

        Args:
            db: Sessão do banco de dados.
            employee_id: ID do colaborador a ser excluído.

        Returns:
            None: Sem retornos.
    """
    employee = get_employee_by_id(db, employee_id)

    db.delete(employee)
    db.commit()

# CRUD dos departamentos
def create_department(db: Session, department: DepartmentCreate) -> DepartmentModel:
    """
        Cria um novo departamento no banco de dados.

        Args:
            db: Sessão do banco de dados.
            department: Dados do departamento a serem criados.

        Returns:
            DepartmentModel: Retorna os dados do departamento recém criado
    """
    db_department = DepartmentModel(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_all_departments(db: Session) -> List[DepartmentModel]:
    """
        Faz uma busca de todos os departamentos cadastrados.

        Args:
            db: Sessão do banco de dados.

        Returns:
            List[DepartmentModel]: Lista de todos os departamentos cadastrados.
    """
    return db.query(DepartmentModel).all()

def get_department_by_id(db: Session, department_id: int) -> DepartmentModel:
    """
        Faz uma busca de departamentos pelo ID.

        Args:
            db: Sessão do banco de dados.

        Returns:
            DepartmentModel: Retorna o departamento cadastrado
    """
    department = db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
    if not department:
        return None
    return department

def update_department(db: Session, department_id: int, update_data: DepartmentUpdate) -> DepartmentModel:
    """
        Atualiza as informações de um departamento buscado pelo ID.

        Args:
            db: Sessão do banco de dados.
            department_id: ID do departamento.
            update_data: Dados a serem atualizados do departamento.

        Returns:
            DepartmentModel: Retorna o departamento com os dados atualizados.
    """
    department = get_department_by_id(db, department_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(department, field, value)
    db.commit()
    db.refresh(department)
    return department

def delete_department(db: Session, department_id: int) -> None:
    """
        Exclui o cadastro de um departamento do banco de dados.

        Args:
            db: Sessão do banco de dados.
            department_id: ID do departamento que deverá ser excluído.

        Returns:
            None: Sem retorno.
    """
    department = get_department_by_id(db, department_id)
    db.delete(department)
    db.commit()

# CRUD dos cargos
def create_job(db: Session, job: JobCreate) -> JobModel:
    """
        Cria um novo cadastro de cargo no banco de dados.

        Args:
            db: Sessão do banco de dados.
            job: Dados do cargo a serem inseridos.

        Returns:
            JobModel: Retorna o cargo cargo criado.
    """
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_all_jobs(db: Session) -> List[JobModel]:
    """
        Faz uma busca de todos os cargos cadastrados.

        Args:
            db: Sessão do banco de dados.

        Returns:
            List[JobModel]: Retorna a lista de todos os cargos.
    """
    return db.query(JobModel).all()

def get_job_by_id(db: Session, job_id: int) -> JobModel:
    """
        Busca um cargo na tabela pelo ID.

        Args:
            db: Sessão do banco de dados.
            job_id: ID do cargo.

        Returns:
            JobModel: Retorna o cargo que responde ao ID.
    """
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        return None
    return job

def update_job(db: Session, job_id: int, update_data: JobUpdate) -> JobModel:
    """
        Faz uma busca de um cargo na tabela pelo ID para ser atualizado.

        Args:
            db: Sessão do banco de dados.
            job_id: ID do cargo.
            update_data: Dados de atualização do cargo.

        Returns:
            JobModel: Retorna o cargo com dados atualizados que respondem ao ID.
    """
    job = get_job_by_id(db, job_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job

def delete_job(db: Session, job_id: int) -> None:
    """
        Busca um cargo na tabela pelo ID para ser deletado.

        Args:
            db: Sessão do banco de dados.
            job_id: ID do cargo.

        Returns:
            None: Sem retorno.
    """
    job = get_job_by_id(db, job_id)
    db.delete(job)
    db.commit()

# CRUD dos usuários
def create_user(db: Session, user: UserCreate) -> UserModel:
    """
        Cria um novo cadastro de usuário no banco de dados.

        Args:
            db: Sessão do banco de dados.
            user: Dados do usuário a serem criados.

        Returns:
            UserModel: Retorna os dados do usuário recém-criado.
    """
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> List[UserModel]:
    """
        Busca todos os usuários cadastrados na tabela.

        Args:
            db: Sessão do banco de dados.

        Returns:
            List[UserModel]: Retorna a lista de todos os usuários.
    """
    return db.query(UserModel).all()

def get_user_by_id(db: Session, user_id: int) -> UserModel:
    """
        Consulta um usuário pelo ID.

        Args:
            db: Sessão do banco de dados.
            user_id: ID do usuário.

        Returns:
            UserModel: Retorna o usuário correspondente ao ID.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return None
    return user

def update_user(db: Session, user_id: int, update_data: UserUpdate) -> UserModel:
    """
        Atualiza todas as informações de um usuário buscando o cadastro pelo ID.

        Args:
            db: Sessão do banco de dados.
            user_id: ID do usuário.
            update_data: Dados com a atualização do usuário.

        Returns:
            UserModel: Retorna os dados do usuário atualizado.
    """

    user = get_user_by_id(db, user_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user_id: int, update_data: UserUpdate) -> UserModel:
    """
        Atualiza somente a senha de um usuário com as novas informações vindas da API.

        Args:
            db: Sessão do banco de dados.
            user_id: ID do usuário.
            update_data: Dados com a senha.

        Returns:
            UserModel: Retorna os dados do usuário atualizado.
    """

    user = get_user_by_id(db, user_id)
    user.passw = update_data.passw
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> None:
    """
        Exclui um usuário do banco de dados.

        Args:
            db: Sessão do banco de dados.
            user_id: ID do usuário que deve ser excluído.

        Returns:
            None: Sem retornos.
    """
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
