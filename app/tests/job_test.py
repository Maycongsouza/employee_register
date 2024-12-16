import unittest
import requests
from faker import Faker

BASE_URL = "http://localhost:5555"
fake = Faker()


class TestJobAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
            Configuração inicial para criar dados necessários ao longo dos testes.
            Um departamento e um cargo são criados uma única vez para reutilização.
        """

        # Criar um departamento para associar ao cargo
        cls.department_data = {
            "name": "Financeiro",
        }
        department_response = requests.post("%s/departments" % BASE_URL, json=cls.department_data)
        if department_response.status_code == 200:
            cls.department = department_response.json()
        else:
            raise RuntimeError(
                "Falha ao criar departamento: %s, %s" % (department_response.status_code, department_response.text))

        # Criar um cargo para reaproveitar nos testes
        cls.job_data = {
            "name": fake.job(),
            "department_id": cls.department['id'],
            "code": "%s%s%s%s" % (
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter()
            )
        }
        job_response = requests.post("%s/jobs" % BASE_URL, json=cls.job_data)
        if job_response.status_code == 200:
            cls.job = job_response.json()
        else:
            raise RuntimeError("Falha ao criar cargo: %s, %s" % (job_response.status_code, job_response.text))

    @classmethod
    def tearDownClass(cls):
        """
            Remove os dados criados após a execução dos testes.
        """

        if hasattr(cls, "job") and cls.job.get("id"):
            requests.delete("%s/jobs/%s" % (BASE_URL, cls.job['id']))

        if hasattr(cls, "department") and cls.department.get("id"):
            requests.delete("%s/departments/%s" % (BASE_URL, cls.department['id']))

    def test_create_job(self):
        """
            Testa a criação de um novo cargo.
        """

        new_job_data = {
            "name": fake.job(),
            "department_id": self.department['id'],
            "code": "%s%s%s%s" % (
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter()
            )
        }
        response = requests.post("%s/jobs" % BASE_URL, json=new_job_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_get_all_jobs(self):
        """
            Faz uma busca de todos os cargos
        """

        response = requests.get("%s/jobs" % BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_job_by_id(self):
        """
            Função para testar a busca de um cargo por ID.
        """

        response = requests.get("%s/jobs/%s" % (BASE_URL, self.job['id']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.job["id"])

    def test_update_job(self):
        """
            Atualização de um cargo.
        """

        update_data = {
            "name": fake.job(),
            "code": "%s%s%s%s" % (
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter(),
            )
        }
        response = requests.put("%s/jobs/%s" % (BASE_URL, self.job['id']), json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("name"), update_data["name"])
        self.assertEqual(response.json().get("code"), update_data["code"])

    def test_delete_job(self):
        """
            Testa a exclusão de um cargo.
        """

        # Criar um cargo temporário para exclusão
        temp_job_data = {
            "name": fake.job(),
            "department_id": self.department['id'],
            "code": "%s%s%s%s" % (
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter(),
                fake.random_letter(),
            )
        }
        response = requests.post("%s/jobs" % BASE_URL, json=temp_job_data)
        temp_job = response.json()

        # Excluir o cargo temporário
        response = requests.delete("%s/jobs/%s" % (BASE_URL, temp_job['id']))
        self.assertEqual(response.status_code, 200)

        # Verificar que o cargo foi excluído
        response = requests.get("%s/jobs/%s" % (BASE_URL, temp_job['id']))
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
