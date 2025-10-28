from pydantic import BaseModel, Field, EmailStr

class Proprietario(BaseModel):
    id: int | None = None
    nome: str = Field(min_length=3, max_length=100)
    email: EmailStr
    telefone: str = Field(min_length=10, max_length=15)
    cpf: str = Field(min_length=11, max_length=11)
