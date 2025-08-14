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
    df = pd.DataFrame(data, columns=[desc[0].upper() for desc in cursor.description])
    return df

df = get_data()

df_sem_total = df[df["MUNICIPIO_NOME"].str.upper() != "TOTAL"]

total_mortes = df["TOTAL_MORTALIDADES_2023"].sum()
total_nascimentos = df["TOTAL_NASCIMENTOS_2023"].sum()
top_morte = df_sem_total.loc[df_sem_total["TOTAL_MORTALIDADES_2023"].idxmax(), "MUNICIPIO_NOME"]
top_nasc = df_sem_total.loc[df_sem_total["TOTAL_NASCIMENTOS_2023"].idxmax(), "MUNICIPIO_NOME"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("💀 Total Mortalidades", f"{total_mortes:,}".replace(",", "."))
col2.metric("👶 Total Nascimentos", f"{total_nascimentos:,}".replace(",", "."))
col3.metric("🏙️ Maior Mortalidade", top_morte)
col4.metric("🏙️ Maior Natalidade", top_nasc)

st.header('📊 Top 10 Municípios em Mortalidade')
st.bar_chart(df_sem_total.sort_values("TOTAL_MORTALIDADES_2023", ascending=False).head(10), 
             x='MUNICIPIO_NOME', y='TOTAL_MORTALIDADES_2023')

st.header('📊 Top 10 Municípios em Nascimentos')
st.bar_chart(df_sem_total.sort_values("TOTAL_NASCIMENTOS_2023", ascending=False).head(10), 
             x='MUNICIPIO_NOME', y='TOTAL_NASCIMENTOS_2023')

st.subheader('📄 Dados Completos')
st.dataframe(df)

conn.close()
