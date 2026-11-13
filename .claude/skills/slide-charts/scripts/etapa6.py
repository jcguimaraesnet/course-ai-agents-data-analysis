"""Gráficos da etapa 6: teste de hipótese, p-valor e intervalos de confiança da avaliação.

A comparação dos slides é a nota média de avulsos e assinantes (só as viagens avaliadas).
As simulações usam as mesmas sementes e o mesmo número de repetições das demos dos slides,
para que o gráfico e a saída da demo mostrem os mesmos números.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from tema import AQUA, AZUL, LARANJA, MUDA, SUPERFICIE, TINTA, TINTA_2, grafico, pct, virgula

COR = {"assinante": AZUL, "avulso": LARANJA}


def notas(base, tipo):
    """As notas de um tipo de usuário, na ordem da base, só entre as viagens avaliadas."""
    av = base.dropna(subset=["avaliacao"])
    return av.loc[av["tipo_usuario"] == tipo, "avaliacao"].to_numpy()


def diferenca(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)


def ic_bootstrap(*amostras, estatistica=np.mean):
    """IC de 95% do scipy.stats.bootstrap, como no código dos slides (BCa, semente 42)."""
    res = stats.bootstrap(amostras, estatistica, confidence_level=0.95, rng=np.random.default_rng(42))
    return res.confidence_interval.low, res.confidence_interval.high


@grafico("eda-permutacao-avaliacao.png")
def permutacao_avaliacao(base):
    # Notas ordenadas, como o np.repeat da demo: a mesma permutação dá o mesmo p-valor.
    avulso, assinante = np.sort(notas(base, "avulso")), np.sort(notas(base, "assinante"))
    obs = avulso.mean() - assinante.mean()
    rng = np.random.default_rng(42)
    todas = np.concatenate([avulso, assinante])
    difs = []
    for _ in range(5_000):
        p = rng.permutation(todas)
        difs.append(p[:avulso.size].mean() - p[avulso.size:].mean())
    difs = np.array(difs)
    p_valor = np.mean(np.abs(difs) >= abs(obs))

    largura = abs(obs) / 6                      # o |obs| cai exatamente numa borda de bin
    limite = largura * np.ceil(np.abs(difs).max() / largura)
    bordas = np.arange(-limite, limite + largura / 2, largura)
    contagem, _ = np.histogram(difs, bins=bordas)
    fig, ax = plt.subplots(figsize=(6, 4))
    for esq, n in zip(bordas[:-1], contagem):
        cauda = esq + largura <= -abs(obs) + 1e-12 or esq >= abs(obs) - 1e-12
        ax.bar(esq, n, width=largura, align="edge", color=LARANJA if cauda else AZUL,
               edgecolor=SUPERFICIE, linewidth=1)
    ax.axvline(obs, color=TINTA_2, linewidth=1.5)
    topo = contagem.max()
    ax.text(obs - largura * 0.6, topo * 0.92, f"diferença\nobservada\n{virgula(obs, 3)}",
            ha="right", va="top", color=TINTA, fontsize=11)
    ax.text(abs(obs) + largura * 0.8, topo * 0.55, f"caudas: {pct(p_valor, 1)}\ndas simulações\n= p-valor",
            ha="left", va="top", color=TINTA, fontsize=11)
    ax.set_xlabel("diferença de nota média sob H₀ (avulso − assinante)")
    ax.set_ylabel("simulações")
    ax.set_xticks(np.arange(-0.10, 0.101, 0.05))
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 2))
    return fig


@grafico("eda-bootstrap-avaliacao.png")
def bootstrap_avaliacao(base):
    avulso = np.sort(notas(base, "avulso"))     # como o np.repeat da demo
    rng = np.random.default_rng(42)
    medias = np.array([rng.choice(avulso, size=avulso.size).mean() for _ in range(5_000)])
    baixo, alto = np.percentile(medias, [2.5, 97.5])

    # A média de 770 notas inteiras só assume múltiplos de 1/770: bins de 3/770 evitam o pente.
    passo = 1 / avulso.size
    bordas = np.arange(medias.min() - passo / 2, medias.max() + 3 * passo, 3 * passo)
    contagem, _ = np.histogram(medias, bins=bordas)
    fig, ax = plt.subplots(figsize=(6, 4))
    for esq, dir_, n in zip(bordas[:-1], bordas[1:], contagem):
        dentro = baixo <= (esq + dir_) / 2 <= alto
        ax.bar(esq, n, width=dir_ - esq, align="edge", color=AZUL if dentro else MUDA,
               alpha=1 if dentro else 0.45, edgecolor=SUPERFICIE, linewidth=1)
    topo = contagem.max()
    y = topo * 1.12
    ax.plot([baixo, alto], [y, y], color=TINTA_2, linewidth=1.5)
    for x in (baixo, alto):
        ax.plot([x, x], [y - topo * 0.03, y + topo * 0.03], color=TINTA_2, linewidth=1.5)
    ax.text((baixo + alto) / 2, y + topo * 0.05, f"IC 95%: {virgula(baixo, 3)} a {virgula(alto, 3)}",
            ha="center", va="bottom", color=TINTA, fontsize=11)
    ax.set_ylim(0, topo * 1.32)
    ax.set_xlabel("nota média dos avulsos em cada reamostra")
    ax.set_ylabel("reamostras")
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 2))
    return fig


@grafico("eda-ic-cobertura.png")
def ic_cobertura(base):
    # Uma população conhecida (as notas dos avulsos) e 20 amostras de 100 notas cada.
    populacao = notas(base, "avulso")
    media_real = populacao.mean()
    rng = np.random.default_rng(3)
    t = stats.t.ppf(0.975, df=99)
    fig, ax = plt.subplots(figsize=(6, 4))
    for i in range(20):
        amostra = rng.choice(populacao, size=100)
        m, ep = amostra.mean(), amostra.std(ddof=1) / np.sqrt(amostra.size)
        baixo, alto = m - t * ep, m + t * ep
        contem = baixo <= media_real <= alto
        cor = AZUL if contem else LARANJA
        ax.plot([baixo, alto], [i, i], color=cor, linewidth=2, solid_capstyle="round")
        ax.plot([m], [i], "o", ms=6, color=cor, markeredgecolor=SUPERFICIE, markeredgewidth=1.5)
        if not contem:
            ax.text(alto + 0.01, i, "não contém", va="center", color=TINTA, fontsize=11)
    ax.axvline(media_real, color=TINTA_2, linewidth=1.5)
    ax.text(media_real, 20.3, f"média real {virgula(media_real, 2)}", ha="center", va="bottom",
            color=TINTA, fontsize=11)
    ax.set_ylim(-1, 21.6)
    ax.set_xlim(4.33, 5.0)
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("IC 95% da nota média, em 20 amostras de 100 viagens")
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    return fig


@grafico("eda-sobreposicao-ic.png")
def sobreposicao_ic(base):
    grupos = {tipo: notas(base, tipo) for tipo in ("assinante", "avulso")}
    ics = {tipo: ic_bootstrap(x) for tipo, x in grupos.items()}
    dif = grupos["avulso"].mean() - grupos["assinante"].mean()
    dif_baixo, dif_alto = ic_bootstrap(grupos["avulso"], grupos["assinante"], estatistica=diferenca)

    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(12, 2.9), gridspec_kw={"wspace": 0.3})
    inicio = max(baixo for baixo, _ in ics.values())
    fim = min(alto for _, alto in ics.values())
    esq.axvspan(inicio, fim, color=TINTA, alpha=0.12, linewidth=0)
    esq.text((inicio + fim) / 2, 1.62, "sobreposição", ha="center", va="bottom", color=TINTA_2, fontsize=11)
    for y, (tipo, (baixo, alto)) in enumerate(ics.items()):
        media = grupos[tipo].mean()
        esq.plot([baixo, alto], [y, y], color=COR[tipo], linewidth=3, solid_capstyle="round")
        esq.plot([media], [y], "o", ms=9, color=COR[tipo], markeredgecolor=SUPERFICIE, markeredgewidth=2)
        esq.text(alto + 0.004, y, f"{tipo}  {virgula(baixo, 3)} a {virgula(alto, 3)}", va="center",
                 color=TINTA, fontsize=11)
    esq.set_title("IC 95% de cada grupo", loc="left")
    esq.set_xlim(4.50, 4.76)
    esq.set_ylim(-0.6, 1.9)
    esq.set_xlabel("nota média")

    dir_.axvline(0, color=TINTA_2, linewidth=1.5, linestyle=(0, (4, 3)))
    dir_.text(0.002, 0.62, "zero", color=TINTA_2, fontsize=11, va="bottom")
    dir_.plot([dif_baixo, dif_alto], [0, 0], color=AQUA, linewidth=3, solid_capstyle="round")
    dir_.plot([dif], [0], "o", ms=9, color=AQUA, markeredgecolor=SUPERFICIE, markeredgewidth=2)
    dir_.text(dif, 0.22, f"{virgula(dif_baixo, 3)} a {virgula(dif_alto, 3)}", ha="center", va="bottom",
              color=TINTA, fontsize=11)
    dir_.set_title("IC 95% da diferença (avulso − assinante)", loc="left")
    dir_.set_xlim(-0.15, 0.05)
    dir_.set_xticks(np.arange(-0.15, 0.051, 0.05))
    dir_.set_ylim(-0.6, 0.9)
    dir_.set_xlabel("diferença de nota média")

    for ax in (esq, dir_):
        ax.set_yticks([])
        ax.grid(False)
        ax.spines["left"].set_visible(False)
        ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 2))
    return fig


@grafico("eda-eixo-recortado.png")
def eixo_recortado(base):
    tipos = ["assinante", "avulso"]
    medias = {tipo: notas(base, tipo).mean() for tipo in tipos}
    ics = {tipo: ic_bootstrap(notas(base, tipo)) for tipo in tipos}
    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(12, 2.9), gridspec_kw={"wspace": 0.25})
    for ax in (esq, dir_):
        ax.bar(tipos, [medias[t] for t in tipos], width=0.5, color=[COR[t] for t in tipos])
        ax.set_ylabel("nota média")

    esq.set_ylim(4.55, 4.65)
    esq.set_title("gerado: eixo recortado de 4,55 a 4,65", loc="left")
    for t in tipos:
        esq.text(t, medias[t] + 0.002, virgula(medias[t]), ha="center", va="bottom", color=TINTA, fontsize=11)
    esq.yaxis.set_major_formatter(lambda v, _: virgula(v, 2))

    for t in tipos:
        baixo, alto = ics[t]
        dir_.errorbar(t, medias[t], yerr=[[medias[t] - baixo], [alto - medias[t]]], color=TINTA_2,
                      capsize=6, linewidth=1.5)
        dir_.text(t, alto + 0.12, virgula(medias[t]), ha="center", va="bottom", color=TINTA, fontsize=11)
    dir_.set_ylim(0, 5.6)
    dir_.set_yticks([0, 1, 2, 3, 4, 5])
    dir_.set_title("corrigido: eixo desde o zero, com IC 95%", loc="left")
    return fig
