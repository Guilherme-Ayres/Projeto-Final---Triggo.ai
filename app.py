import streamlit as st
import snowflake.connector
import pandas as pd


st.title('Análise de Nascimentos e Mortalidades no Brasil - 2023')


conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
)


@st.cache_data(ttl=600)
def get_data():
    query = """
    SELECT
        m.municipio_nome,
        m.total_mortalidades_2023,
        n.total_nascimentos_2023
    FROM
        fat_mortalidades AS m
    JOIN
        fat_nascimentos_vivos AS n ON m.id_localidade = n.id_localidade
    ORDER BY
        m.total_mortalidades_2023 DESC
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
    return df


df = get_data()


st.header('Top 10 Municípios em Mortalidade')


st.bar_chart(df.head(10), x='MUNICIPIO_NOME', y='TOTAL_MORTALIDADES_2023')

st.header('Top 10 Municípios em Nascimentos')


st.bar_chart(df.head(10), x='MUNICIPIO_NOME', y='TOTAL_NASCIMENTOS_2023')


st.subheader('Dados Completos')
st.dataframe(df)


conn.close()
