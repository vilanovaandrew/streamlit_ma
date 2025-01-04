import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from mplsoccer import Pitch, VerticalPitch

st.title ("Mapa de chutes")
st.subheader("Filtra clubes")

data = pd.read_csv('J:/Projetos/BD/events.csv')

pitch = Pitch(pitch_type='wyscout', axis=False, label=False, half=True, corner_arcs=True,pitch_color='grass', line_color='white',
              stripe=False)
fig, ax = pitch.draw()

# Assumindo que as colunas são 'X' e 'Y' no seu arquivo CSV
x_data = data['X']
y_data = data['Y']


# Plotar os dados X e Y no campo de futebol
ax.scatter(x_data, y_data, color='blue')

st.pyplot(fig)