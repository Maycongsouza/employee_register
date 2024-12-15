try:
    import unittest
    import requests
    from faker import Faker
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

BASE_URL = "http://localhost:5555"
fake = Faker()


class TestEmployeeAPI(unittest.TestCase):
    def setUp(self):

        # Dados de amostra para criar um colaborador
        self.new_employee_data = {
            "name": fake.name(),
            "last_name": fake.last_name(),
            "register_number": str(fake.random_int(min=10000, max=99999)),
            "job_id": 1,
            "salary": fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=10000),
        }

    def test_create_employee(self):
        """
            Função para testar API de criar um novo colaborador.
        """

        response = requests.post("%s/employees" % BASE_URL, json=self.new_employee_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.employee_id = response.json().get("id")

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

        employee = self.create_test_employee()
        response = requests.get("%s/employees/%s" % (BASE_URL, employee['id']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), employee["id"])

    def test_promote_error_employee(self):
        """
            Função para testar a API de promoção para colaborador.
            Esse teste tem como objetivo verificar se a trigger está funcionando
            e não permitindo que um funcionário seja promovido para um cargo de liderança
            que já esteja ocupado.
        """

        employee = self.create_test_employee()
        update_data = {"job_id": 3, "salary": 8000.0}
        response = requests.put("%s/employees/%s/promote" % (BASE_URL, employee['id']), json=update_data)
        self.assertEqual(response.status_code, 500)

    def test_promote_success_employee(self):
        """
            Função para testar a API de promoção para colaborador.
        """

        employee = self.create_test_employee()
        update_data = {"job_id": 2, "salary": 8000.0}
        response = requests.put("%s/employees/%s/promote" % (BASE_URL, employee['id']), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("job_id"), 2)
        self.assertEqual(response.json().get("salary"), 8000.0)

    def test_archive_employee(self):
        """
            Função para testar a API de demissão/arquivamento de colaboradores.
        """

        employee = self.create_test_employee()
        response = requests.put("%s/employees/%s/archive" % (BASE_URL, employee['id']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "Archived")

    def test_delete_employee(self):
        """
            Função para testar a API que deleta os registeros
            do colaborador.
        """

        employee = self.create_test_employee()
        response = requests.delete("%s/employees/%s" % (BASE_URL, employee['id']))
        self.assertEqual(response.status_code, 200)
        response = requests.get("%s/employees/%s" % (BASE_URL, employee['id']))
        self.assertEqual(response.status_code, 404)

    def create_test_employee(self):
        response = requests.post(f"%s/employees" % BASE_URL, json=self.new_employee_data)
        return response.json()


if __name__ == "__main__":
    unittest.main()
