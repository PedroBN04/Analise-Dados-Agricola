# Análise de Dados Agrícolas com Python e MySQL

Pipeline de análise de dados de plantio e colheita integrado ao MySQL. O sistema importa arquivos CSV, transforma e persiste os dados, gera views prontas para consumo no Power BI e produz visualizações estatísticas para suporte à tomada de decisão no setor agrícola.

---

## Sumário

1. [Funcionalidades](#funcionalidades)
2. [Arquitetura do Pipeline](#arquitetura-do-pipeline)
3. [Tecnologias](#tecnologias)
4. [Pré-requisitos](#pré-requisitos)
5. [Instalação](#instalação)
6. [Configuração](#configuração)
7. [Como Executar](#como-executar)
8. [Exemplo de Saída](#exemplo-de-saída)
9. [Contribuição](#contribuição)
10. [Licença](#licença)

---

## Funcionalidades

**Carregamento de dados**
Importação de arquivos CSV com dados de plantio e colheita para processamento em memória via Pandas.

**Transformação de dados**
Renomeação de colunas, conversão de tipos e cálculo de métricas derivadas: produtividade (Kg/ha) e duração do ciclo de plantio.

**Persistência no MySQL**
Criação automática de tabelas e inserção dos dados processados no banco de dados relacional.

**Views para Power BI**
Geração de views SQL com agregações de produtividade e rendimento, prontas para conexão direta ao Power BI.

**Análise estatística**
Cálculo de produtividade média por cultura e fazenda, detecção de baixa produtividade e identificação de outliers.

**Visualizações gráficas**
Geração de gráficos de produtividade com Matplotlib e Seaborn para análise exploratória direta no terminal.

---

## Arquitetura do Pipeline

```
arquivos CSV (plantio / colheita)
        │
        ▼
[ Carregamento — Pandas ]
        │  leitura e parsing
        ▼
[ Transformação ]
        │  renomeação · conversão de tipos · cálculo de métricas
        ▼
[ Persistência — SQLAlchemy + MySQL ]
        │  criação de tabelas + inserção de dados
        ├──────────────────────────────┐
        ▼                              ▼
[ Views SQL ]               [ Análise Estatística ]
  pronto para Power BI        produtividade média
                               outliers · alertas
        │                              │
        └──────────────┬───────────────┘
                       ▼
             [ Visualizações Gráficas ]
               Matplotlib · Seaborn
```

---

## Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| Pandas | — | Carregamento e transformação de dados |
| SQLAlchemy | — | Abstração da camada de persistência |
| PyMySQL | — | Driver de conexão ao MySQL |
| Matplotlib | — | Geração de gráficos |
| Seaborn | — | Visualizações estatísticas |
| MySQL Server | 8.0+ | Banco de dados relacional |

---

## Pré-requisitos

- Python 3.8+
- MySQL Server 8.0+ em execução
- Credenciais de acesso ao banco de dados (usuário, senha, host, nome do banco)

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/PedroBN04/analise-agricola.git
cd analise-agricola

# 2. Instale as dependências Python
pip install pandas sqlalchemy pymysql matplotlib seaborn
```

---

## Configuração

Antes de executar, configure as credenciais do banco de dados no script principal. Localize o bloco de conexão e substitua os valores:

```python
DB_USER     = "seu_usuario"
DB_PASSWORD = "sua_senha"
DB_HOST     = "localhost"
DB_NAME     = "agricola_db"
```

Certifique-se de que o MySQL está em execução e que o banco de dados especificado em `DB_NAME` existe. As tabelas serão criadas automaticamente na primeira execução.

---

## Como Executar

```bash
python script.py
```

O script executará todas as etapas do pipeline em sequência: carregamento, transformação, persistência e geração de visualizações. Os gráficos serão exibidos ao final da execução.

Para consultar os dados persistidos e as views geradas, acesse o MySQL:

```sql
USE agricola_db;
SHOW TABLES;
SELECT * FROM view_produtividade_por_cultura;
```

---

## Exemplo de Saída

**Produtividade média por cultura**

```
Cultura    Produtividade (Kg/ha)
-------    ---------------------
Soja                      3200.5
Milho                     2800.2
Trigo                     1800.7
```

**Detecção de baixa produtividade**
Culturas abaixo do limiar configurado são sinalizadas no terminal com o nome da fazenda, cultura e valor registrado.

---

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua modificação: `git checkout -b minha-melhoria`
3. Commit suas alterações: `git commit -m 'Descrição da melhoria'`
4. Faça push para a branch: `git push origin minha-melhoria`
5. Abra um Pull Request.

---

## Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

**Autor:** Pedro Humberto Bitencourt Nascimento
