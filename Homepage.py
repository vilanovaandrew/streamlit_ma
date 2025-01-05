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

st.title("Local das estatísticas do campeonato Maranhense 2025")
st.sidebar.success("Seleciona páginas acima.")