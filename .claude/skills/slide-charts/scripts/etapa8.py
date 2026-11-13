"""Gráficos da etapa 8: os resíduos do modelo da etapa 7 e a correlação entre as preditoras."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression

from dados import com_duracao
from etapa7 import treino_teste
from tema import AZUL, DIVERGENTE, LARANJA, MUDA, SUPERFICIE, TINTA, TINTA_2, grafico, pct, virgula


def residuos_teste(base):
    """Previsões e resíduos do modelo simples (duração pela distância) no conjunto de teste."""
    X_tr, X_te, y_tr, y_te = treino_teste(base)
    prev = LinearRegression().fit(X_tr, y_tr).predict(X_te)
    return prev, (y_te - prev).to_numpy()


@grafico("eda-residuos-previsto.png")
def residuos_previsto(base):
    prev, res = residuos_teste(base)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(0, color=TINTA_2, linewidth=1.5)
    ax.scatter(prev, res, s=12, color=AZUL, alpha=0.55, linewidths=0)
    ax.text(0.98, 0.96, "o erro cresce nas\nviagens longas", transform=ax.transAxes, ha="right", va="top",
            color=TINTA, fontsize=11)
    ax.grid(True, axis="both")
    ax.set_xlabel("duração prevista (min)")
    ax.set_ylabel("resíduo (min)")
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 0))
    return fig


@grafico("eda-residuos-hist.png")
def residuos_hist(base):
    _, res = residuos_teste(base)
    baixo, alto = np.percentile(res, [2.5, 97.5])
    fora = np.mean(np.abs(res) > 5)
    bordas = np.arange(-15, 21, 1.0)
    contagem, _ = np.histogram(res, bins=bordas)
    fig, ax = plt.subplots(figsize=(6, 4))
    for esq, n in zip(bordas[:-1], contagem):
        cauda = esq >= 5 or esq + 1 <= -5
        ax.bar(esq, n, width=1, align="edge", color=LARANJA if cauda else AZUL, edgecolor=SUPERFICIE, linewidth=1)
    topo = contagem.max()
    for v in (baixo, alto):
        ax.axvline(v, color=TINTA_2, linewidth=1.2, linestyle=(0, (4, 3)))
    ax.text(alto + 0.4, topo * 0.92, f"95% dos erros\nentre {virgula(baixo, 1)} e {virgula(alto, 1)}",
            color=TINTA, fontsize=11, va="top")
    ax.text(alto + 0.4, topo * 0.55, f"|erro| > 5 min:\n{pct(fora, 1)} das viagens", color=TINTA, fontsize=11, va="top")
    ax.set_xlim(-15, 20)
    ax.set_xlabel("resíduo no teste (min)")
    ax.set_ylabel("viagens")
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 0))
    return fig


@grafico("eda-heatmap-preditoras.png")
def heatmap_preditoras(base):
    reg = com_duracao(base).copy()
    reg["avulso"] = (reg["tipo_usuario"] == "avulso").astype(int)
    reg["choveu"] = reg["choveu"].astype(int)
    cols = ["distancia_km", "avulso", "choveu", "chuva_mm", "temp_max"]
    pares = reg[cols].corr().iloc[1:, :-1]
    mascara = np.triu(np.ones_like(pares, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(6, 4.2))
    sns.heatmap(pares, mask=mascara, cmap=DIVERGENTE, vmin=-1, vmax=1, annot=pares.map(virgula), fmt="",
                annot_kws={"color": TINTA, "fontsize": 11}, linewidths=2, linecolor=SUPERFICIE,
                cbar_kws={"shrink": 0.8}, ax=ax)
    ax.grid(False)
    ax.tick_params(axis="x", rotation=30)
    ax.tick_params(axis="y", rotation=0)
    for rotulo in ax.get_xticklabels() + ax.get_yticklabels():
        rotulo.set_color(TINTA_2)
    barra = ax.collections[0].colorbar
    barra.ax.tick_params(colors=MUDA)
    barra.outline.set_visible(False)
    barra.set_ticks([-1, -0.5, 0, 0.5, 1])
    barra.ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    return fig
