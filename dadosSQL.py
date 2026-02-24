# Importando bibliotecas necessárias
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns

# Configurando estilo de gráficos
sns.set(style="whitegrid")

# Etapa 1: Carregar as planilhas para DataFrames
plantio_df = pd.read_csv(r'PATH_PLANTIO', sep=';', decimal=',')
colheita_df = pd.read_csv(r'PATH_COLHEITA', sep=';', decimal=',')

# Renomeando colunas para corresponder ao esquema SQL
plantio_df.rename(columns={
    'Area Plantio (ha)': 'Area_Plantio',
    'Tipo Adubacao': 'Tipo_Adubacao',
    'Recomendacao (kg/ha)': 'Recomendacao',
    'Data Inicio Plantio': 'Data_Inicio_Plantio',
    'Data Fim Plantio': 'Data_Fim_Plantio'
}, inplace=True)

colheita_df.rename(columns={
    'Destinação': 'Destinacao',
    'Colhido (Kg)': 'Colhido_Kg',
    'Area Colhida (Há)': 'Area_Colhida',
    'Data Colheita': 'Data_Colheita'
}, inplace=True)

# Limpeza dos dados
plantio_df['Area_Plantio'] = pd.to_numeric(plantio_df['Area_Plantio'], errors='coerce')
colheita_df['Area_Colhida'] = pd.to_numeric(colheita_df['Area_Colhida'], errors='coerce')
colheita_df['Colhido_Kg'] = pd.to_numeric(colheita_df['Colhido_Kg'], errors='coerce')
colheita_df['Produtividade'] = colheita_df['Colhido_Kg'] / colheita_df['Area_Colhida']

# Convertendo colunas de datas para o formato correto
plantio_df['Data_Inicio_Plantio'] = pd.to_datetime(plantio_df['Data_Inicio_Plantio'], format='%d/%m/%Y', errors='coerce')
plantio_df['Data_Fim_Plantio'] = pd.to_datetime(plantio_df['Data_Fim_Plantio'], format='%d/%m/%Y', errors='coerce')
colheita_df['Data_Colheita'] = pd.to_datetime(colheita_df['Data_Colheita'], format='%d/%m/%Y', errors='coerce')

# Calculando a duração do plantio
plantio_df['Duracao_Plantio'] = (plantio_df['Data_Fim_Plantio'] - plantio_df['Data_Inicio_Plantio']).dt.days

# Etapa 2: Configurar conexão ao MySQL com SQLAlchemy
engine = create_engine("SQL")

# Criar tabelas no banco de dados
with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS plantio (
        Ano INT,
        Safra INT,
        Fazenda VARCHAR(255),
        Talhao VARCHAR(255),
        Cultura VARCHAR(255),
        Variedade VARCHAR(255),
        Destinacao VARCHAR(255),
        Area_Plantio FLOAT,
        Tipo_Adubacao VARCHAR(255),
        Recomendacao FLOAT,
        Data_Inicio_Plantio DATE,
        Data_Fim_Plantio DATE,
        Duracao_Plantio INT,
        Estado VARCHAR(2)
    );
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS colheita (
        Ano INT,
        Safra INT,
        Fazenda VARCHAR(255),
        Talhao VARCHAR(255),
        Cultura VARCHAR(255),
        Variedade VARCHAR(255),
        Destinacao VARCHAR(255),
        Colhido_Kg INT,
        Area_Colhida FLOAT,
        Data_Colheita DATE,
        Produtividade FLOAT
    );
    """))

# Inserir dados no banco de dados
plantio_df.to_sql('plantio', con=engine, if_exists='append', index=False)
colheita_df.to_sql('colheita', con=engine, if_exists='append', index=False)

# Criar views para facilitar análises no Power BI
with engine.connect() as conn:
    conn.execute(text("""
    CREATE OR REPLACE VIEW resumo_produtividade AS
    SELECT Cultura, Fazenda, AVG(Produtividade) AS Media_Produtividade, SUM(Colhido_Kg) AS Total_Colhido
    FROM colheita
    GROUP BY Cultura, Fazenda;
    """))

    conn.execute(text("""
    CREATE OR REPLACE VIEW rendimento_plantio_colheita AS
    SELECT p.Fazenda, p.Cultura, p.Area_Plantio, c.Area_Colhida,
           (c.Area_Colhida / p.Area_Plantio) * 100 AS Percentual_Colheita
    FROM plantio p
    JOIN colheita c ON p.Cultura = c.Cultura;
    """))

# Análise de Dados com Python
# Produtividade média por cultura
produtividade_cultura = colheita_df.groupby('Cultura')['Produtividade'].mean().sort_values(ascending=False)
print("\nProdutividade média por cultura (Kg/Há):")
print(produtividade_cultura)

# Identificando culturas com baixa produtividade
baixa_produtividade = colheita_df[colheita_df['Produtividade'] < 1000]
print("\nCulturas com baixa produtividade (Kg/Há < 1000):")
print(baixa_produtividade)

# Visualizações
# Gráfico de barras para produtividade média por cultura
produtividade_cultura.plot(kind='bar', figsize=(10, 6), title='Produtividade Média por Cultura')
plt.xlabel('Cultura')
plt.ylabel('Produtividade (Kg/Há)')
plt.show()

# Histograma para produtividade geral
sns.histplot(colheita_df['Produtividade'], kde=True, bins=20)
plt.title('Distribuição da Produtividade (Kg/Há)')
plt.xlabel('Produtividade (Kg/Há)')
plt.ylabel('Frequência')
plt.show()

# Análise de produtividade por fazenda
produtividade_fazenda = colheita_df.groupby('Fazenda')['Produtividade'].mean().sort_values(ascending=False)
print("\nProdutividade média por fazenda (Kg/Há):")
print(produtividade_fazenda)

# Identificação de outliers
Q1 = colheita_df['Produtividade'].quantile(0.25)
Q3 = colheita_df['Produtividade'].quantile(0.75)
IQR = Q3 - Q1
outliers = colheita_df[(colheita_df['Produtividade'] < (Q1 - 1.5 * IQR)) | 
                       (colheita_df['Produtividade'] > (Q3 + 1.5 * IQR))]
print("\nOutliers de produtividade:")
print(outliers)
