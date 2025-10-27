# 🚀 Guia de Estudo - Stack de Desenvolvimento Carify

Este guia apresenta os comandos essenciais e conceitos fundamentais para trabalhar com a stack de desenvolvimento do projeto Carify.

## 📋 Índice

1. [Docker](#docker)
2. [PyEnv](#pyenv)
3. [Poetry](#poetry)
4. [Alembic](#alembic)
5. [Bash](#bash)
6. [Fluxo de Trabalho](#fluxo-de-trabalho)

---

## 🐳 Docker

**Documentação oficial:** https://docs.docker.com/

### Comandos Essenciais

| Comando | Descrição |
|---------|-----------|
| `docker compose up -d` | Iniciar containers em background |
| `docker ps` | Listar containers em execução |
| `docker compose down -v` | Parar containers e remover volumes |

### Conceitos Importantes
- **Containerização**: Isolamento de aplicações
- **Docker Compose**: Orquestração de múltiplos containers
- **Volumes**: Persistência de dados

---

## 🐍 PyEnv

**Documentação oficial:** https://github.com/pyenv/pyenv

### Instalação e Configuração

```bash
# Instalar versão específica do Python
pyenv install 3.12.0

# Criar ambiente virtual
pyenv virtualenv 3.13.1 carify

# Ativar ambiente virtual
pyenv activate carify

# Listar ambientes virtuais disponíveis
pyenv virtualenvs
```

### Conceitos Importantes
- **Gerenciamento de versões**: Múltiplas versões do Python
- **Ambientes virtuais**: Isolamento de dependências
- **Ativação**: Contexto de execução

---

## 📦 Poetry

**Documentação oficial:** https://python-poetry.org/

### Comandos Fundamentais

```bash
# Criar novo projeto
poetry new carify

# Instalar dependências do projeto
poetry install

# Configurar ambiente virtual
poetry env use $(pyenv which python)

# Adicionar dependência de desenvolvimento
poetry add --dev alembic
```

### Conceitos Importantes
- **Gerenciamento de dependências**: Controle de pacotes
- **Lock file**: Versões exatas das dependências
- **Ambiente virtual**: Isolamento automático

---

## 🔄 Alembic

**Documentação oficial:** https://alembic.sqlalchemy.org/en/latest/index.html

### Comandos de Migração

```bash
# Inicializar sistema de migrações
alembic init migrations

# Criar nova migração automática
alembic revision --autogenerate -m "Add Proprietarios table"

# Aplicar migrações pendentes
alembic upgrade head

# Reverter última migração
alembic downgrade -1
```

### Conceitos Importantes
- **Migrações**: Controle de versão do banco de dados
- **Auto-generação**: Detecção automática de mudanças
- **Versionamento**: Histórico de alterações

---

## 💻 Bash

### Comandos Úteis

```bash
# Carregar variáveis de ambiente
source .env
```

### Conceitos Importantes
- **Variáveis de ambiente**: Configuração externa
- **Source**: Execução de scripts no contexto atual

---

## 🔄 Fluxo de Trabalho

### 1. Configuração Inicial
```bash
# Instalar Python
pyenv install 3.13.1

# Criar ambiente virtual
pyenv virtualenv 3.13.1 carify

# Ativar ambiente
pyenv activate carify

# Configurar Poetry
poetry env use $(pyenv which python)
```

### 2. Desenvolvimento Diário
```bash
# Ativar ambiente
pyenv activate carify

# Instalar dependências
poetry install

# Carregar variáveis
source .env

# Iniciar containers
docker compose up -d
```

### 3. Migrações de Banco
```bash
# Criar migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migração
alembic upgrade head
```

### 4. Finalização
```bash
# Parar containers
docker compose down -v
```

---

## 📚 Recursos Adicionais

- [Docker Documentation](https://docs.docker.com/)
- [PyEnv GitHub](https://github.com/pyenv/pyenv)
- [Poetry Documentation](https://python-poetry.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## ⚠️ Dicas Importantes

1. **Sempre ative o ambiente virtual** antes de trabalhar
2. **Use Poetry** para gerenciar dependências
3. **Faça backup** antes de aplicar migrações
4. **Teste localmente** antes de fazer deploy
5. **Mantenha o .env** atualizado e seguro
