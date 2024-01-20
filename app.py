# Desenvolvido por Levi Lucena - https://www.linkedin.com/in/levilucena/
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Função para gerar dados fictícios
def generate_fake_data(num_rows=1000):
    np.random.seed(42)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    date_generated = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days)]

    data = {
        "Date": np.random.choice(date_generated, size=num_rows),
        "Product line": np.random.choice(["Electronic accessories", "Fashion accessories", "Food and beverages", "Health and beauty", "Home and lifestyle", "Sports and travel"], size=num_rows),
        "City": np.random.choice(["City A", "City B", "City C"], size=num_rows),
        "Total": np.random.uniform(100, 2000, size=num_rows),
        "Payment": np.random.choice(["Credit card", "Ewallet", "Cash"], size=num_rows),
        "Rating": np.random.uniform(3, 5, size=num_rows)
    }

    return pd.DataFrame(data)

# Criando dados fictícios
df_fake = generate_fake_data()

# Adicione a logo
st.sidebar.image("logo.png", use_column_width=True)

# Criando um aplicativo Streamlit
st.title('Análise de Desempenho de Vendas')

# Substituindo os valores pelos dados fictícios
df = df_fake
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Esta parte será usada para os Filtros
df["Month"] = df["Date"].dt.strftime("%Y-%m")
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)
col10, col11, col12 = st.columns(3)

# Gráfico de barras empilhadas por tipo de produto e cidade
fig_stacked_bar = px.bar(df_filtered, x="Date", y="Total", color="Product line", facet_col="City", category_orders={"Product line": ["Electronic accessories", "Fashion accessories", "Food and beverages", "Health and beauty", "Home and lifestyle", "Sports and travel"]}, title="Faturamento por tipo de produto e cidade")
col1.plotly_chart(fig_stacked_bar, use_container_width=True)

# Gráfico de linha para mostrar o total acumulado por dia
df_filtered["Cumulative Total"] = df_filtered.groupby("City")["Total"].cumsum()
fig_cumulative = px.line(df_filtered, x="Date", y="Cumulative Total", color="City", title="Total acumulado por dia")
col2.plotly_chart(fig_cumulative, use_container_width=True)

# Gráfico de barras para mostrar a contribuição percentual por tipo de pagamento
payment_contribution = df_filtered.groupby("Payment")["Total"].sum() / df_filtered["Total"].sum() * 100
fig_payment_contribution = px.bar(payment_contribution, x=payment_contribution.index, y=payment_contribution.values, labels={"y": "Contribuição (%)"}, title="Contribuição por tipo de pagamento")
col3.plotly_chart(fig_payment_contribution, use_container_width=True)

# Gráfico de pizza para mostrar a distribuição de produtos
fig_product_distribution = px.pie(df_filtered, names="Product line", title="Distribuição de produtos")
col4.plotly_chart(fig_product_distribution, use_container_width=True)

# Box plot para mostrar a distribuição das avaliações por cidade
fig_rating_box = px.box(df_filtered, x="City", y="Rating", title="Distribuição das avaliações por cidade")
col5.plotly_chart(fig_rating_box, use_container_width=True)

# Histograma para mostrar a distribuição dos valores totais
fig_total_distribution = px.histogram(df_filtered, x="Total", nbins=20, title="Distribuição dos valores totais")
col6.plotly_chart(fig_total_distribution, use_container_width=True)

# Scatter plot para mostrar a relação entre o total e a avaliação
fig_scatter_rating = px.scatter(df_filtered, x="Total", y="Rating", color="City", title="Relação entre Total e Avaliação")
col7.plotly_chart(fig_scatter_rating, use_container_width=True)

# Gráfico de barras horizontais para mostrar a média de avaliação por tipo de produto
fig_avg_rating_product = px.bar(df_filtered, x="Rating", y="Product line", orientation="h", title="Média de Avaliação por Tipo de Produto")
col8.plotly_chart(fig_avg_rating_product, use_container_width=True)

# Gráfico de linha para mostrar a tendência do faturamento ao longo do tempo
fig_trend_over_time = px.line(df_filtered, x="Date", y="Total", color="City", title="Tendência do Faturamento ao Longo do Tempo")
col9.plotly_chart(fig_trend_over_time, use_container_width=True)

# Gráfico de barras para mostrar o faturamento por tipo de produto e cidade
fig_faturamento_produto_cidade = px.bar(df_filtered, x="Product line", y="Total", color="City", title="Faturamento por Tipo de Produto e Cidade")
col10.plotly_chart(fig_faturamento_produto_cidade, use_container_width=True)

# Gráfico de pizza para mostrar a distribuição de filiais
fig_distribuicao_filiais = px.pie(df_filtered, names="City", title="Distribuição de Filiais")
col11.plotly_chart(fig_distribuicao_filiais, use_container_width=True)

# Gráfico de dispersão para mostrar a relação entre faturamento e avaliação por tipo de produto
fig_relacao_faturamento_avaliacao = px.scatter(df_filtered, x="Total", y="Rating", color="Product line", title="Relação entre Faturamento e Avaliação por Tipo de Produto")
col12.plotly_chart(fig_relacao_faturamento_avaliacao, use_container_width=True)

# Adicione o rodapé com a imagem
st.image("rodape.png", use_column_width=True)