"""Gráficos da etapa 7: a reta de regressão da duração pela distância e a avaliação no teste.

A divisão em treino e teste é a mesma dos slides e do live coding: 80% e 20%, random_state=42.
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

from dados import com_duracao
from tema import AZUL, LARANJA, MUDA, SUPERFICIE, TINTA, TINTA_2, grafico, virgula


def reta(base):
    """Coeficientes de mínimos quadrados na base toda: b = cov / var e a = ȳ − b·x̄."""
    reg = com_duracao(base)
    x, y = reg["distancia_km"], reg["duracao_min"]
    b = x.cov(y) / x.var()
    return y.mean() - b * x.mean(), b


def treino_teste(base):
    """A divisão dos slides: 80% para treino e 20% para teste, com random_state=42."""
    reg = com_duracao(base)
    return train_test_split(reg[["distancia_km"]], reg["duracao_min"], test_size=0.2, random_state=42)


@grafico("eda-reta-duracao.png")
def reta_duracao(base):
    reg = com_duracao(base)
    a, b = reta(base)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(reg["distancia_km"], reg["duracao_min"], s=10, color=AZUL, alpha=0.35, linewidths=0)
    xs = np.array([0, 12.3])
    ax.plot(xs, a + b * xs, color=LARANJA, linewidth=2.5)
    ax.text(0.5, 71, f"duração = {virgula(a)} + {virgula(b)} × distância", color=TINTA, fontsize=11)
    ax.grid(True, axis="both")
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 80)
    ax.set_xlabel("distância (km)")
    ax.set_ylabel("duração (min)")
    return fig


@grafico("eda-minimos-quadrados.png")
def minimos_quadrados(base):
    reg = com_duracao(base)
    a, b = reta(base)
    amostra = reg[reg["distancia_km"] <= 6].sample(16, random_state=5)
    x, y = amostra["distancia_km"].to_numpy(), amostra["duracao_min"].to_numpy()
    prev = a + b * x
    fig, ax = plt.subplots(figsize=(6, 4))
    for xi, yi, pi in zip(x, y, prev):
        ax.plot([xi, xi], [yi, pi], color=MUDA, linewidth=1.3, linestyle=(0, (3, 2)))
    xs = np.array([0, 6.3])
    ax.plot(xs, a + b * xs, color=LARANJA, linewidth=2.5)
    ax.scatter(x, y, s=46, color=AZUL, edgecolors=SUPERFICIE, linewidths=1.5, zorder=3)
    i = int(np.argmax(np.abs(y - prev)))
    ax.annotate("resíduo = observado − previsto", xy=(x[i], (y[i] + prev[i]) / 2), xytext=(0.15, 25),
                color=TINTA, fontsize=11, arrowprops=dict(arrowstyle="-", color=MUDA, lw=1))
    ax.grid(True, axis="both")
    ax.set_xlim(0, 6.3)
    ax.set_xlabel("distância (km)")
    ax.set_ylabel("duração (min)")
    return fig


@grafico("eda-previsto-observado.png")
def previsto_observado(base):
    X_tr, X_te, y_tr, y_te = treino_teste(base)
    prev = LinearRegression().fit(X_tr, y_tr).predict(X_te)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(prev, y_te, s=12, color=AZUL, alpha=0.5, linewidths=0)
    ax.plot([0, 72], [0, 72], color=TINTA_2, linewidth=1.5)
    ax.text(50, 44, "previsão\nperfeita", color=TINTA_2, fontsize=11, va="top")
    ax.text(0.03, 0.96, f"teste: R² = {virgula(r2_score(y_te, prev))}\n"
                        f"RMSE = {virgula(root_mean_squared_error(y_te, prev))} min",
            transform=ax.transAxes, va="top", color=TINTA, fontsize=11)
    ax.grid(True, axis="both")
    ax.set_xlim(0, 72)
    ax.set_ylim(0, 72)
    ax.set_xlabel("duração prevista (min)")
    ax.set_ylabel("duração observada (min)")
    return fig
