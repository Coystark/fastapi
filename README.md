# FastAPI Study Project

Projeto de estudos com FastAPI usando Clean Architecture.

## Arquitetura

```
app/
├── core/        # Configurações globais (env vars, logging)
├── api/v1/      # Endpoints versionados (FastAPI Routers)
├── services/    # Lógica de negócio
├── adapters/    # Integrações externas (Gemini SDK, etc.)
└── models/      # Pydantic DTOs (request/response)
```

## Setup

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -e ".[dev]"
```

## Configuração

Copie o `.env.example` para `.env` e preencha as variáveis:

```bash
cp .env.example .env
```

Variáveis disponíveis:

| Variável         | Descrição                     | Default               |
| ---------------- | ----------------------------- | --------------------- |
| `APP_NAME`       | Nome da aplicação             | FastAPI Study Project |
| `DEBUG`          | Modo debug                    | false                 |
| `GEMINI_API_KEY` | Chave de API do Google Gemini | (obrigatório)         |

## Rodando

```bash
# Desenvolvimento (auto-reload)
fastapi dev app/main.py

# Produção
fastapi run app/main.py
```

A documentação interativa fica disponível em:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testes

```bash
pytest
```

## Docker

```bash
docker build -t fastapi-study .
docker run -p 8000:8000 --env-file .env fastapi-study
```
