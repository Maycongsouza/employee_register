from sqlalchemy.orm import Session
from app.models.department import Department
from app.models.job import Job
from app.models.user import User
from app.models.employee import Employee
from faker import Faker

# Usando a lib faker para gerar dados dos funcionários aleatóriamente.
fake = Faker()

# Inserindo dados de demonstração
def seed_data(db: Session):

    # Criando departamentos
    department_tech = Department(name="Tecnologia da Informação")
    department_hr = Department(name="Recursos Humanos")

    # Commitando para o banco apenas os departamentos
    db.add_all([department_tech, department_hr])
    db.commit()

    # Criando cargos
    job_dev = Job(name="Desenvolvedor Python", department_id=department_tech.id, code="DEVP")
    job_tech_leader = Job(name="Líder Técnico", department_id=department_tech.id, code="LEAD")
    job_hr_manager = Job(name="Coordenador de RH", department_id=department_hr.id, code="CDRH")

    # Commitando para o banco apenas os cargos
    db.add_all([job_dev, job_tech_leader, job_hr_manager])
    db.commit()

    # Criando funcionários
    employee_1 = Employee(
        name=fake.name(),
        last_name=fake.last_name(),
        register_number=str(fake.random_int(min=10000, max=99999)),
        job_id=job_dev.id,
        department_id=department_tech.id,
        salary=fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=8000),
        status="active",
    )
    employee_2 = Employee(
        name=fake.name(),
        last_name=fake.last_name(),
        register_number=str(fake.random_int(min=10000, max=99999)),
        job_id=job_tech_leader.id,
        department_id=department_tech.id,
        salary=fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=10000),
        status="active",
    )
    employee_3 = Employee(
        name=fake.name(),
        last_name=fake.last_name(),
        register_number=str(fake.random_int(min=10000, max=99999)),
        job_id=job_hr_manager.id,
        department_id=department_hr.id,
        salary=fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=3000, max_value=12000),
        status="active",
    )

    # Commitando para o banco apenas os funcionários
    db.add_all([employee_1, employee_2, employee_3])
    db.commit()


    # Criando usuários
    user_1 = User(
        login="dev@company.com.br",
        passw=fake.password(),
        employee_id=employee_1.id
    )
    user_2 = User(
        login="tech@company.com.br",
        passw=fake.password(),
        employee_id=employee_2.id
    )
    user_3 = User(
        login="hr@company.com.br",
        passw=fake.password(),
        employee_id=employee_3.id
    )
    user_admin = User(login="admin", passw="admin")

    # Commitando para o banco os usuários
    db.add_all([user_1, user_2, user_3])
    db.commit()
    db.add_all([user_admin])
    db.commit()
