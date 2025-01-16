import requests
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

# Configurações do Bot
TELEGRAM_TOKEN = "7579283306:AAGUBweTxfa3_52ovHtaW4xHgS-6rZFB9eU"  # Substitua pelo seu Token
CHAT_ID = "-1002368608523"  # Substitua pelo seu Chat ID

# Função para enviar mensagem ao Telegram
def enviar_telegram(mensagem, nome=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    if nome:
        mensagem = f"{nome} diz:\n\n{mensagem}"
    else:
        mensagem = f"Anônimo diz:\n\n{mensagem}"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        st.error(f"Erro: {response.status_code} - {response.text}")
    return response.status_code == 200

# Interface no Streamlit
st.subheader("Envie sua mensagem/sugestão")

with st.form(key="form_mensagem"):
    nome = st.text_input("Seu nome (ou anônimo):")
    mensagem = st.text_area("Sua mensagem/sugestão:")
    enviar = st.form_submit_button("Enviar")
    if enviar:
        if mensagem.strip():  # Verifica se a mensagem não está vazia
            sucesso = enviar_telegram(mensagem, nome if nome.strip() else None)
            if sucesso:
                st.success("Mensagem enviada com sucesso!")
            else:
                st.error("Falha ao enviar a mensagem.")
        else:
            st.warning("Por favor, escreva uma mensagem antes de enviar.")

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