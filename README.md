# Carify - Sistema de Gerenciamento de Oficina

Sistema para gestão de proprietários, veículos, fabricantes, serviços e vendas.

---

## 🚀 Quick Start

### Setup Completo (Recomendado)

```bash
# Ver todos os comandos disponíveis
make help

# Setup completo: instala + inicia Jaeger + roda servidor
make dev

# Com observabilidade completa (Jaeger + Grafana)
make observability
make run
```

### Comandos Principais

```bash
# Desenvolvimento
make install          # Instala dependências
make run              # Roda servidor
make test             # Executa testes
make clean            # Limpa cache

# Docker/Observabilidade
make docker-up        # Inicia todos os serviços
make docker-jaeger    # Inicia apenas Jaeger
make docker-grafana   # Inicia Grafana + Tempo
make jaeger          # Abre Jaeger UI
make grafana         # Abre Grafana UI

# Documentação
make docs            # Abre Swagger UI
```

### Testar a API

Use o arquivo **`api.http`** com a extensão [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) do VSCode:

1. Abra o arquivo `api.http`
2. Clique em "Send Request" acima de cada endpoint
3. Veja a resposta diretamente no VSCode

**OU use o Scalar UI:**
```
http://localhost:3000/docs/scalar/
```

---

## 📋 Modelo de Domínio

### Entidades e Relacionamentos

```
Proprietarios (1..n) ←→ (0..n) Veiculos
Veiculos (n..1) → (1..1) Fabricantes
Vendas (n..1) → (1..1) Proprietarios
Vendas (n..1) → (1..1) Veiculos
Vendas (1..n) ←→ (1..n) Servicos
```

---

## 🎯 Regras de Negócio

### Gestão de Proprietários

- ✅ CPF deve ser único no sistema
- ✅ Todos os campos são obrigatórios (nome, email, telefone, cpf)
- ✅ CPF duplicado retorna erro
- ✅ Listagem com paginação (page, limit)
- ✅ Buscar veículos por proprietário

### Gestão de Veículos

- ✅ Placa deve ser única no sistema
- ✅ Fabricante é obrigatório
- ✅ Proprietário é opcional (pode não ter dono)
- ✅ Placa duplicada retorna erro
- ✅ Veículo vinculado a um fabricante

### Gestão de Fabricantes

- ✅ Nome deve ser único no sistema
- ✅ Nome é obrigatório
- ✅ Nome duplicado retorna erro

### Gestão de Serviços

- ✅ Nome deve ser único no sistema
- ✅ Preço é obrigatório e deve ser positivo
- ✅ Descrição é obrigatória
- ✅ Preço zero ou negativo retorna erro

### Gestão de Vendas

- ✅ Proprietário e veículo são obrigatórios
- ✅ Deve ter pelo menos um serviço
- ✅ Total calculado automaticamente (soma dos serviços × quantidades)
- ✅ Data de criação registrada automaticamente
- ✅ Data de atualização registrada ao modificar
- ✅ Vendas podem ser canceladas (data de cancelamento)
- ✅ Vendas canceladas não aparecem em relatórios

### Relatórios

- ✅ Vendas por fabricante (período)
- ✅ Vendas por serviço (período)
- ✅ Vendas por proprietário (período)
- ✅ Filtros por data (início e fim)
- ✅ Apenas vendas ativas (não canceladas)

---

## 🗄️ Estrutura de Dados

### Proprietarios
```
- id: INTEGER (PRIMARY KEY)
- nome: VARCHAR(255) NOT NULL
- email: VARCHAR(255) NOT NULL
- telefone: VARCHAR(20) NOT NULL
- cpf: VARCHAR(11) UNIQUE NOT NULL
```

### Veiculos
```
- id: INTEGER (PRIMARY KEY)
- ano: INTEGER NOT NULL
- cor: VARCHAR(50) NOT NULL
- placa: VARCHAR(10) UNIQUE NOT NULL
- proprietario_id: INTEGER (FOREIGN KEY)
- fabricante_id: INTEGER (FOREIGN KEY) NOT NULL
```

### Fabricantes
```
- id: INTEGER (PRIMARY KEY)
- nome: VARCHAR(255) UNIQUE NOT NULL
```

### Servicos
```
- id: INTEGER (PRIMARY KEY)
- nome: VARCHAR(255) UNIQUE NOT NULL
- descricao: TEXT NOT NULL
- preco: DECIMAL(10,2) NOT NULL
```

### Vendas
```
- id: INTEGER (PRIMARY KEY)
- data_criacao: TIMESTAMP NOT NULL DEFAULT NOW()
- data_atualizacao: TIMESTAMP
- data_cancelamento: TIMESTAMP
- proprietario_id: INTEGER (FOREIGN KEY) NOT NULL
- veiculo_id: INTEGER (FOREIGN KEY) NOT NULL
- total: DECIMAL(10,2) NOT NULL
```

### VendasServicos (Tabela Associativa)
```
- venda_id: INTEGER (FOREIGN KEY)
- servico_id: INTEGER (FOREIGN KEY)
- quantidade: INTEGER NOT NULL
- preco_unitario: DECIMAL(10,2) NOT NULL
- total: DECIMAL(10,2) NOT NULL
PRIMARY KEY (venda_id, servico_id)
```

---

## 📡 Endpoints da API

### Proprietários

#### `POST /proprietarios`
Cadastrar novo proprietário
```json
Request:
{
  "nome": "John Doe",
  "email": "john.doe@example.com",
  "telefone": "1234567890",
  "cpf": "12345678900"
}

Response: 201 Created
{
  "id": 1,
  "nome": "John Doe",
  "email": "john.doe@example.com",
  "telefone": "1234567890",
  "cpf": "12345678900"
}
```

#### `GET /proprietarios?page=1&limit=10`
Listar proprietários com paginação
```json
Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "nome": "John Doe",
      "email": "john.doe@example.com",
      "telefone": "1234567890",
      "cpf": "12345678900"
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 10,
  "totalPages": 10
}
```

#### `GET /proprietarios/{id}/veiculos`
Buscar veículos de um proprietário
```json
Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "ano": 2014,
      "cor": "Preto",
      "placa": "ABC-1234",
      "fabricante": {
        "id": 1,
        "nome": "Audi"
      }
    }
  ]
}
```

---

### Vendas

#### `POST /vendas`
Criar nova venda
```json
Request:
{
  "proprietarioId": 1,
  "veiculoId": 1,
  "servicos": [
    {
      "servicoId": 1,
      "quantidade": 1
    },
    {
      "servicoId": 2,
      "quantidade": 2
    }
  ]
}

Response: 201 Created
{
  "id": 1,
  "dataCriacao": "2025-01-01T10:00:00Z",
  "dataAtualizacao": null,
  "dataCancelamento": null,
  "total": 260.00,
  "proprietario": {
    "id": 1,
    "nome": "John Doe"
  },
  "veiculo": {
    "id": 1,
    "ano": 2014,
    "cor": "Preto",
    "placa": "ABC-1234",
    "fabricante": {
      "id": 1,
      "nome": "Audi"
    }
  },
  "servicos": [
    {
      "id": 1,
      "nome": "Alinhamento",
      "preco": 100.00,
      "quantidade": 1,
      "total": 100.00
    },
    {
      "id": 2,
      "nome": "Balanceamento",
      "preco": 80.00,
      "quantidade": 2,
      "total": 160.00
    }
  ]
}
```

---

### Relatórios

#### `GET /relatorios/vendas/fabricantes?inicio=2025-01-01&fim=2025-01-31`
Relatório de vendas por fabricante
```json
Response: 200 OK
{
  "data": [
    {
      "fabricante": {
        "id": 1,
        "nome": "Audi"
      },
      "quantidade": 10
    },
    {
      "fabricante": {
        "id": 2,
        "nome": "Ford"
      },
      "quantidade": 5
    }
  ]
}
```

#### `GET /relatorios/vendas/servicos?inicio=2025-01-01&fim=2025-01-31`
Relatório de vendas por serviço
```json
Response: 200 OK
{
  "data": [
    {
      "servico": {
        "id": 1,
        "nome": "Troca de Óleo"
      },
      "quantidade": 20
    }
  ]
}
```

#### `GET /relatorios/vendas/proprietarios?inicio=2025-01-01&fim=2025-01-31`
Relatório de vendas por proprietário
```json
Response: 200 OK
{
  "data": [
    {
      "proprietario": {
        "id": 1,
        "nome": "John Doe"
      },
      "quantidade": 5
    }
  ]
}
```

---

## 🧪 Executar Testes

### Todos os Testes
```bash
poetry run python -m unittest discover tests
```

### Testes de Proprietário
```bash
poetry run python -m unittest tests.proprietario.test_usecases
```

### Teste Específico
```bash
poetry run python -m unittest tests.proprietario.test_usecases.TestCreateProprietarioUseCase.test_should_create_proprietario_successfully
```

### Executar com verbose
```bash
poetry run python -m unittest discover tests -v
```

---

## 🏗️ Arquitetura

```
carify/
├── proprietarios/             # Módulo Proprietários (tudo relacionado)
│   ├── __init__.py
│   ├── models.py             # Entidade Proprietario (Pydantic)
│   ├── dtos.py               # DTOs de request/response
│   ├── repositories.py       # Repository (interface + in-memory)
│   ├── usecases.py           # Use cases (CreateProprietarioUseCase)
│   └── routes.py             # Blueprint Flask (rotas HTTP)
│
├── exceptions/                # Exceções customizadas
│   ├── __init__.py
│   ├── base.py               # BaseError
│   ├── proprietario.py       # Exceções de proprietário
│   └── README.md             # Documentação de exceções
│
├── migrations/                # Scripts de migração do banco
│
├── tests/                     # Testes unitários
│   ├── factories/            # Geradores de dados (Faker)
│   │   └── proprietario_factory.py
│   └── proprietario/         # Testes de proprietário
│       └── test_usecases.py  # Testes unitários dos casos de uso
│
└── scripts/                   # Scripts auxiliares (seed, etc)
```

### Organização Modular

Cada entidade de domínio possui seu próprio módulo com:

1. **models.py**: Entidade de domínio (Pydantic BaseModel)
2. **dtos.py**: DTOs de request/response com validação
3. **repositories.py**: Interface + implementação do repositório
4. **usecases.py**: Casos de uso (lógica de negócio)
5. **routes.py**: Blueprint Flask com endpoints HTTP

### Vantagens

- ✅ **Alta coesão**: Tudo relacionado ao proprietário em um lugar
- ✅ **Fácil navegação**: Encontrar código é mais rápido
- ✅ **Escalável**: Adicionar nova entidade = criar nova pasta
- ✅ **Independente**: Cada módulo pode ser testado isoladamente

### Princípios

- ✅ Clean Architecture
- ✅ Dependency Inversion
- ✅ Repository Pattern
- ✅ Use Case Pattern
- ✅ Test Factories (Faker)
- ✅ Exceções Tipadas

---

## 🧪 Testes

### Estratégia de Testes

Este projeto utiliza **testes unitários** com foco em:

1. **Isolamento**: Cada caso de uso é testado independentemente
2. **Repository In-Memory**: Testes sem dependência de banco de dados
3. **Faker**: Geração de dados fictícios realistas

### Estrutura de Testes

```
tests/
├── factories/                  # Geradores de dados (Faker)
│   └── proprietario_factory.py
│
└── proprietario/               # Testes de proprietário
    └── test_usecases.py        # Testes unitários (casos de uso)
```

### Exemplo de Teste com Factory

```python
from tests.factories.proprietario_factory import create_proprietario

def test_should_create_proprietario_with_fake_data(self):
    prop = create_proprietario()

    result = self.usecase.execute(
        nome=prop.nome,
        email=prop.email,
        telefone=prop.telefone,
        cpf=prop.cpf
    )

    self.assertIsNotNone(result.id)
```

### Cobertura de Testes

- ✅ Casos de sucesso
- ✅ Validações e erros
- ✅ CPF duplicado
- ✅ Múltiplos cadastros
- ✅ Personalização de dados

Veja mais em [`tests/factories/README.md`](tests/factories/README.md)

---

## 🚀 Como Executar

### Requisitos
- Python 3.12+
- Poetry
- Make (opcional, mas recomendado)

### Instalação

**Com Make:**
```bash
make install
```

**Sem Make:**
```bash
poetry install
```

### Executar Aplicação

**Com Make:**
```bash
make run          # Modo desenvolvimento
make docs         # Abre Swagger no navegador
```

**Sem Make:**
```bash
poetry run python -m carify.app
# OU
poetry run flask --app carify.app run --debug
```

### 📚 Documentação e Observabilidade

A API estará disponível em `http://localhost:3000`

**Scalar UI (Interativo):** http://localhost:3000/docs/scalar/

**Jaeger (Tracing):** http://localhost:16686
**Grafana (Métricas):** http://localhost:3001 (admin/admin)
**Prometheus (Métricas):** http://localhost:9090
**Loki (Logs):** http://localhost:3100

### Testar API

#### Opção 1: Arquivo `.http` (Recomendado)

Use o arquivo **`api.http`** com a extensão [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) do VSCode:

1. Abra `api.http`
2. Clique em "Send Request" acima dos endpoints
3. Veja as respostas em tempo real

#### Opção 2: cURL

**Verificar saúde da API:**
```bash
curl http://localhost:3000/health
```

**Criar proprietário:**
```bash
curl -X POST http://localhost:3000/proprietarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "John Doe",
    "email": "john@example.com",
    "telefone": "11999999999",
    "cpf": "12345678900"
  }'
```

#### Listar proprietários
```bash
curl http://localhost:3000/proprietarios
```

#### Buscar proprietário por ID
```bash
curl http://localhost:3000/proprietarios/1
```

### Executar Testes Unitários
```bash
poetry run python -m unittest discover tests
```

### Gerar Dados Fictícios (Seed)
```bash
poetry run python scripts/seed_data.py
```

---

## 🔍 Observabilidade

### OpenTelemetry + Jaeger + Grafana

O projeto inclui observabilidade completa com:

- **OpenTelemetry**: Instrumentação automática do Flask
- **Jaeger**: Visualização de traces distribuídos
- **Grafana + Tempo**: Dashboards e métricas
- **Error Tracking**: Captura automática de exceções

### Configuração

```bash
# Iniciar observabilidade
make observability

# Ou apenas Jaeger
make docker-jaeger

# Ver traces
make jaeger
```

### Serviços Docker

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| API | 3000 | Aplicação principal |
| Jaeger | 16686 | UI de traces |
| Grafana | 3001 | Dashboards (admin/admin) |
| Prometheus | 9090 | Coleta de métricas |
| Loki | 3100 | Coleta de logs |
| Tempo | 3200 | Backend de traces |
| MariaDB | 3306 | Banco de dados |

### Comandos Docker

```bash
make docker-up        # Inicia todos os serviços
make docker-down      # Para todos os serviços
make docker-logs      # Ver logs
make docker-clean     # Remove volumes
```
