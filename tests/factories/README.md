# Factories - Geradores de Dados Fictícios

Usando **Faker** para gerar dados de teste realistas.

## 🎭 Uso Básico

### ProprietarioFactory

```python
from tests.factories.proprietario_factory import create_proprietario, create_proprietarios

proprietario = create_proprietario()
proprietario = create_proprietario(nome='João Silva', cpf='12345678900')
proprietarios = create_proprietarios(count=10)
```

## 📋 Exemplos Completos

### 1. Usar em Testes Unitários

```python
import unittest
from tests.factories.proprietario_factory import create_proprietario
from carify.repositories.proprietario_repository_in_memory import ProprietarioRepositoryInMemory
from carify.usecases.create_proprietario_usecase import CreateProprietarioUseCase

class TestCreateProprietarioUseCase(unittest.TestCase):
    def setUp(self):
        self.repository = ProprietarioRepositoryInMemory()
        self.usecase = CreateProprietarioUseCase(self.repository)

    def test_should_create_multiple_proprietarios(self):
        for _ in range(10):
            prop = create_proprietario()
            result = self.usecase.execute(
                nome=prop.nome,
                email=prop.email,
                telefone=prop.telefone,
                cpf=prop.cpf
            )
            self.assertIsNotNone(result.id)
```

### 2. Seed de Dados para Desenvolvimento

```python
from tests.factories.proprietario_factory import create_proprietarios
from carify.repositories.proprietario_repository_in_memory import ProprietarioRepositoryInMemory

repository = ProprietarioRepositoryInMemory()
proprietarios = create_proprietarios(count=50)

for prop in proprietarios:
    repository.create(prop)

print(f"Criados {len(proprietarios)} proprietários!")
```

### 3. Personalizar Dados

```python
from faker import Faker
from tests.factories.proprietario_factory import create_proprietario

fake = Faker('pt_BR')

proprietario = create_proprietario(
    nome=fake.name_male(),
    email=f'{fake.first_name().lower()}@empresa.com',
    cpf='12345678900'
)
```

## 🌍 Localização

Faker suporta múltiplas localizações:

```python
from faker import Faker

fake_br = Faker('pt_BR')
fake_en = Faker('en_US')

nome_br = fake_br.name()
nome_en = fake_en.name()
```

## 📝 Dados Disponíveis do Faker

### Dados Pessoais
```python
fake.name()
fake.first_name()
fake.last_name()
fake.email()
fake.phone_number()
fake.cpf()
fake.date_of_birth()
```

### Endereços
```python
fake.address()
fake.street_address()
fake.city()
fake.state()
fake.postcode()
fake.country()
```

### Empresas
```python
fake.company()
fake.company_suffix()
fake.cnpj()
```

### Internet
```python
fake.email()
fake.url()
fake.ipv4()
fake.user_name()
```

### Texto
```python
fake.text()
fake.sentence()
fake.paragraph()
```

### Números
```python
fake.random_int(min=1, max=100)
fake.random_number(digits=5)
fake.pydecimal(left_digits=5, right_digits=2, positive=True)
```

### Datas
```python
fake.date()
fake.date_time()
fake.date_between(start_date='-30d', end_date='today')
fake.future_date()
fake.past_date()
```

## 🔧 Criar Outras Factories

### VeiculoFactory

```python
from faker import Faker
from carify.domain.veiculo import Veiculo

fake = Faker('pt_BR')

def create_veiculo(**kwargs):
    cores = ['Preto', 'Branco', 'Prata', 'Vermelho', 'Azul']
    defaults = {
        'id': None,
        'ano': fake.random_int(min=2000, max=2024),
        'cor': fake.random_element(cores),
        'placa': fake.license_plate().replace('-', ''),
        'proprietario_id': fake.random_int(min=1, max=100),
        'fabricante_id': fake.random_int(min=1, max=10)
    }
    defaults.update(kwargs)
    return Veiculo(**defaults)
```

### ServicoFactory

```python
from faker import Faker
from carify.domain.servico import Servico

fake = Faker('pt_BR')

def create_servico(**kwargs):
    servicos = [
        ('Troca de Óleo', 'Troca de óleo do motor'),
        ('Alinhamento', 'Alinhamento e balanceamento'),
        ('Revisão', 'Revisão completa do veículo')
    ]
    servico = fake.random_element(servicos)
    defaults = {
        'id': None,
        'nome': servico[0],
        'descricao': servico[1],
        'preco': fake.pydecimal(left_digits=3, right_digits=2, positive=True)
    }
    defaults.update(kwargs)
    return Servico(**defaults)
```

## 📦 Instalação

```bash
poetry add --group dev faker
```

## 📚 Documentação

- [Faker Docs](https://faker.readthedocs.io/)
- [Faker Providers](https://faker.readthedocs.io/en/master/providers.html)
