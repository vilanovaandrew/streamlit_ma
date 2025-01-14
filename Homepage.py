import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from mplsoccer import Pitch, VerticalPitch

st.set_page_config(
    page_title="Campeonato Maranhense Estatísticas",
    page_icon="📊",
)

st.title("Local das estatísticas do Campeonato Maranhense 2025")

st.markdown("Expanda a barra lateral esquerda para visualizar e acessar todas as categorias disponíveis.")

st.sidebar.success("Categorias")



# Criando 8 colunas
cols = st.columns(8)

# Ajustando o tamanho de todas as imagens para serem do mesmo tamanho
image_size = 50  # Ajuste conforme necessário

cols[0].image("Iape.png", width=image_size)
cols[1].image("Imperatriz.png", width=image_size)
cols[2].image("Maranhao.png", width=image_size)
cols[3].image("Moto.png", width=image_size)
cols[4].image("Pinheiro.png", width=image_size)
cols[5].image("Sampaio.png", width=image_size)
cols[6].image("Tuntum.png", width=image_size)
cols[7].image("Viana.png", width=image_size)