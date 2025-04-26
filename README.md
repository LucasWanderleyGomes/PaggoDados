```markdown
# ETL Pipeline com FastAPI e PostgreSQL

Este projeto simula um pipeline de ETL onde dados são extraídos de um banco PostgreSQL via API (protegendo o acesso direto), transformados com agregações e carregados em um segundo banco de dados. O objetivo é apresentar uma arquitetura moderna, desacoplada e robusta, utilizando Python, FastAPI, SQLAlchemy e Pandas.

---

## Pré-requisitos

⚠️ Python 3.10 ou superior  
⚠️ PostgreSQL (ex: versão 13+, com acesso via localhost)  
⚠️ pgAdmin (opcional, para administração dos bancos de dados)

Siga as instruções para garantir que você tem o ambiente pronto.

---

## Visão Geral do Projeto

- **Banco fonte:** contém dados simulados de sensores gravados a cada minuto por 10 dias.
- **API** (FastAPI): protege o acesso ao banco de dados fonte, fornecendo dados filtrados conforme parâmetro de tempo e variáveis selecionadas.
- **Banco alvo:** recebe agregações 10-minutais (média, min, max, std) por variável, que são processadas pelo ETL.
- **Script ETL:** extrai dados via API, executa as transformações e grava no banco de dados alvo.
- **(Opcional)** Docker para orquestração fácil dos serviços.

---

## Configuração Inicial

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie os dois bancos de dados (no pgAdmin ou terminal)

- **Banco fonte:** `fonte`
- **Banco alvo:** `alvo`

### 3. Crie as tabelas 

No banco **fonte**:

```sql
CREATE TABLE data (
  timestamp TIMESTAMP PRIMARY KEY,
  wind_speed FLOAT,
  power FLOAT,
  ambient_temperature FLOAT
);
```

No banco **alvo**:

```sql
CREATE TABLE signal (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE signal_data (
  id SERIAL PRIMARY KEY,
  signal_id INTEGER REFERENCES signal(id),
  timestamp TIMESTAMP,
  value FLOAT,
  min_value FLOAT,
  max_value FLOAT,
  std_value FLOAT
);
```

---

## Populando o Banco Fonte

Acesse o diretório do script:
```bash
cd fonte_db
```

Altere a string de conexão do `load_fonte.py` de acordo com suas credenciais PostgreSQL (usuário/senha/porta).

Instale dependências:
```bash
pip install pandas sqlalchemy numpy psycopg2
```

Rode o script para povoar a tabela:
```bash
python load_fonte.py
```
Após rodar, o banco **fonte** terá 10 dias de dados minutais.

---

## Criando e povoando a tabela de sinais no banco alvo

Acesse o diretório:
```bash
cd ../alvo_db
```

Ajuste a string de conexão do `create_alvo.py` conforme suas credenciais.

Execute o script para criar as tabelas e inserir os sinais (`wind_speed` e `power`):

```bash
python create_alvo.py
```

---

## Subindo a API FastAPI

Vá para o diretório da API:

```bash
cd ../api_fonte
```

Instale dependências necessárias:

```bash
pip install fastapi uvicorn sqlalchemy pandas psycopg2
```

**Inicie a API:**

```bash
python -m uvicorn main:app --reload --port 8000
```

Acesse a documentação interativa:  
[http://localhost:8000/docs](http://localhost:8000/docs)

Você pode testar a rota `/data`, passando parâmetros como:

- start: `2023-01-01T00:00:00`
- end: `2023-01-02T00:00:00`
- variables: `wind_speed`, `power`

---

## Executando o ETL

Abra **outro terminal** e acesse a pasta do ETL:

```bash
cd ../etl
```

Instale as dependências:

```bash
pip install httpx pandas sqlalchemy psycopg2
```

Edite o script `etl.py` para garantir que a URL da API, usuário, senha e porta do banco alvo estão corretos.

Execute o ETL informando uma data presente na base (exemplo):

```bash
python etl.py
```

O script faz:

1. Consulta a API por um período de 1 dia.
2. Agrega as variáveis `wind_speed` e `power` a cada 10 minutos.
3. Escreve esses dados agregados no banco `alvo`, tabela `signal_data`.

---

## Conferindo os Resultados

Abra o **pgAdmin** na base `alvo`.  
Execute:

```sql
SELECT * FROM signal_data LIMIT 10;
```

Você deverá ver agregações 10-minutais de cada sinal.

---

## Estrutura de Pastas

```
etl-pipeline/
├── fonte_db/
│   └── load_fonte.py
├── alvo_db/
│   └── create_alvo.py
│   └── models.py
├── api_fonte/
│   ├── main.py
├── etl/
│   └── etl.py
├── README.md
```

---

## Observações Finais

- Deixe a API rodando durante a execução do ETL.
- Para processar outros dias, altere a data no script ETL.
- Certifique-se de editar as strings de conexão para refletir seu usuário, senha e porta!
- Se desejar rodar tudo via Docker, adicione os arquivos de orquestração posteriormente.

---

## Exemplo de uso

1. Rode a API em um terminal.
2. Em outro terminal, execute o ETL.
3. Verifique os dados agregados no banco alvo.

---

## Funcionamento resumido

- **Banco fonte** → **API FastAPI** → **ETL (Python)** → **Banco alvo**

---

Pronto! Pipeline testado e funcional.
```
