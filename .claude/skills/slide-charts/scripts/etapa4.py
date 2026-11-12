"""Gráficos da etapa 4: relações entre variáveis numéricas."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from dados import com_duracao
from tema import AZUL, DIVERGENTE, EIXO, LARANJA, MUDA, SUPERFICIE, TINTA, TINTA_2, grafico, virgula


@grafico("eda-scatter-distancia-duracao.png")
def scatter_distancia_duracao(base):
    reg = com_duracao(base)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for tipo, cor in [("assinante", AZUL), ("avulso", LARANJA)]:
        g = reg[reg["tipo_usuario"] == tipo]
        ax.scatter(g["distancia_km"], g["duracao_min"], s=10, color=cor, alpha=0.45, linewidths=0, label=tipo)
    ax.grid(True, axis="both")
    ax.set_xlabel("distância (km)")
    ax.set_ylabel("duração (min)")
    legenda = ax.legend(loc="upper left", markerscale=2.5)
    for marca in legenda.legend_handles:
        marca.set_alpha(1)
    return fig


@grafico("eda-padroes-scatter.png")
def padroes_scatter(base):
    """Dados sintéticos (não usa a base): os quatro padrões típicos de um scatter plot."""
    rng = np.random.default_rng(8)
    xs = rng.uniform(0, 10, 150)
    casos = [("linear positiva", 2 * xs + rng.normal(0, 2, 150)),
             ("linear negativa", -1.5 * xs + rng.normal(0, 2, 150)),
             ("não linear", (xs - 5) ** 2 + rng.normal(0, 1.5, 150)),
             ("sem relação", rng.normal(0, 1, 150))]
    fig, axs = plt.subplots(1, 4, figsize=(12, 3.1))
    for ax, (nome, ys) in zip(axs, casos):
        ax.scatter(xs, ys, s=12, color=AZUL, alpha=0.7, linewidths=0)
        ax.set_title(f"{nome}\nr = {virgula(np.corrcoef(xs, ys)[0, 1])}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for lado in ["left", "bottom"]:
            ax.spines[lado].set_color(EIXO)
    fig.tight_layout()
    return fig


@grafico("eda-heatmap-correlacao.png")
def heatmap_correlacao(base):
    cols = ["distancia_km", "duracao_min", "avaliacao", "chuva_mm", "temp_max", "capacidade"]
    # sem a diagonal (sempre 1) e sem a metade de cima, que repete a de baixo
    pares = base[cols].corr().iloc[1:, :-1]
    mascara = np.triu(np.ones_like(pares, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
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
