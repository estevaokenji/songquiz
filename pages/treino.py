import streamlit as st
import subprocess
from pathlib import Path
import random

MUSIC_DIR = Path(__file__).resolve().parent.parent / "musicas"

musicas = list(MUSIC_DIR.glob("*.opus"))

def musica_cortada(musica: Path, tempo: float):
    return subprocess.run(
        [
            "ffmpeg",
            "-i", str(musica),
            "-t", str(tempo),
            "-f", "mp3",
            "pipe:1"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).stdout

if "treino" not in st.session_state:

    st.session_state.treino = {
        "musicas": [],
        "idx": 0,
        "acertos": 0,
        "resultado": None
    }

st.title("Sabrina Quiz")

st.header("Treino")

treino = st.session_state.treino

if not treino["musicas"]:

    treino["musicas"] = random.sample(
        musicas,
        min(5, len(musicas))
    )

    treino["idx"] = 0
    treino["acertos"] = 0
    treino["resultado"] = None


musica_treino = treino["musicas"][treino["idx"]]
nome_musicas = [i.stem for i in treino["musicas"]]
random.shuffle(nome_musicas)

st.write(
    f"Progresso: {treino['acertos']}/5"
)

st.progress(
    treino["acertos"] / 5
)

st.audio(
    musica_cortada(musica_treino, 5),
    format="audio/mp3",
    autoplay=True
)


guess_treino = st.selectbox(
    "Qual é a música?",
    nome_musicas,
    key=f"treino_guess_{treino['idx']}_{treino['acertos']}"
)


if treino["resultado"]:

    tipo, mensagem = treino["resultado"]

    if tipo == "success":
        st.success(mensagem)

    elif tipo == "error":
        st.error(mensagem)

    elif tipo == "info":
        st.info(mensagem)


if st.button("Responder", key="treino_responder"):

    if musica_treino.stem == guess_treino:

        treino["acertos"] += 1

        treino["resultado"] = (
            "success",
            "Você acertou!"
        )

        # Terminou as 5
        if treino["acertos"] >= 5:

            treino["resultado"] = (
                "success",
                "Você acertou as 5 músicas! Próximo grupo!"
            )

            treino["musicas"] = []
            treino["idx"] = 0
            treino["acertos"] = 0

    else:

        treino["resultado"] = (
            "error",
            f"Você errou! Era **{musica_treino.stem}**."
        )

        # Errou → volta para a primeira música
        treino["musicas"] = random.sample(treino["musicas"], len(treino["musicas"]))
        treino["idx"] = 0
        treino["acertos"] = 0

    # Se acertou e ainda não terminou as 5
    if treino["resultado"][0] == "success" and treino["musicas"]:

        treino["idx"] += 1

    st.rerun()