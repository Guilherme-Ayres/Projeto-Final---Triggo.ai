# Análise de Dados de Nascimentos e Mortalidades no Brasil em 2023

# 1. Visão Geral do Projeto
Este projeto implementa uma pipeline de engenharia de dados completa utilizando o Modern Data Stack para analisar dados de nascimentos e mortalidades no Brasil em 2023. A solução transforma dados brutos de fontes governamentais em um formato estruturado, confiável e pronto para análise de negócio.

# Tecnologias Utilizadas:

- Armazenamento e ELT: Snowflake

- Transformação: dbt (Data Build Tool)

- Visualização: Streamlit

# 2. Arquitetura da Solução
A arquitetura do projeto segue uma abordagem de três camadas (Medallion Architecture):

- Bronze (Raw Data): Dados brutos importados diretamente dos arquivos CSV para o Snowflake.

- Silver (Staging): Dados limpos e padronizados, com remoção de valores inconsistentes ("Total", "Município IGNORADO").

- Gold (Marts): Tabelas de fato (fat) e dimensão (dim) otimizadas para análise, prontas para consumo por ferramentas de Business Intelligence (BI).

# 3. Etapas da Pipeline de Dados
# 3.1. Ingestão de Dados
Os dados foram coletados de arquivos CSV de fontes públicas e carregados no Snowflake. As tabelas de origem são mortalidades_origem e nascimentos_vivos_origem, que servem como a camada de dados brutos do projeto.

# 3.2. Modelagem e Transformação com dbt
A etapa de transformação foi inteiramente construída com dbt, garantindo que as transformações sejam versionadas, testáveis e documentadas.

- stg_mortalidades & stg_nascimentos_vivos: Padronizam os nomes das colunas e removem dados inconsistentes, como as linhas de totalização ("Total") e os municípios não identificados ("IGNORADO").

- dim_localidade: Cria uma tabela de dimensão que serve como uma fonte única de verdade para os municípios, com uma chave única (id_localidade).

- fat_mortalidades & fat_nascimentos_vivos: Agregam os dados por localidade e ano, criando as tabelas de fato finais prontas para análise.

# 3.3. Qualidade de Dados (Data Quality)
Para garantir a integridade dos dados, foram implementados 6 testes de qualidade no arquivo schema.yml:

- not_null: Garante que as chaves não tenham valores nulos.

- unique: Assegura que as chaves primárias e as chaves compostas sejam únicas.

- relationships: Confirma a integridade referencial entre as tabelas de fato e dimensão.

# 3.4. Orquestração e Automação com Snowflake Tasks
A pipeline de dados pode ser automatizada utilizando o recurso Tasks do Snowflake. O fluxo seria orquestrado da seguinte forma:

- Task 1 (Ingestão): Responsável por carregar novos dados brutos diariamente.

- Task 2 (Transformação): Executa dbt run logo após a Task 1 ser concluída, garantindo que os dados transformados estejam sempre atualizados.

- Task 3 (Validação): Executa dbt test após a Task 2, validando a integridade dos dados antes de disponibilizá-los para a camada de visualização.

# 3.5. Visualização e Insights com Streamlit
Um dashboard interativo foi desenvolvido com o Streamlit para consumir as tabelas de fato (fat) e dimensão (dim), permitindo a visualização dos dados de nascimentos e mortalidades por município.

# 4. Recursos Avançados do Snowflake
Para garantir a segurança, agilidade e eficiência da solução, foram considerados os seguintes recursos do Snowflake:

Time Travel: Permite consultar dados de um ponto específico no tempo, facilitando a recuperação de dados em caso de erros ou a verificação de histórico sem a necessidade de backups. O recurso pode ser usado para consultar uma tabela como ela estava há 1 hora, por exemplo, com um comando SELECT ... AT(OFFSET => -3600).

Zero-Copy Cloning: Cria uma cópia completa de um banco de dados, schema ou tabela de forma instantânea e sem custo de armazenamento adicional. Isso é ideal para criar ambientes de teste, desenvolvimento ou de segurança rapidamente, usando um comando como CREATE DATABASE ... CLONE ....

# 5. Como Executar o Projeto

- Clone o repositório.

- Configure a sua conexão com o Snowflake no arquivo profiles.yml do dbt.

- Execute dbt deps para instalar as dependências.

- Execute dbt run para criar todas as tabelas e views.

- Execute dbt test para validar a qualidade dos dados.

- Para visualizar a documentação do dbt, use dbt docs generate e depois dbt docs serve.

- Para rodar o dashboard, configure o arquivo .streamlit/secrets.toml e execute streamlit run app.py.

# 6. Link para a Documentação Interativa
https://datasus-dbt-analytics.streamlit.app/
