# 🚀 Guia de Estudo - Stack de Desenvolvimento Carify

Este guia apresenta os comandos essenciais e conceitos fundamentais para trabalhar com a stack de desenvolvimento do projeto Carify.

## 📋 Índice

1. [WSL](#wsl)
2. [Docker](#docker)
3. [PyEnv](#pyenv)
4. [Poetry](#poetry)
5. [Alembic](#alembic)
6. [Bash](#bash)
7. [Fluxo de Trabalho](#fluxo-de-trabalho)

---

## 🪟 WSL (Windows Subsystem for Linux)

**Documentação oficial:** https://docs.microsoft.com/en-us/windows/wsl/

### Comandos Essenciais

| Comando | Descrição |
|---------|-----------|
| `wsl --list --verbose` | Listar distribuições instaladas |
| `wsl --set-default <distro>` | Definir distribuição padrão |
| `wsl --shutdown` | Desligar todas as instâncias WSL |
| `wsl --update` | Atualizar WSL para versão mais recente |
| `wsl --status` | Verificar status do WSL |

### Comandos de Distribuição

```bash
# Entrar no WSL
wsl

# Executar comando específico no WSL
wsl -d Ubuntu-20.04 -- <comando>

# Sair do WSL
exit
```

### Configuração e Instalação

```bash
# Instalar WSL2 (Windows PowerShell como Admin)
wsl --install

# Instalar distribuição específica
wsl --install -d Ubuntu-22.04

# Converter WSL1 para WSL2
wsl --set-version Ubuntu-20.04 2
```

### Conceitos Importantes
- **WSL1**: Emulação de sistema Linux
- **WSL2**: Máquina virtual Linux completa
- **Integração**: Acesso a arquivos Windows e Linux
- **Performance**: WSL2 oferece melhor performance

### Configurações Úteis

```bash
# Configurar memória máxima do WSL2
# Criar arquivo: C:\Users\<user>\.wslconfig
[wsl2]
memory=8GB
processors=4
swap=2GB
```

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

### 1. Configuração Inicial (WSL + Ambiente)

```bash
# Verificar WSL
wsl --status

# Entrar no WSL
wsl

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
# Entrar no WSL (se necessário)
wsl

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

- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Docker Documentation](https://docs.docker.com/)
- [PyEnv GitHub](https://github.com/pyenv/pyenv)
- [Poetry Documentation](https://python-poetry.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

