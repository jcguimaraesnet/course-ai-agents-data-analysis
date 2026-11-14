"""As bases das aulas, montadas com o código que está nas notas dos slides.

Estatística e EDA: carregar_base(). Modelagem Preditiva: carregar_base_pm().


Não há cópia do código aqui: o gerar_dados.py (etapa 1, mais o trecho de abril da
etapa 2) e o preparar_base.py (etapa 3) são lidos das notas do Live Coding e
executados numa pasta temporária. Se as notas mudarem, os gráficos acompanham.
"""
import contextlib
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
NOTAS = REPO / "pages" / "statistics-eda"

# (arquivo, início da linha "ARQUIVO ..." que vem logo antes do bloco ```python)
GERAR_DADOS = [
    ("slide-etapa1.md", "ARQUIVO 1 — gerar_dados.py"),
    ("slide-etapa2.md", "ARQUIVO 1 — acrescentar ao final do gerar_dados.py"),
]
PREPARAR_BASE = ("slide-etapa3.md", "ARQUIVO 1 — preparar_base.py")


def bloco_das_notas(arquivo, marcador, notas=NOTAS):
    """Devolve o código do primeiro bloco ```python depois da linha que começa com o marcador."""
    linhas = (notas / arquivo).read_text(encoding="utf-8").splitlines()
    try:
        inicio = next(i for i, linha in enumerate(linhas) if linha.startswith(marcador))
        abre = next(i for i in range(inicio + 1, len(linhas)) if linhas[i].startswith("```python"))
        fecha = next(i for i in range(abre + 1, len(linhas)) if linhas[i].startswith("```"))
    except StopIteration:
        raise SystemExit(f"Não achei o código depois de '{marcador}' em {arquivo}: "
                         "o marcador ou a cerca ```python mudou nas notas?") from None
    return "\n".join(linhas[abre + 1:fecha]) + "\n"


def carregar_base():
    """Gera os arquivos de dados numa pasta temporária e devolve a base limpa da etapa 3."""
    gerar_dados = "".join(bloco_das_notas(*bloco) for bloco in GERAR_DADOS)
    preparar_base = bloco_das_notas(*PREPARAR_BASE)
    with tempfile.TemporaryDirectory() as pasta, contextlib.chdir(pasta):
        exec(compile(gerar_dados, "gerar_dados.py", "exec"), {"__name__": "__main__"})
        modulo = {"__name__": "preparar_base"}
        exec(compile(preparar_base, "preparar_base.py", "exec"), modulo)
        return modulo["carregar_base"]()


NOTAS_PM = REPO / "pages" / "predictive-modeling"
GERAR_DADOS_PM = ("slide-etapa1.md", "ARQUIVO 1 — gerar_dados.py")


def carregar_base_pm():
    """Gera o usuarios_avulsos.csv do deck de Modelagem Preditiva (notas da etapa 1) e devolve o DataFrame."""
    import pandas as pd
    arquivo, marcador = GERAR_DADOS_PM
    codigo = bloco_das_notas(arquivo, marcador, NOTAS_PM)
    with tempfile.TemporaryDirectory() as pasta, contextlib.chdir(pasta):
        exec(compile(codigo, "gerar_dados.py", "exec"), {"__name__": "__main__"})
        return pd.read_csv("usuarios_avulsos.csv")


def com_duracao(base):
    """Só as viagens com duração registrada: a duração ausente não é preenchida."""
    return base.dropna(subset=["duracao_min"])
