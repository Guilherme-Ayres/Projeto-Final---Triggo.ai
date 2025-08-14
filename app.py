import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

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

col1, col2 = st.columns(2)
col1.metric("💀 Total Mortalidades", f"{total_mortes:,}".replace(",", "."))
col2.metric("👶 Total Nascimentos", f"{total_nascimentos:,}".replace(",", "."))

st.header('📊 Top 10 Municípios em Mortalidade')
top_mortes = df_sem_total.sort_values("TOTAL_MORTALIDADES_2023", ascending=False).head(10)
fig1 = px.bar(
    top_mortes,
    x="MUNICIPIO_NOME",
    y="TOTAL_MORTALIDADES_2023",
    title="Top 10 Municípios com Maior Mortalidade",
    text="TOTAL_MORTALIDADES_2023"
)
fig1.update_traces(texttemplate='%{text:,}', textposition='outside')
fig1.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig1, use_container_width=True)

st.header('📊 Top 10 Municípios em Nascimentos')
top_nasc = df_sem_total.sort_values("TOTAL_NASCIMENTOS_2023", ascending=False).head(10)
fig2 = px.bar(
    top_nasc,
    x="MUNICIPIO_NOME",
    y="TOTAL_NASCIMENTOS_2023",
    title="Top 10 Municípios com Maior Natalidade",
    text="TOTAL_NASCIMENTOS_2023"
)
fig2.update_traces(texttemplate='%{text:,}', textposition='outside')
fig2.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig2, use_container_width=True)

st.subheader('📄 Dados Completos')
st.dataframe(df)

conn.close()
