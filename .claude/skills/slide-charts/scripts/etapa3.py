"""Gráficos da etapa 3: probabilidades e análise gráfica da duração das viagens."""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

from dados import com_duracao
from tema import AZUL, LARANJA, MUDA, SUPERFICIE, TINTA, TINTA_2, grafico, pct, virgula


@grafico("eda-pmf-avaliacao.png")
def pmf_avaliacao(base):
    pmf = base["avaliacao"].dropna().value_counts(normalize=True).sort_index()
    pmf = pmf.reindex([1.0, 2.0, 3.0, 4.0, 5.0], fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(pmf.index.astype(int), pmf.values, width=0.5, color=AZUL)
    for x, p in zip(pmf.index.astype(int), pmf.values):
        ax.text(x, p + 0.015, pct(p, 1), ha="center", va="bottom", color=TINTA, fontsize=11)
    ax.set_xlabel("avaliação (nota)")
    ax.set_ylabel("probabilidade")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 0.78)
    ax.yaxis.set_major_formatter(lambda v, _: pct(v, 0))
    return fig


@grafico("eda-ecdf-duracao.png")
def ecdf_duracao(base):
    dur = com_duracao(base)["duracao_min"]
    f30 = (dur <= 30).mean()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.ecdfplot(x=dur, ax=ax, color=AZUL, linewidth=2)
    ax.axvline(30, color=MUDA, linewidth=1)
    ax.plot([30], [f30], "o", ms=8, color=AZUL, markeredgecolor=SUPERFICIE, markeredgewidth=2)
    ax.annotate(f"F(30) = {virgula(f30, 3)}\nP(duração > 30) = {pct(1 - f30, 1)}",
                xy=(30, f30), xytext=(38, 0.62), color=TINTA, fontsize=11,
                arrowprops=dict(arrowstyle="-", color=MUDA, lw=1))
    ax.set_xlabel("duração da viagem (min)")
    ax.set_ylabel("proporção acumulada")
    ax.set_xlim(0, 80)
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    return fig


@grafico("eda-hist-duracao.png")
def hist_duracao(base):
    dur = com_duracao(base)["duracao_min"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(dur, bins=30, color=AZUL, edgecolor=SUPERFICIE, linewidth=1.2)
    for valor, nome, altura in [(dur.median(), "mediana", 0.92), (dur.mean(), "média", 0.80)]:
        ax.axvline(valor, color=TINTA_2, linewidth=1.5)
        ax.text(valor + 1, ax.get_ylim()[1] * altura, f"{nome} {virgula(valor)}", color=TINTA, fontsize=11)
    ax.set_xlabel("duração da viagem (min)")
    ax.set_ylabel("viagens")
    return fig


@grafico("eda-bins-duracao.png")
def bins_duracao(base):
    dur = com_duracao(base)["duracao_min"]
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.2), sharey=False)
    for ax, bins in zip(axs, [5, 30, 200]):
        ax.hist(dur, bins=bins, color=AZUL, edgecolor=SUPERFICIE, linewidth=0.8 if bins < 200 else 0.2)
        ax.set_title(f"bins = {bins}")
        ax.set_xlabel("duração (min)")
    axs[0].set_ylabel("viagens")
    fig.tight_layout()
    return fig


@grafico("eda-boxplot-duracao.png")
def boxplot_duracao(base):
    reg = com_duracao(base)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    sns.boxplot(data=reg, x="tipo_usuario", y="duracao_min", order=["assinante", "avulso"],
                hue="tipo_usuario", palette={"assinante": AZUL, "avulso": LARANJA}, width=0.45,
                legend=False, ax=ax, linewidth=1.5, linecolor=TINTA_2,
                flierprops=dict(marker="o", markersize=4, markerfacecolor=MUDA, markeredgecolor=MUDA, alpha=0.6))
    # anatomia anotada na caixa dos assinantes
    a = reg.loc[reg["tipo_usuario"] == "assinante", "duracao_min"]
    q1, med, q3 = a.quantile([0.25, 0.5, 0.75])
    bigode = a[a <= q3 + 1.5 * (q3 - q1)].max()
    for y, texto in [(q3, "Q3"), (med, "mediana"), (q1, "Q1"), (bigode, "limite: Q3 + 1,5 × IQR")]:
        ax.annotate(texto, xy=(0.24, y), xytext=(0.42, y), color=TINTA, fontsize=10, va="center",
                    arrowprops=dict(arrowstyle="-", color=MUDA, lw=1))
    ax.annotate("outliers", xy=(0, 52), xytext=(0.42, 52), color=TINTA, fontsize=10, va="center",
                arrowprops=dict(arrowstyle="-", color=MUDA, lw=1))
    ax.set_xlabel("")
    ax.set_ylabel("duração da viagem (min)")
    return fig


@grafico("eda-normal-duracao.png")
def normal_duracao(base):
    dur = com_duracao(base)["duracao_min"]
    m, s = dur.mean(), dur.std()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(dur, bins=40, density=True, color=AZUL, edgecolor=SUPERFICIE, linewidth=1, label="dados")
    x = np.linspace(-20, 80, 400)
    ax.plot(x, stats.norm.pdf(x, m, s), color=LARANJA, linewidth=2, label="normal (mesma média e desvio)")
    ax.axvline(0, color=MUDA, linewidth=1)
    ax.set_ylim(0, 0.085)
    ax.text(-24.5, 0.026, f"a normal põe\n{pct(stats.norm.cdf(0, m, s), 0)} das viagens\nabaixo de zero",
            color=TINTA, fontsize=9)
    ax.set_xlabel("duração da viagem (min)")
    ax.set_ylabel("densidade")
    ax.legend(loc="upper right")
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 2))
    return fig
