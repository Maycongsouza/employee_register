try:
    import unittest
    import requests
    from faker import Faker
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

BASE_URL = "http://localhost:5555"  # Atualize conforme necessário
fake = Faker()


class TestEmployeeAPI(unittest.TestCase):
    def setUp(self):

        # Dados iniciais
        self.new_employee_data = {
            "name": fake.name(),
            "last_name": fake.last_name(),
            "register_number": str(fake.random_int(min=10000, max=99999)),
            "job_id": 1,
            "department_id": None,
            "salary": fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=1500, max_value=10000),
        }
        response = requests.post("%s/employees" % BASE_URL, json=self.new_employee_data)
        self.employee_id = response.json().get("id")

        # Criação de um usuário associado ao colaborador
        self.user_data = {
            "login": fake.user_name(),
            "passw": "defaultPassword", # Defino um password fácil de identificar
            "employee_id": self.employee_id,
        }
        response = requests.post("%s/users" % BASE_URL, json=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.user_id = response.json().get("id")

    def tearDown(self):
        # Exclusão do usuário e do colaborador após a realização dos testes
        requests.delete("%s/users/%s" % (BASE_URL, self.user_id))
        requests.delete("%s/employees/%s" % (BASE_URL, self.employee_id))

    def test_change_password(self):
        """
            Função para testar API de alteração de senha
        """

        new_password = fake.password()
        payload = {"passw": new_password}

        # Envio da requisição
        response = requests.put("%s/users/%s/password" % (BASE_URL, self.user_id), json=payload)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
