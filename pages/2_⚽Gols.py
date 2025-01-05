import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from matplotlib.patheffects import withStroke
import numpy as np

st.title("Mapa de gols")

data = pd.read_csv('EventGols.csv')

# Criar os filtros com 'None' ou valores vazios como padrão
time_filter = st.selectbox("Selecione o Time", ['Todos'] + sorted(list(data['Team'].unique())))
modo_do_gol_filter = st.selectbox("Selecione o Modo do Gol", ['Todos'] + sorted(list(data['Event'].unique())))

# Filtro de jogador - baseado nos jogadores disponíveis após a seleção de 'Time' e 'Modo do Gol'
filtered_players = data.copy()

if time_filter != 'Todos':
    filtered_players = filtered_players[filtered_players['Team'] == time_filter]
if modo_do_gol_filter != 'Todos':
    filtered_players = filtered_players[filtered_players['Event'] == modo_do_gol_filter]

# Lista de jogadores disponíveis
player_options = list(filtered_players['Player'].unique())

# Campo de digitação para o filtro de jogador
player_filter = st.text_input(
    "Digite o nome do Jogador",
    value="",
    placeholder="Comece a digitar o nome do jogador..."
)

# Aplicar filtro de jogador somente se algo for digitado
filtered_data = data.copy()

if time_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Team'] == time_filter]
if modo_do_gol_filter != 'Todos':
    filtered_data = filtered_data[filtered_data['Event'] == modo_do_gol_filter]
if player_filter.strip() != "":
    filtered_data = filtered_data[filtered_data['Player'].str.contains(player_filter, case=False, na=False)]

# Criar o layout com colunas
col1, col2 = st.columns(2)

# Instanciar o Pitch
pitch = Pitch(pitch_type='wyscout', half=False, pitch_color='#22312b', line_color='#c7d5cc')

# Gráfico 1
with col1:
    fig1, ax1 = pitch.draw()
    x_data1 = filtered_data['X']  # Usar dados filtrados
    y_data1 = filtered_data['Y']  # Usar dados filtrados
    ax1.scatter(x_data1, y_data1, color='#90EE90')
    st.pyplot(fig1)

# Gráfico 2
with col2:
    pitch = Pitch(pitch_type='wyscout', line_zorder=2, pitch_color='#f4edf0', half=False)
    fig, ax = pitch.draw()
    fig.set_facecolor('#f4edf0')
    
    # Gerar o heatmap
    bin_statistic = pitch.bin_statistic(filtered_data['X'], filtered_data['Y'], statistic='count', bins=(6, 5), normalize=True)
    pitch.heatmap(bin_statistic, ax=ax, cmap='Reds', edgecolor='gray')
    
    # Efeitos de texto para os rótulos do heatmap
    path_eff = [withStroke(linewidth=3, foreground="black")]
    labels = pitch.label_heatmap(bin_statistic, color='#f4edf0', fontsize=10, ax=ax, ha='center', va='center', str_format='{:.0%}', path_effects=path_eff)
    st.pyplot(fig)

# Ranking de jogadores
st.subheader("Artilharia")

# Calcular a contagem de gols por jogador
player_counts = filtered_data['Player'].value_counts()

# Criar a tabela de ranking com os top jogadores
ranking_table = player_counts.reset_index()
ranking_table.columns = ['Jogador', 'Gols']

# Ordenar pela quantidade de Gols (decrescente) e pelo nome do jogador (crescente)
ranking_table = ranking_table.sort_values(by=['Gols', 'Jogador'], ascending=[False, True]).reset_index(drop=True)

# Exibir a tabela abaixo dos gráficos, com índice começando em 1
st.dataframe(ranking_table, use_container_width=True)