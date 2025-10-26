


Proprietarios:
- ID (PRIMARY KEY)
- Nome
- Email
- Telefone
- CPF (UNIQUE)

1..n (Pessoas) -> 0..n (Carros) - Um para muitos

Veiculos:
- ID (PRIMARY KEY)
- Ano
- Cor
- Placa (UNIQUE)
- ProprietarioID (FOREIGN KEY) CHAVE COMPOSTA (ProprietarioID, Placa)
- FabricanteID (FOREIGN KEY)
1..1 (Veiculos) -> 1..1 (Fabricantes) - Um para um

Fabricantes:
- ID (PRIMARY KEY)
- Nome (UNIQUE NOT NULL)


Vendas:
- ID (PRIMARY KEY)
- DataCriacao
- DataAtualizacao
- DataCancelamento
- ProprietarioID (FOREIGN KEY)
- VeiculoID (FOREIGN KEY)
- ServicoID (FOREIGN KEY)
- Total (NOT NULL) BIGDECIMAL

{
  "id": 1,
  "dataCriacao": "2025-01-01",
  "dataAtualizacao": "2025-01-01",
  "dataCancelamento": "2025-01-01",
  "total": 100.00
  "proprietario": {
    "id": 1,
    "nome": "John Doe"
  },
  "veiculo": {
    "id": 1,
    "ano": 2014,
    "cor": "Preto",
    "placa": "FV-1234",
    "fabricante": {
      "id": 1,
      "nome": "Audi"
    }
  }
  "servicos": [{
    "id": 1,
    "nome": "Servico 1"
    "preco": 100.00
    "quantidade": 1
    "total": 100.00
  },
  {
    "id": 2,
    "nome": "Servico 2",
    "preco": 200.00
    "quantidade": 2
    "total": 400.00
  }]
}

1..n (Vendas) -> 1..n (Veiculos) -> 1..n (Servicos) - Um para muitos

Servicos:
- ID (PRIMARY KEY)
- Nome (UNIQUE NOT NULL)
- Descricao (NOT NULL)
- Preco (NOT NULL) BIGDECIMAL


- Qual o total de vendas por fabricante?
//GET /relatorios/vendas/fabricantes?inicio=2025-01-01&fim=2025-01-31
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
      "quantidade": 20
    }
  ]
}

- Qual o total de vendas por servico?
//GET /relatorios/vendas/servicos?inicio=2025-01-01&fim=2025-01-31
{
  "data": [
    {
      "servico": {
        "id": 1,
        "nome": "Servico 1"
      },
      "quantidade": 10
    }
  ]
}

- Qual o total de vendas por proprietario?
//GET /relatorios/vendas/proprietarios?inicio=2025-01-01&fim=2025-01-31
{
  "data": [
    {
      "proprietario": {
        "id": 1,
        "nome": "John Doe"
      },
      "quantidade": 10
    }
  ]
}

// GET /proprietarios?page=1&limit=2
{
    "data": [
          {
              "id": 1,
              "nome": "John Doe",
              "email": "john.doe@example.com",
              "telefone": "1234567890",
              "cpf": "1234567890",
          },
              {
              "id": 2,
              "nome": "Jane Doe",
              "email": "jane.doe@example.com",
              "telefone": "0987654321",
              "cpf": "1234567890",
          }
    ],
    "total": 100,
    "page": 1,
    "limit": 2,
    "totalPages": 50
}

//GET /proprietarios/1/veiculos
{
    "data": [
        {
            "id": 1,
            "ano": 2014,
            "cor": "Preto",
            "placa": "FV-1234",
            "fabricante": {
                "id": 1,
                "nome": "Audi"
            }
        },
        {
            "id": 2,
            "ano": 2015,
            "cor": "Prata",
            "placa": "FV-1A235",
            "fabricante": {
                "id": 1,
                "nome": "Audi"
            }
        }
    ]
}
