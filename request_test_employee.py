import requests
from faker import Faker

fake = Faker()
BASE_URL = "http://127.0.0.1:5555"  # Atualize com o URL do seu servidor, se necessário


# Criar um colaborador
def create_employee():
    data = {
        "name": fake.name(),
        "last_name": fake.last_name(),
        "register_number": str(fake.random_int(min=10000, max=99999)),
        "job_id": 1,
        "department_id": None,
        "salary": fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=10000),
    }
    response = requests.post(f"{BASE_URL}/employees", json=data)
    print("Create Employee Response:", response.status_code, response.json())
    return response.json().get("id")


# Obter todos os colaboradores
def get_all_employees():
    response = requests.get(f"{BASE_URL}/employees")
    print("All Employees:", response.status_code, response.json())


# Obter um colaborador por ID
def get_employee_by_id(employee_id):
    response = requests.get(f"{BASE_URL}/employees/{employee_id}")
    print(f"Employee {employee_id}:", response.status_code, response.json())


# Atualizar dados do colaborador (promoção)
def promote_employee(employee_id):
    data = {
        "job_id": 3,  # Atualize para o ID do novo cargo
        "salary": 7000.0,
    }
    response = requests.put(f"{BASE_URL}/employees/{employee_id}/promote", json=data)
    print("Promote Employee Response:", response.status_code, response.json())


# Arquivar (demitir) um colaborador
def archive_employee(employee_id):
    response = requests.put(f"{BASE_URL}/employees/{employee_id}/archive")
    print("Archive Employee Response:", response.status_code, response.json())


# Deletar um colaborador
def delete_employee(employee_id):
    response = requests.delete(f"{BASE_URL}/employees/{employee_id}")
    print("Delete Employee Response:", response.status_code, response.json())


# Teste os endpoints
if __name__ == "__main__":
    print("=== Testing Employee API ===")

    # Criar um novo colaborador
    employee_id = create_employee()

    if employee_id:
        # Consultar todos os colaboradores
        get_all_employees()

        # Consultar um colaborador por ID
        get_employee_by_id(employee_id)

        # Promover o colaborador
        promote_employee(employee_id)

        # Arquivar o colaborador
        archive_employee(employee_id)
        #
        # # Excluir o colaborador
        # delete_employee(employee_id)
        #
        # Consultar novamente todos os colaboradores para verificar exclusão
        get_all_employees()
