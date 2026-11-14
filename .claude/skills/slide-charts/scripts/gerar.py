# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas==3.1.1",
#     "numpy==2.5.4",
#     "matplotlib==3.11.2",
#     "seaborn==0.13.2",
#     "scipy==1.18.1",
#     "openpyxl==3.1.5",
#     "scikit-learn==1.9.1",
# ]
# ///
"""Gera os gráficos estáticos dos slides (public/eda-*.png e public/pm-*.png) com as bases das aulas.

Uso, na raiz do repo:
    uv run .claude/skills/slide-charts/scripts/gerar.py --lista
    uv run .claude/skills/slide-charts/scripts/gerar.py [trecho do nome ...] [--deck D] [--etapa N] [--saida PASTA]
"""
import argparse
import importlib
import sys
import warnings
from pathlib import Path

sys.dont_write_bytecode = True  # sem __pycache__ dentro da skill

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import tema  # noqa: E402
from dados import REPO, carregar_base, carregar_base_pm  # noqa: E402

# O seaborn 0.13 passa ao boxplot um parâmetro que o matplotlib 3.11 deprecou: o aviso é da biblioteca.
warnings.filterwarnings("ignore", message=".*vert: bool was deprecated")

PASTA = Path(__file__).resolve().parent
for modulo in sorted([*PASTA.glob("etapa*.py"), *PASTA.glob("pm_etapa*.py")]):
    importlib.import_module(modulo.stem)

BASES = {"statistics-eda": carregar_base, "predictive-modeling": carregar_base_pm}


def main():
    parser = argparse.ArgumentParser(description="Gera os gráficos estáticos dos slides.")
    parser.add_argument("nomes", nargs="*", help="trechos do nome do PNG (ex.: boxplot heatmap); sem nenhum, todos")
    parser.add_argument("--deck", choices=sorted(BASES), help="só os gráficos deste deck")
    parser.add_argument("--etapa", type=int, help="só os gráficos desta etapa")
    parser.add_argument("--saida", type=Path, default=REPO / "public", help="pasta de saída (padrão: public/)")
    parser.add_argument("--lista", action="store_true", help="só lista os gráficos, sem gerar")
    args = parser.parse_args()

    escolhidos = [(nome, deck, etapa, funcao)
                  for nome, (deck, etapa, funcao) in sorted(tema.GRAFICOS.items(), key=lambda g: (g[1][0], g[1][1], g[0]))
                  if (args.deck is None or deck == args.deck)
                  and (args.etapa is None or etapa == args.etapa)
                  and (not args.nomes or any(trecho in nome for trecho in args.nomes))]
    if not escolhidos:
        sys.exit("Nenhum gráfico com esse filtro; veja os nomes com --lista.")
    if args.lista:
        for nome, deck, etapa, _ in escolhidos:
            print(f"{deck}  etapa {etapa}  {nome}")
        return

    bases = {}
    for deck in sorted({deck for _, deck, _, _ in escolhidos}):
        bases[deck] = BASES[deck]()
        if deck == "statistics-eda":
            print(f"base: {len(bases[deck])} viagens ({bases[deck]['duracao_min'].notna().sum()} com duração)")
        else:
            print(f"base pm: {len(bases[deck])} usuários avulsos ({bases[deck]['virou_assinante'].mean():.1%} viraram assinantes)")
    publico = REPO / "public"
    saida = args.saida.resolve()
    saida.mkdir(parents=True, exist_ok=True)
    for nome, deck, _, funcao in escolhidos:
        destino = saida / nome
        tema.salvar(funcao(bases[deck]), destino)
        situacao = ""
        if saida != publico:
            atual = publico / nome
            situacao = ("  (novo)" if not atual.exists()
                        else "  (igual ao public/)" if atual.read_bytes() == destino.read_bytes()
                        else "  (diferente do public/)")
        print(f"ok {destino.relative_to(REPO) if destino.is_relative_to(REPO) else destino}{situacao}")


if __name__ == "__main__":
    main()
