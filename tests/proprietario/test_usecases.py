import unittest
from returns.result import Success, Failure
from carify.proprietarios.models import Proprietario
from carify.proprietarios.repositories import ProprietarioRepositoryInMemory
from carify.proprietarios.usecases import CreateProprietarioUseCase
from carify.exceptions.proprietario import ProprietarioCPFDuplicadoException
from tests.factories.proprietario_factory import create_proprietario

class TestCreateProprietarioUseCase(unittest.TestCase):
    def setUp(self):
        self.repository = ProprietarioRepositoryInMemory()
        self.usecase = CreateProprietarioUseCase(self.repository)

    def test_should_create_proprietario_successfully(self):
        result = self.usecase.execute(
            nome='John Doe',
            email='john.doe@example.com',
            telefone='1234567890',
            cpf='12345678900'
        )

        # Verifica Result pattern (returns library)
        self.assertIsInstance(result, Success)

        proprietario = result.unwrap()
        self.assertEqual(proprietario.id, 1)
        self.assertEqual(proprietario.nome, 'John Doe')
        self.assertEqual(proprietario.email, 'john.doe@example.com')
        self.assertEqual(proprietario.telefone, '1234567890')
        self.assertEqual(proprietario.cpf, '12345678900')

        found = self.repository.find_by_cpf('12345678900')
        self.assertIsNotNone(found)
        self.assertEqual(found.id, 1)

    def test_should_not_create_proprietario_with_duplicate_cpf(self):
        self.repository.create(Proprietario(
            id=None,
            nome='Existing User',
            email='existing@example.com',
            telefone='0987654321',
            cpf='12345678900'
        ))

        result = self.usecase.execute(
            nome='John Doe',
            email='john.doe@example.com',
            telefone='1234567890',
            cpf='12345678900'
        )

        # Verifica Result pattern - deve falhar (returns library)
        self.assertIsInstance(result, Failure)

        error = result.failure()
        self.assertIsInstance(error, ProprietarioCPFDuplicadoException)
        self.assertEqual(error.cpf, '12345678900')
        self.assertEqual(error.status_code, 400)
        self.assertIn('CPF 12345678900 já cadastrado', error.message)

        all_proprietarios = list(self.repository.proprietarios.values())
        self.assertEqual(len(all_proprietarios), 1)
        self.assertEqual(all_proprietarios[0].nome, 'Existing User')

    def test_should_create_proprietario_with_fake_data(self):
        prop = create_proprietario()

        result = self.usecase.execute(
            nome=prop.nome,
            email=prop.email,
            telefone=prop.telefone,
            cpf=prop.cpf
        )

        self.assertIsInstance(result, Success)
        proprietario = result.unwrap()
        self.assertIsNotNone(proprietario.id)
        self.assertEqual(proprietario.nome, prop.nome)
        self.assertEqual(proprietario.email, prop.email)
        self.assertEqual(proprietario.cpf, prop.cpf)

    def test_should_create_multiple_proprietarios(self):
        for i in range(10):
            prop = create_proprietario()
            result = self.usecase.execute(
                nome=prop.nome,
                email=prop.email,
                telefone=prop.telefone,
                cpf=prop.cpf
            )
            self.assertIsInstance(result, Success)
            self.assertEqual(result.unwrap().id, i + 1)

        self.assertEqual(len(self.repository.proprietarios), 10)

    def test_should_override_specific_fields(self):
        prop = create_proprietario(nome='John Doe', cpf='12345678900')

        result = self.usecase.execute(
            nome=prop.nome,
            email=prop.email,
            telefone=prop.telefone,
            cpf=prop.cpf
        )

        self.assertIsInstance(result, Success)
        proprietario = result.unwrap()
        self.assertEqual(proprietario.nome, 'John Doe')
        self.assertEqual(proprietario.cpf, '12345678900')

if __name__ == '__main__':
    unittest.main()
