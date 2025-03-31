# API de Gerenciamento de Parcelas Agrícolas

Esta API REST foi desenvolvida com Python e FastAPI para gerenciar dados vetoriais de parcelas agrícolas. Ela utiliza:

- **PostgreSQL com PostGIS** para armazenamento e operações espaciais.
- **Celery** para processamento assíncrono (união de parcelas).
- **Redis** como broker e backend para as tasks do Celery.
- **Docker e Docker Compose** para orquestração dos serviços.

## Funcionalidades

- **Cadastro de Parcelas:** Inserção de uma ou mais parcelas utilizando formatos GeoJSON ou WKT.
- **Consulta de Parcelas:** Listagem de todas as parcelas ou filtragem por bounding box.
- **Processamento Assíncrono:** União espacial de parcelas (usando ST_Union do PostGIS) e armazenamento do resultado, com monitoramento via endpoint.

## Estrutura do Projeto

```
.
projeto/
├── app/
│   ├── app.py              # Inicialização da aplicação FastAPI e Endpoints
│   ├── celery_app.py       # Configuração do Celery
│   ├── database.py         # Funções de acesso ao banco (inserir, consultar, unir parcelas).
│   ├── tasks.py            # Definição das tasks do Celery.
├── Dockerfile              # Build da aplicação
├── docker-compose.yml      # Orquestração dos containers (API, DB, Redis, Celery)
├── requirements.txt        # Dependências Python
├── init.sql                # Script para criação da tabela e inserção de exemplos de dados (executado na criação do BD)
└── README.md               # Este arquivo.
```

## Como Rodar a Aplicação

1. **Clone o repositório (ou baixe o arquivo do projeto):**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <nome_do_repositorio>
   ```

2. **Execute o Docker Compose:**
   ```bash
   docker-compose up --build
   ```

## Exemplos de Chamadas para Cada Endpoint

### 1. Cadastro de Parcelas (POST /parcels)

- **GeoJSON:**
  ```bash
  curl -X POST "http://localhost:8000/parcels" -H "Content-Type: application/json" -d '{
    "type": "Feature",
    "properties": {
      "name": "Parcela GeoJSON Exemplo",
      "owner": "João da Silva"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[10.0,10.0],[20.0,10.0],[20.0,20.0],[10.0,20.0],[10.0,10.0]]]
    }
  }'
  ```

- **WKT:**
  ```bash
  curl -X POST "http://localhost:8000/parcels" -H "Content-Type: application/json" -d '{
    "nome": "Parcela WKT Exemplo",
    "proprietario": "Maria Oliveira",
    "geometria": "POLYGON((30 30, 40 30, 40 40, 30 40, 30 30))"
  }'
  ```

### 2. Consulta de Parcelas (GET /parcels)

- **Todas as parcelas:**
  ```bash
  curl -X GET "http://localhost:8000/parcels"
  ```

- **Filtrar por bounding box:**
  ```bash
  curl -X GET "http://localhost:8000/parcels?bbox=10,10,20,20"
  ```

### 3. Produzir União de percelas via processamento assíncrono (POST /process/union)

```bash
curl -X POST "http://localhost:8000/process/union" -H "Content-Type: application/json" -d '{"bbox": "10,10,20,20"}'
```

### 4. Verificar Status da Task (GET /process/status/{task_id})

```bash
curl -X GET "http://localhost:8000/process/status/<task_id>"
```

## Fluxo do Processamento Assíncrono

1. **/process/union:** Dispara a task Celery.
2. **Worker Celery:**
   - Busca parcelas com ST_Intersects.
   - Faz a união com ST_Union.
   - Salva o resultado com uma nova parcela.
3. **/process/status/{task_id}:** Permite acompanhar o progresso.

---
