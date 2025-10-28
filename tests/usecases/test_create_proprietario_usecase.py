import unittest
from carify.domain.proprietario import Proprietario
from carify.repositories.proprietario import ProprietarioRepositoryInMemory
from carify.usecases.proprietario import CreateProprietarioUseCase

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

        self.assertEqual(result.id, 1)
        self.assertEqual(result.nome, 'John Doe')
        self.assertEqual(result.email, 'john.doe@example.com')
        self.assertEqual(result.telefone, '1234567890')
        self.assertEqual(result.cpf, '12345678900')

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

        with self.assertRaises(ValueError) as context:
            self.usecase.execute(
                nome='John Doe',
                email='john.doe@example.com',
                telefone='1234567890',
                cpf='12345678900'
            )

        self.assertIn('CPF 12345678900 já cadastrado', str(context.exception))

        all_proprietarios = list(self.repository.proprietarios.values())
        self.assertEqual(len(all_proprietarios), 1)
        self.assertEqual(all_proprietarios[0].nome, 'Existing User')

if __name__ == '__main__':
    unittest.main()
