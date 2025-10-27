from .base import BaseError

class ProprietarioCPFDuplicadoException(BaseError):
    def __init__(self, cpf: str):
        super().__init__(f"CPF {cpf} já cadastrado", status_code=400)
        self.cpf = cpf

class ProprietarioNaoEncontradoException(BaseError):
    def __init__(self, id: int):
        super().__init__(f"Proprietário com ID {id} não encontrado", status_code=404)
        self.id = id

class ProprietarioCampoObrigatorioException(BaseError):
    def __init__(self, campo: str):
        super().__init__(f"Campo '{campo}' é obrigatório", status_code=400)
        self.campo = campo
