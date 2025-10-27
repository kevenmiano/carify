from pydantic import BaseModel, Field, EmailStr


class CreateProprietarioDto(BaseModel):
    """DTO de entrada para criar um proprietário"""
    nome: str = Field(min_length=3, max_length=100, description="Nome completo do proprietário")
    email: EmailStr = Field(description="Email válido")
    telefone: str = Field(min_length=10, max_length=15, pattern=r'^\d+$', description="Telefone apenas números")
    cpf: str = Field(min_length=11, max_length=11, pattern=r'^\d{11}$', description="CPF com 11 dígitos")

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João da Silva",
                "email": "joao.silva@example.com",
                "telefone": "11987654321",
                "cpf": "12345678900"
            }
        }
