from faker import Faker
from carify.proprietarios.models import Proprietario

fake = Faker('pt_BR')

def create_proprietario(**kwargs):
    defaults = {
        'id': None,
        'nome': fake.name(),
        'email': fake.email(),
        'telefone': fake.phone_number().replace('-', '').replace(' ', '').replace('(', '').replace(')', '')[:11],
        'cpf': fake.cpf().replace('.', '').replace('-', '')
    }
    defaults.update(kwargs)
    return Proprietario(**defaults)

def create_proprietarios(count: int = 5):
    return [create_proprietario() for _ in range(count)]
