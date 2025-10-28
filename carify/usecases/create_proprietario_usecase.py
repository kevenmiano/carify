from carify.domain.proprietario import Proprietario
from carify.repositories.proprietario import ProprietarioRepository

class CreateProprietarioUseCase:
    def __init__(self, repository: ProprietarioRepository):
        self.repository = repository

    def execute(self, nome: str, email: str, telefone: str, cpf: str) -> Proprietario:
        existing = self.repository.find_by_cpf(cpf)
        if existing:
            raise ValueError(f"CPF {cpf} já cadastrado")

        proprietario = Proprietario(
            id=None,
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf
        )

        return self.repository.create(proprietario)
