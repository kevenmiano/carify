from returns.result import Result, Success, Failure
from carify.exceptions import BaseError
from carify.exceptions.proprietario import ProprietarioCPFDuplicadoException
from .models import Proprietario
from .repositories import ProprietarioRepository


class CreateProprietarioUseCase:
    def __init__(self, repository: ProprietarioRepository):
        self.repository = repository

    def execute(self, nome: str, email: str, telefone: str, cpf: str) -> Result[Proprietario, BaseError]:
        """
        Executa o caso de uso e retorna Result[Proprietario, BaseError]
        Usando a biblioteca 'returns' para Either pattern
        """
        existing = self.repository.find_by_cpf(cpf)
        if existing:
            return Failure(ProprietarioCPFDuplicadoException(cpf))

        proprietario = Proprietario(
            id=None,
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf
        )

        created = self.repository.create(proprietario)
        return Success(created)
