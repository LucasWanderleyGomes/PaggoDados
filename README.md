# ETL Pipeline - Teste Prático

Este projeto consiste em um pipeline de ETL, utilizando dois bancos PostgreSQL (fonte e alvo), uma API FastAPI para consulta no fonte e um script ETL para processar e transferir os dados para o alvo.

## Pré-requisitos

- Python 3.10+
- PostgreSQL instalado
- pgAdmin (opcional, para gerenciar os bancos)
- pip (gerenciador de pacotes Python)

## 1. Configure os bancos de dados

### 1.1. Crie dois bancos PostgreSQL: `fonte` e `alvo`
No pgAdmin ou terminal, crie dois bancos:
- **fonte**
- **alvo**

### 1.2. Crie as tabelas
No banco `fonte`, rode:
```sql
CREATE TABLE data (
  timestamp TIMESTAMP PRIMARY KEY,
  wind_speed FLOAT,
  power FLOAT,
  ambient_temperature FLOAT
);
```
No banco alvo, rode:
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

## 2. Popule o banco fonte com dados aleatórios
Navegue até a pasta fonte_db:
``` cd fonte_db ```

Edite load_fonte.py para colocar seu usuário, senha, host e porta corretos:
```python
engine = create_engine('postgresql://postgres:SUA_SENHA@localhost:5433/fonte')
```

Instale as dependências (se já não tem):
```python
pip install pandas sqlalchemy numpy psycopg2
```

Execute o script:
```python
python load_fonte.py
```

## 3. Crie e popule a tabela 'signal' no banco alvo
Navegue até a pasta alvo_db:
```python
cd ../alvo_db
```

Edite create_alvo.py para colocar seu usuário, senha, host e porta corretos.
Execute o script:
```python
python create_alvo.py
```

## 4. Rode a API FastAPI
Navegue até a pasta onde está seu main.py (geralmente api_fonte):
```python
cd ../api_fonte
```
Instale as dependências:
```python
pip install fastapi uvicorn sqlalchemy pandas psycopg2
```

Rode a API:
```python
python -m uvicorn main:app --reload --port 8000
```

Acesse a documentação interativa da API:
```
http://localhost:8000/docs
```

## 5. Rode o script ETL

Abra outro terminal, navegue até a pasta etl:
```
cd ../etl
```

Instale as dependências (se necessário):
```
pip install httpx pandas sqlalchemy psycopg2
```

Execute o ETL informando uma data dentro do intervalo dos dados (exemplo):
```
python etl.py
```

Você também pode editar o script para mudar a data de referência.


## 6. Confira os resultados

Abra o banco 'alvo' no pgAdmin ou Query Tool e execute:
```sql
SELECT * FROM signal_data LIMIT 10;
```

Você verá os dados processados de wind_speed e power, agregados a cada 10 minutos.


## Observações
# Deixe a API rodando enquanto executa o ETL.
# Se quiser modificar datas, faça no ETL ou na consulta da API.
# Para outras dúvidas, consulte os comentários nos scripts ou abra uma issue.
