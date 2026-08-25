import streamlit as st
from pathlib import Path
import random

MUSIC_DIR = Path(__file__).resolve().parent.parent / "musicas" / "Sabrina"

musicas = list(MUSIC_DIR.glob("*.opus"))
nome_musicas = [i.stem for i in musicas]
    
def musica_atual(musicas: list[Path], idx: int):
    return musicas[idx % len(musicas)]

if "inf_musicas" not in st.session_state:
    st.session_state.inf_musicas = musicas.copy()
    random.shuffle(st.session_state.inf_musicas)
    st.session_state.musica_idx = 0
    st.session_state.resultado = None

st.header("Quiz Infinito")

musica = musica_atual(
    st.session_state.inf_musicas,
    st.session_state.musica_idx
)

random.shuffle(nome_musicas)

st.audio(
    musica,
    autoplay=True
)

guess = st.selectbox(
    "Selecionar",
    nome_musicas,
    key="quiz_guess"
)

if st.session_state.resultado:
    tipo, mensagem = st.session_state.resultado
    if tipo == "info":
        st.info(mensagem)
    elif tipo == "success":
        st.success(mensagem)
    elif tipo == "error":
        st.error(mensagem)

if st.button("Adivinhar"):
    if musica.stem == guess:
        st.session_state.resultado = (
            "success",
            "Você acertou!"
        )
        st.session_state.musica_idx += 1

    else:
        st.session_state.resultado = (
            "error",
            "Você errou! Tente novamente"
        )

    st.rerun()