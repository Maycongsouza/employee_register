try:
    import unittest
    import requests
    from faker import Faker
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

BASE_URL = "http://localhost:5555"
fake = Faker()


class TestDepartmentAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Criar um departamento apenas uma vez antes de todos os testes.
        cls.new_department_data = {
            "name": "Administrativo",
        }
        response = requests.post("%s/departments" % BASE_URL, json=cls.new_department_data)
        if response.status_code == 200:
            cls.department = response.json()
        else:
            raise RuntimeError("Falha ao criar o departamento inicial: %s, %s" % (response.status_code, response.text))

    @classmethod
    def tearDownClass(cls):
        # Deletar o departamento criado ao final dos testes.
        if hasattr(cls, "department") and cls.department.get("id"):
            requests.delete("%s/departments/%s" % (BASE_URL, cls.department["id"]))

    def test_get_all_departments(self):
        """
            Função para testar a API que busca todos os registros
            dos departamentos inseridos no banco de dados.
        """

        response = requests.get("%s/departments" % BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_department_by_id(self):
        """
            Função para testar a API que busca um registro específico
            de um dos departamentos inseridos no banco de dados.
        """

        response = requests.get("%s/departments/%s" % (BASE_URL, self.department["id"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.department["id"])

    def test_update_department(self):
        """
            Função para testar a API de atualização de um departamento.
        """

        update_data = {"name": "Vendas"}
        response = requests.put("%s/departments/%s" % (BASE_URL, self.department["id"]), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), update_data["name"])
        # Restaurar o nome original para os testes seguintes.
        requests.put("%s/departments/%s" % (BASE_URL, self.department["id"]), json=self.new_department_data)

    def test_delete_department(self):
        """
            Função para testar a exclusão de um departamento.
        """

        # Criar um novo departamento para testar a exclusão sem interferir no registro principal.
        temp_department_data = {"name": "Temporary Department"}
        response = requests.post("%s/departments" % BASE_URL, json=temp_department_data)
        temp_department = response.json()

        # Excluir o departamento temporário.
        response = requests.delete("%s/departments/%s" % (BASE_URL, temp_department["id"]))
        self.assertEqual(response.status_code, 200)

        # Verificar que o departamento foi excluído.
        response = requests.get("%s/departments/%s" % (BASE_URL, temp_department["id"]))
        self.assertEqual(response.status_code, 500)

if __name__ == "__main__":
    unittest.main()
