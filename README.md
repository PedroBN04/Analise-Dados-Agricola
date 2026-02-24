# Análise de Dados Agrícolas com Python e MySQL

## Visão Geral
Este projeto realiza a análise de dados de plantio e colheita, armazenando as informações em um banco de dados MySQL e gerando insights através de visualizações gráficas. O objetivo é facilitar a tomada de decisão no setor agrícola, identificando padrões de produtividade e possíveis ineficiências.

## Funcionalidades
- **Carregamento de Dados**: Importa dados de plantio e colheita a partir de arquivos CSV.
- **Transformação de Dados**: Renomeia colunas, converte tipos de dados e calcula métricas como produtividade e duração do plantio.
- **Armazenamento no MySQL**: Cria tabelas no banco de dados e insere os dados processados.
- **Criação de Views para Análise no Power BI**: Gera visões agregadas de produtividade e rendimento.
- **Análise Estatística**: Calcula produtividade média por cultura e fazenda, identifica baixa produtividade e outliers.
- **Visualizações Gráficas**: Gera gráficos de produtividade para insights visuais.

## Tecnologias Utilizadas
- **Linguagem**: Python
- **Bibliotecas**: Pandas, SQLAlchemy, Matplotlib, Seaborn
- **Banco de Dados**: MySQL

## Requisitos
- Python 3.x
- MySQL Server
- Bibliotecas Python:
  ```sh
  pip install pandas sqlalchemy pymysql matplotlib seaborn
  ```

## Como Executar
1. **Configurar Banco de Dados:**
   - Certifique-se de que o MySQL está rodando e que as credenciais estão configuradas corretamente no código.

2. **Executar o Script:**
   - Rode o arquivo Python para processar os dados e carregá-los no banco.
   ```sh
   python script.py
   ```

3. **Visualizar os Resultados:**
   - Consulte as tabelas e views no MySQL.
   - Analise os relatórios gráficos gerados pelo script.

## Exemplo de Saída
- **Produtividade Média por Cultura:**
  ```
  Cultura       Produtividade (Kg/Há)
  Soja                   3200.5
  Milho                  2800.2
  Trigo                  1800.7
  ```
- **Gráfico de Produtividade**:
  ![Exemplo de Gráfico](#)

## Contribuição
Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades. Para isso:
1. Faça um fork do repositório.
2. Crie uma branch para sua modificação (`git checkout -b minha-melhoria`).
3. Commit suas mudanças (`git commit -m 'Melhoria na análise'`).
4. Faça push para a branch (`git push origin minha-melhoria`).
5. Abra um Pull Request.

## Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usar e modificar conforme necessário.

---
Criado por Pedro Humberto Bitencourt Nascimento
