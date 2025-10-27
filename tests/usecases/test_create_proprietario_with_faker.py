import unittest
from tests.factories.proprietario_factory import create_proprietario
from carify.repositories.proprietario import ProprietarioRepositoryInMemory
from carify.usecases.proprietario import CreateProprietarioUseCase

class TestCreateProprietarioUseCaseWithFaker(unittest.TestCase):
    def setUp(self):
        self.repository = ProprietarioRepositoryInMemory()
        self.usecase = CreateProprietarioUseCase(self.repository)

    def test_should_create_proprietario_with_fake_data(self):
        prop = create_proprietario()

        result = self.usecase.execute(
            nome=prop.nome,
            email=prop.email,
            telefone=prop.telefone,
            cpf=prop.cpf
        )

        self.assertIsNotNone(result.id)
        self.assertEqual(result.nome, prop.nome)
        self.assertEqual(result.email, prop.email)
        self.assertEqual(result.cpf, prop.cpf)

    def test_should_create_multiple_proprietarios(self):
        for i in range(10):
            prop = create_proprietario()
            result = self.usecase.execute(
                nome=prop.nome,
                email=prop.email,
                telefone=prop.telefone,
                cpf=prop.cpf
            )
            self.assertEqual(result.id, i + 1)

        self.assertEqual(len(self.repository.proprietarios), 10)

    def test_should_override_specific_fields(self):
        prop = create_proprietario(nome='John Doe', cpf='12345678900')

        result = self.usecase.execute(
            nome=prop.nome,
            email=prop.email,
            telefone=prop.telefone,
            cpf=prop.cpf
        )

        self.assertEqual(result.nome, 'John Doe')
        self.assertEqual(result.cpf, '12345678900')

if __name__ == '__main__':
    unittest.main()
