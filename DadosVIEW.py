# Importando bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurando estilo de gráficos
sns.set(style="whitegrid")

# Etapa 2: Carregar os dados
# Ajuste os caminhos para os arquivos corretos
plantio_df = pd.read_csv(r'PATH_PLANTIO', sep=';', decimal=',')
colheita_df = pd.read_csv(r'PATH_COLHEITA', sep=';', decimal=',')

# Visualizando as primeiras linhas
print("Dados do Plantio:")
print(plantio_df.head())
print("\nDados da Colheita:")
print(colheita_df.head())

# Etapa 3: Limpeza de Dados

# Diagnóstico inicial das colunas
print("\nInformações do Plantio:")
print(plantio_df.info())
print("\nInformações da Colheita:")
print(colheita_df.info())

# Tratamento da coluna 'Area Plantio (ha)'
if plantio_df['Area Plantio (ha)'].dtype == 'object':  # Se os valores forem strings
    plantio_df['Area Plantio (ha)'] = plantio_df['Area Plantio (ha)'].str.replace(',', '.').astype(float)

# Convertendo colunas de datas
plantio_df['Data Inicio Plantio'] = pd.to_datetime(plantio_df['Data Inicio Plantio'], format='%d/%m/%Y', errors='coerce')
plantio_df['Data Fim Plantio'] = pd.to_datetime(plantio_df['Data Fim Plantio'], format='%d/%m/%Y', errors='coerce')

# Tratamento da coluna 'Area Colhida (Há)'
colheita_df['Area Colhida (Há)'] = pd.to_numeric(colheita_df['Area Colhida (Há)'], errors='coerce')

# Ajustando a coluna 'Colhido (Kg)'
colheita_df['Colhido (Kg)'] = pd.to_numeric(colheita_df['Colhido (Kg)'], errors='coerce')

# Criando coluna de produtividade
colheita_df['Produtividade (Kg/Há)'] = colheita_df['Colhido (Kg)'] / colheita_df['Area Colhida (Há)']

# Verificando dados ausentes
print("\nDados ausentes no Plantio:")
print(plantio_df.isnull().sum())
print("\nDados ausentes na Colheita:")
print(colheita_df.isnull().sum())

# Tratamento de valores ausentes
colheita_df['Produtividade (Kg/Há)'].fillna(colheita_df['Produtividade (Kg/Há)'].mean(), inplace=True)

# Etapa 4: Análise de Dados

# Produtividade média por cultura
produtividade_cultura = colheita_df.groupby('Cultura')['Produtividade (Kg/Há)'].mean().sort_values(ascending=False)
print("\nProdutividade média por cultura (Kg/Há):")
print(produtividade_cultura)

# Identificando culturas com baixa produtividade
baixa_produtividade = colheita_df[colheita_df['Produtividade (Kg/Há)'] < 1000]
print("\nCulturas com baixa produtividade (Kg/Há < 1000):")
print(baixa_produtividade)

# Visualizações
# Gráfico de barras para produtividade média por cultura
produtividade_cultura.plot(kind='bar', figsize=(10, 6), title='Produtividade Média por Cultura')
plt.xlabel('Cultura')
plt.ylabel('Produtividade (Kg/Há)')
plt.show()

# Histograma para produtividade geral
sns.histplot(colheita_df['Produtividade (Kg/Há)'], kde=True, bins=20)
plt.title('Distribuição da Produtividade (Kg/Há)')
plt.xlabel('Produtividade (Kg/Há)')
plt.ylabel('Frequência')
plt.show()

# Análise de produtividade por fazenda
produtividade_fazenda = colheita_df.groupby('Fazenda')['Produtividade (Kg/Há)'].mean().sort_values(ascending=False)
print("\nProdutividade média por fazenda (Kg/Há):")
print(produtividade_fazenda)

# Duração do plantio
plantio_df['Duracao Plantio (dias)'] = (plantio_df['Data Fim Plantio'] - plantio_df['Data Inicio Plantio']).dt.days
sns.scatterplot(data=plantio_df, x='Duracao Plantio (dias)', y='Area Plantio (ha)')
plt.title('Duração do Plantio vs Área Plantada')
plt.xlabel('Duração do Plantio (dias)')
plt.ylabel('Área Plantada (ha)')
plt.show()

# Identificação de outliers
Q1 = colheita_df['Produtividade (Kg/Há)'].quantile(0.25)
Q3 = colheita_df['Produtividade (Kg/Há)'].quantile(0.75)
IQR = Q3 - Q1
outliers = colheita_df[(colheita_df['Produtividade (Kg/Há)'] < (Q1 - 1.5 * IQR)) | 
                       (colheita_df['Produtividade (Kg/Há)'] > (Q3 + 1.5 * IQR))]
print("\nOutliers de produtividade:")
print(outliers)
