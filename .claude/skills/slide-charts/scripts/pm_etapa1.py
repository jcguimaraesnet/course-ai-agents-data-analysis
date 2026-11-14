"""Gráficos da etapa 1 de Modelagem Preditiva: underfitting e overfitting pela força da regularização.

Mesma divisão, mesmas colunas e mesmo modelo do slide e do live coding da etapa 1: as três colunas
numéricas sem ausentes, 80% para treino e 20% para teste, random_state=42 (sem estratificar: a
estratificação é da etapa 2), e a regressão logística com termos polinomiais de grau 8.
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from tema import AZUL, LARANJA, MUDA, TINTA_2, grafico, virgula

NUMERICAS = ["idade", "viagens_30d", "distancia_media_km"]
GRADE_C = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]


def modelo(C):
    """O pipeline do slide: escala, termos polinomiais de grau 8, escala de novo e regressão logística."""
    return make_pipeline(StandardScaler(), PolynomialFeatures(8), StandardScaler(),
                         LogisticRegression(C=C, max_iter=5000))


def rotulo_c(c):
    """0.0001 -> '0,0001'; 10000 -> '10.000'."""
    if c >= 1:
        return f"{c:,.0f}".replace(",", ".")
    return f"{c:.4f}".rstrip("0").replace(".", ",")


@grafico("pm-complexidade-c.png")
def complexidade_c(base):
    X_tr, X_te, y_tr, y_te = train_test_split(base[NUMERICAS], base["virou_assinante"],
                                              test_size=0.2, random_state=42)
    treino, teste = [], []
    for C in GRADE_C:
        m = modelo(C).fit(X_tr, y_tr)
        treino.append(m.score(X_tr, y_tr))
        teste.append(m.score(X_te, y_te))
    referencia = max(y_te.mean(), 1 - y_te.mean())
    x = np.arange(len(GRADE_C))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(referencia, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(len(GRADE_C) - 1, referencia - 0.004, f"sempre \"não vira\": {virgula(referencia)}",
            color=MUDA, fontsize=10, ha="right", va="top")
    ax.plot(x, treino, color=AZUL, marker="o", markersize=5, label="treino")
    ax.plot(x, teste, color=LARANJA, marker="o", markersize=5, label="teste")
    ax.text(0.15, 0.703, "underfitting", color=TINTA_2, fontsize=11)
    ax.text(len(GRADE_C) - 1, 0.825, "overfitting", color=TINTA_2, fontsize=11, ha="right")
    ax.set_xticks(x[::2], [rotulo_c(c) for c in GRADE_C[::2]])
    ax.set_ylim(0.70, 0.84)
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v))
    ax.set_xlabel("C (menor = mais regularização)")
    ax.set_ylabel("acurácia")
    ax.legend(loc="upper left")
    return fig
