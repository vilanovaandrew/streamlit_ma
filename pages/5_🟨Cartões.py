import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
import numpy as np

st.title("Análise de Cartões")

# Carregar os dados do Excel
data = pd.read_excel('BDcampeonatomaranhense2025.xlsx', 'Cartoes')

# Consolidar dados por jogador único com base na coluna 'CBF'
aggregated_data = (
    data.groupby('CBF', as_index=False)
    .agg({
        'Jogador': 'first',          # Primeiro valor do nome do jogador
        'Time': 'first',             # Primeiro valor do time
        'Amarelo': 'sum',            # Soma dos cartões amarelos
        'Vermelho': 'sum'            # Soma dos cartões vermelhos
    })
)

# Renomear as colunas para melhor entendimento (opcional)
aggregated_data.rename(columns={
    'Amarelo': 'Total Amarelos',
    'Vermelho': 'Total Vermelhos'
}, inplace=True)

# Criar gráficos separados para cartões amarelos e vermelhos
if not data.empty:
    time_data = (
        data.groupby('Time', as_index=False)
        .agg({
            'Amarelo': 'sum',
            'Vermelho': 'sum'
        })
        .rename(columns={'Amarelo': 'Total Amarelos', 'Vermelho': 'Total Vermelhos'})
    )

    # Criar subplots lado a lado
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    # Gráfico de cartões amarelos
    ax1.bar(time_data['Time'], time_data['Total Amarelos'], color='gold', edgecolor='black')
    ax1.set_title('Cartões Amarelos por Time', fontsize=14)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Quantidade de Cartões', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    for i, v in enumerate(time_data['Total Amarelos']):
        ax1.text(i, v, str(v), ha='center', va='bottom', fontsize=10)

    # Gráfico de cartões vermelhos
    ax2.bar(time_data['Time'], time_data['Total Vermelhos'], color='red', edgecolor='black')
    ax2.set_title('Cartões Vermelhos por Time', fontsize=14)
    ax2.set_xlabel('Time', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    for i, v in enumerate(time_data['Total Vermelhos']):
        ax2.text(i, v, str(v), ha='center', va='bottom', fontsize=10)

    # Ajustar espaçamento
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

st.subheader("Jogadores advertidos")

# Exibir o filtro após os gráficos
time_filter = st.selectbox("Selecione o Time", ['Todos'] + sorted(list(data['Time'].unique())))

# Aplicar o filtro ao DataFrame original
filtered_data = data if time_filter == 'Todos' else data[data['Time'] == time_filter]

# Atualizar dados consolidados com base no filtro
filtered_aggregated_data = (
    filtered_data.groupby('CBF', as_index=False)
    .agg({
        'Jogador': 'first',
        'Time': 'first',
        'Amarelo': 'sum',
        'Vermelho': 'sum'
    })
    .rename(columns={
        'Amarelo': 'Cartões Amarelos',
        'Vermelho': 'Cartões Vermelhos'
    })
)

# Adicionar a nova coluna 'Total Cartões' que é a soma das colunas 'Cartões Amarelos' e 'Cartões Vermelhos'
filtered_aggregated_data['Total Cartões'] = filtered_aggregated_data['Cartões Amarelos'] + filtered_aggregated_data['Cartões Vermelhos']

# Ordenar os dados pela coluna 'Total Cartões' de forma decrescente e, em caso de empate, por 'Jogador' em ordem alfabética
filtered_aggregated_data = filtered_aggregated_data.sort_values(by=['Total Cartões', 'Jogador'], ascending=[False, True])

# Resetar o índice para ordenar conforme 'Total Cartões' e 'Jogador' e renomear a coluna de índice para "Posição"
filtered_aggregated_data = filtered_aggregated_data.reset_index(drop=True)

# Ajustar o índice para começar de 1 e renomeá-lo como 'Posição'
filtered_aggregated_data.index = filtered_aggregated_data.index + 1
filtered_aggregated_data.index.name = 'Posição'

# Exibir a tabela após a ordenação
if not filtered_aggregated_data.empty:
    st.dataframe(filtered_aggregated_data, use_container_width=True)
else:
    st.write("Não há dados disponíveis para os filtros selecionados.")