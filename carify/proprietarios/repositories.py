from abc import ABC, abstractmethod
from .models import Proprietario

class ProprietarioRepository(ABC):
    @abstractmethod
    def create(self, proprietario: Proprietario) -> Proprietario:
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Proprietario | None:
        pass

class ProprietarioRepositoryInMemory(ProprietarioRepository):
    def __init__(self):
        self.proprietarios: dict[int, Proprietario] = {}
        self.next_id = 1

    def create(self, proprietario: Proprietario) -> Proprietario:
        proprietario_with_id = proprietario.model_copy(update={'id': self.next_id})
        self.proprietarios[self.next_id] = proprietario_with_id
        self.next_id += 1
        return proprietario_with_id

    def find_by_cpf(self, cpf: str) -> Proprietario | None:
        for proprietario in self.proprietarios.values():
            if proprietario.cpf == cpf:
                return proprietario
        return None


