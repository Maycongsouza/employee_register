try:
    import unittest
    import requests
    from faker import Faker
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

BASE_URL = "http://localhost:5555"
fake = Faker()


class TestEmployeeAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
            Configuração inicial da classe para criar um colaborador apenas uma vez.
        """

        cls.new_employee_data = {
            "name": fake.name(),
            "last_name": fake.last_name(),
            "register_number": str(fake.random_int(min=10000, max=99999)),
            "job_id": 1,
            "salary": fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=10000),
        }
        response = requests.post("%s/employees" % BASE_URL, json=cls.new_employee_data)
        if response.status_code == 200:
            cls.employee = response.json()
        else:
            raise RuntimeError("Falha ao criar o colaborador inicial: %s, %s" % (response.status_code, response.text))

    @classmethod
    def tearDownClass(cls):
        """
            Deletar o colaborador criado ao final de todos os testes.
        """
        if hasattr(cls, "employee") and cls.employee.get("id"):
            requests.delete("%s/employees/%s" % (BASE_URL, cls.employee["id"]))

    def test_get_all_employees(self):
        """
            Função para testar a API que busca todos os registros
            dos colaboradores inseridos no banco de dados.
        """

        response = requests.get("%s/employees" % BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_employee_by_id(self):
        """
            Função para testar a API que busca um registro específico
            de um dos colaboradores inseridos no banco de dados.
        """

        response = requests.get("%s/employees/%s" % (BASE_URL, self.employee["id"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.employee["id"])

    def test_promote_error_employee(self):
        """
            Função para testar a API de promoção para colaborador.
            Esse teste tem como objetivo verificar se a trigger está funcionando
            e não permitindo que um funcionário seja promovido para um cargo de liderança
            que já esteja ocupado.
        """

        temp_employee = self.create_temp_employee()
        update_data = {"job_id": 3, "salary": 8000.0}
        response = requests.put("%s/employees/%s/promote" % (BASE_URL, temp_employee["id"]), json=update_data)
        self.assertEqual(response.status_code, 500)

    def test_promote_success_employee(self):
        """
            Função para testar a API de promoção/atualização para colaborador.
        """

        update_data = {"job_id": 2, "salary": 8000.0}
        response = requests.put("%s/employees/%s/promote" % (BASE_URL, self.employee["id"]), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("job_id"), 2)
        self.assertEqual(response.json().get("salary"), 8000.0)
        # Restaurar o cargo e salário original.
        requests.put("%s/employees/%s/promote" % (BASE_URL, self.employee["id"]), json=self.new_employee_data)

    def test_archive_employee(self):
        """
            Função para testar a API de demissão/arquivamento de colaboradores.
        """
        temp_employee = self.create_temp_employee()
        response = requests.put("%s/employees/%s/archive" % (BASE_URL, temp_employee["id"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "Archived")

    def test_delete_employee(self):
        """
            Função para testar a API que deleta os registros do colaborador.
        """

        temp_employee = self.create_temp_employee()
        response = requests.delete("%s/employees/%s" % (BASE_URL, temp_employee["id"]))
        self.assertEqual(response.status_code, 200)
        response = requests.get("%s/employees/%s" % (BASE_URL, temp_employee["id"]))
        self.assertEqual(response.status_code, 404)

    def create_temp_employee(self):
        """
            Função auxiliar para criar um colaborador temporário para testes específicos.
        """

        temp_data = {
            "name": fake.name(),
            "last_name": fake.last_name(),
            "register_number": str(fake.random_int(min=10000, max=99999)),
            "job_id": 1,
            "salary": fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=10000),
        }
        response = requests.post("%s/employees" % BASE_URL, json=temp_data)
        return response.json()

if __name__ == "__main__":
    unittest.main()
