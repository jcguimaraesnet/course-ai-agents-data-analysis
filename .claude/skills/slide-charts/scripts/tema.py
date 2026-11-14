"""Tema escuro dos gráficos dos slides: paleta validada, estilo e formatação pt-BR.

Importar este módulo já aplica o estilo do matplotlib. Os módulos etapaN.py
registram cada gráfico com @grafico("eda-<assunto>.png").
"""
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Paleta validada com o validador da skill dataviz no modo escuro, contra a superfície.
SUPERFICIE = "#1e1f29"                                  # fundo do gráfico
AZUL, LARANJA, AQUA = "#3987e5", "#d95926", "#199e70"   # séries, sempre nesta ordem
TINTA, TINTA_2, MUDA = "#f0efec", "#c3c2b7", "#898781"  # texto: principal, secundário e apagado
GRADE, EIXO = "#2c2e3b", "#3a3c4a"                      # linhas de grade e eixos
DIVERGENTE = LinearSegmentedColormap.from_list(        # correlação: azul, cinza neutro e vermelho
    "divergente", ["#2a78d6", "#383835", "#e66767"])

plt.rcParams.update({
    "figure.facecolor": SUPERFICIE, "axes.facecolor": SUPERFICIE, "savefig.facecolor": SUPERFICIE,
    "axes.edgecolor": EIXO, "axes.labelcolor": TINTA_2, "axes.labelsize": 12,
    "xtick.color": MUDA, "ytick.color": MUDA, "xtick.labelsize": 11, "ytick.labelsize": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": GRADE, "grid.linewidth": 1, "grid.linestyle": "-", "axes.axisbelow": True,
    "text.color": TINTA, "legend.frameon": False, "legend.labelcolor": TINTA_2, "legend.fontsize": 11,
    "font.size": 11, "axes.titlecolor": TINTA_2, "axes.titlesize": 12, "lines.linewidth": 2,
})

GRAFICOS = {}  # nome do PNG -> (deck, etapa, função)


def grafico(nome):
    """Registra a função como o gráfico <nome>: ela recebe a base do deck e devolve a figura.

    Módulos etapaN.py são do deck statistics-eda (eda-*.png); pm_etapaN.py, do predictive-modeling (pm-*.png).
    """
    def registrar(funcao):
        if nome in GRAFICOS:
            raise ValueError(f"Gráfico registrado duas vezes: {nome}")
        modulo = funcao.__module__
        deck = "predictive-modeling" if modulo.startswith("pm_") else "statistics-eda"
        GRAFICOS[nome] = (deck, int(modulo.removeprefix("pm_").removeprefix("etapa")), funcao)
        return funcao
    return registrar


def salvar(fig, caminho):
    fig.savefig(caminho, dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def virgula(valor, casas=2):
    """0.947 -> '0,95'; negativo com o sinal de menos tipográfico (−)."""
    return f"{valor:.{casas}f}".replace(".", ",").replace("-", "−")


def pct(valor, casas=1):
    """0.049 -> '4,9%'."""
    return f"{valor:.{casas}%}".replace(".", ",").replace("-", "−")
