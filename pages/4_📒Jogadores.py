import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from matplotlib.patheffects import withStroke
import numpy as np

# Carregar os dados do Excel
data = pd.read_excel('BDcampeonatomaranhense2025.xlsx', 'Escalacao')

st.title("Estatísticas de Participações dos Jogadores")

# Contar partidas (coluna CBF)
data['Partidas'] = data.groupby('CBF')['CBF'].transform('count')

# Agrupar dados por jogador único
aggregated_data = (
    data.groupby('CBF', as_index=False)
    .agg({
        'Jogador': 'first', 
        'Time': 'first',
        'Tempo Jogado': 'sum',
        'Partidas': 'first',
    })
)

# Calcular o tempo médio por partida
aggregated_data['Tempo Médio por Partida'] = aggregated_data['Tempo Jogado'] / aggregated_data['Partidas']

# Ordenar pelo tempo jogado
aggregated_data = aggregated_data.sort_values(by='Tempo Jogado', ascending=False, ignore_index=True)

# Criar o primeiro gráfico
fig1, ax1 = plt.subplots(figsize=(10, 6))
agg_players_count = aggregated_data.groupby('Time')['CBF'].nunique().sort_index()  # Ordenado em ordem alfabética
ax1.barh(agg_players_count.index, agg_players_count.values, color='darkblue')
ax1.set_title('Jogadores Relacionados')

# Adicionar rótulos na extremidade interna das barras
for i, v in enumerate(agg_players_count.values):
    ax1.text(v, i, str(v), color='white', ha='right', va='center',fontweight='bold')

# Criar o segundo gráfico
fig2, ax2 = plt.subplots(figsize=(10, 6))
agg_used_players = aggregated_data[aggregated_data['Tempo Jogado'] > 1].groupby('Time')['CBF'].nunique().sort_index()  # Ordenado em ordem alfabética
ax2.barh(agg_used_players.index, agg_used_players.values, color='darkblue')
ax2.set_title('Jogadores Utilizados')

# Adicionar rótulos na extremidade interna das barras
for i, v in enumerate(agg_used_players.values):
    ax2.text(v, i, str(v), color='white', ha='right', va='center',fontweight='bold')

# Exibir os gráficos lado a lado
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)


# Exibir a tabela após o filtro
st.subheader("Detalhamento dos dados")

# Aplicar filtros após os gráficos
time_filter = st.selectbox("Selecione o Time", ['Todos'] + sorted(list(data['Time'].unique())))
confronto_filter = st.selectbox("Selecione o Confronto", ['Todos'] + sorted(list(data['Confronto'].unique())))

player_filter = st.text_input(
    "Digite o nome do Jogador",
    value="",
    placeholder="Comece a digitar o nome do jogador..."
)

# Aplicar filtros no DataFrame original
filtered_data = data.copy()
if time_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Time'] == time_filter]
if confronto_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Confronto'] == confronto_filter]
if player_filter.strip() != "":
    filtered_data = filtered_data[filtered_data['Jogador'].str.contains(player_filter, case=False, na=False)]

# Contar partidas (ocorrências de cada CBF)
filtered_data['Partidas'] = filtered_data.groupby('CBF')['CBF'].transform('count')

# Consolidar dados por jogador único com base na coluna 'CBF'
aggregated_filtered_data = (
    filtered_data.groupby('CBF', as_index=False)
    .agg({
        'Jogador': 'first',          # Primeiro valor do nome do jogador
        'Time': 'first',             # Primeiro valor do time
        'Tempo Jogado': 'sum',       # Soma do tempo jogado
        'Partidas': 'first',         # Contagem de partidas
    })
)

# Calcular o tempo médio jogado por partida
aggregated_filtered_data['Tempo Médio por Partida'] = aggregated_filtered_data['Tempo Jogado'] / aggregated_filtered_data['Partidas']

# Ordenar o DataFrame pelo tempo jogado em ordem decrescente
if not aggregated_filtered_data.empty:
    aggregated_filtered_data = aggregated_filtered_data.sort_values(by='Tempo Jogado', ascending=False, ignore_index=True)

# Exibir a tabela abaixo dos gráficos, com índice começando em 1
if not aggregated_filtered_data.empty:
    st.dataframe(aggregated_filtered_data, use_container_width=True)
