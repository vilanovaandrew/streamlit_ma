import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from matplotlib.patheffects import withStroke
import numpy as np



st.title ("Mapa de Assistências")

data = pd.read_csv('EventAssistencia.csv')

# Criar os filtros com 'None' ou valores vazios como padrão
time_filter = st.selectbox("Selecione o Time", ['Todos'] + sorted(list(data['Team'].unique())))

# Filtro de jogador - baseado nos jogadores disponíveis após a seleção de 'Time' e 'Modo do Gol'
filtered_players = data.copy()

if time_filter != 'Todos':
    filtered_players = filtered_players[filtered_players['Team'] == time_filter]

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
if player_filter.strip() != "":
    filtered_data = filtered_data[filtered_data['Player'].str.contains(player_filter, case=False, na=False)]

# Set up the pitch
pitch = Pitch(pitch_type='wyscout', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw( constrained_layout=True, tight_layout=False)
fig.set_facecolor('#22312b')

# Plot the completed passes
pitch.arrows(filtered_data['X'], filtered_data['Y'],
             filtered_data['X2'], filtered_data['Y2'], width=1,
             headwidth=6, headlength=6, color='#48D1CC', ax=ax)

# Plot circulo no inicio da jogada
ax.scatter(filtered_data['X'], filtered_data['Y'], color='#FFFAFA', s=10, zorder=5)  # Adiciona o ponto da bola

st.pyplot(fig)

# Ranking de jogadores
st.subheader("Liderança de Assistências")

# Calcular a contagem de Assistências por jogador
player_counts = filtered_data['Player'].value_counts()

# Criar a tabela de ranking com os top jogadores
ranking_table = player_counts.reset_index()
ranking_table.columns = ['Jogador', 'Assistências']

# Ordenar pela quantidade de Assistências (decrescente) e pelo nome do jogador (crescente)
ranking_table = ranking_table.sort_values(by=['Assistências', 'Jogador'], ascending=[False, True]).reset_index(drop=True)

# Exibir a tabela abaixo dos gráficos, com índice começando em 1
st.dataframe(ranking_table, use_container_width=True)