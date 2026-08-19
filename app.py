import subprocess
import streamlit as st
from pathlib import Path
import random
import pandas as pd


MUSIC_DIR = Path(__file__).resolve().parent / "musicas"

musicas = list(MUSIC_DIR.glob("*.opus"))
nome_musicas = [i.stem for i in musicas]

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


def musica_atual(musicas: list[Path], idx: int):
    return musicas[idx % len(musicas)]


def divisao(a, b):
    if b == 0:
        return 0

    return a / b


DIFICULDADES = {
    "fácil": (10, "próxima"),
    "normal": (5, "fácil"),
    "difícil": (3, "normal"),
    "impossível": (1, "difícil")
}


# =========================
# INICIALIZAÇÃO
# =========================

if "musicas" not in st.session_state:

    st.session_state.musicas = musicas.copy()
    random.shuffle(st.session_state.musicas)

    st.session_state.musica_idx = 0

    st.session_state.dificuldade = "impossível"

    st.session_state.resultado = None

    st.session_state.estatisticas = {
        musica.stem: {
            "acertos": 0,
            "pontos": 0,
            "tentativas": 0
        }
        for musica in musicas
    }

abas = st.tabs(['Quiz', 'Estatísticas'])

# =========================
# QUIZ NORMAL
# =========================

with abas[0]:

    st.header("Quiz")

    musica = musica_atual(
        st.session_state.musicas,
        st.session_state.musica_idx
    )

    dificuldade = (
        st.session_state.dificuldade,
    ) + DIFICULDADES[st.session_state.dificuldade]

    random.shuffle(nome_musicas)

    st.write(f"{dificuldade[0].capitalize()}:")

    st.audio(
        musica_cortada(musica, dificuldade[1]),
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

        stats = st.session_state.estatisticas[musica.stem]

        stats["tentativas"] += 1

        if musica.stem == guess:

            stats["acertos"] += 1

            st.session_state.resultado = (
                "success",
                "Você acertou!"
            )

            st.session_state.musica_idx += 1
            st.session_state.dificuldade = "impossível"

        else:

            if dificuldade[2] == "próxima":

                st.session_state.resultado = (
                    "error",
                    f"Você errou! Era {musica.stem}"
                )

                st.session_state.musica_idx += 1
                st.session_state.dificuldade = "impossível"

            else:

                st.session_state.resultado = (
                    "error",
                    "Você errou! Tente novamente"
                )

                st.session_state.dificuldade = dificuldade[2]

        st.rerun()


# =========================
# ESTATÍSTICAS
# =========================

with abas[1]:

    st.header("Estatísticas")

    df = pd.DataFrame([
        {
            "Música": nome,
            "Acertos": divisao(
                stats["acertos"],
                stats["tentativas"]
            ) * 100
        }
        for nome, stats
        in st.session_state.estatisticas.items()
    ])

    st.bar_chart(
        df,
        x="Música",
        y="Acertos"
    )