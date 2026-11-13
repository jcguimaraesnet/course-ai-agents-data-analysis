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
"""Gera os gráficos estáticos dos slides (public/eda-*.png) com a base das aulas.

Uso, na raiz do repo:
    uv run .claude/skills/slide-charts/scripts/gerar.py --lista
    uv run .claude/skills/slide-charts/scripts/gerar.py [trecho do nome ...] [--etapa N] [--saida PASTA]
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
from dados import REPO, carregar_base  # noqa: E402

# O seaborn 0.13 passa ao boxplot um parâmetro que o matplotlib 3.11 deprecou: o aviso é da biblioteca.
warnings.filterwarnings("ignore", message=".*vert: bool was deprecated")

for modulo in sorted(Path(__file__).resolve().parent.glob("etapa*.py")):
    importlib.import_module(modulo.stem)


def main():
    parser = argparse.ArgumentParser(description="Gera os gráficos estáticos dos slides.")
    parser.add_argument("nomes", nargs="*", help="trechos do nome do PNG (ex.: boxplot heatmap); sem nenhum, todos")
    parser.add_argument("--etapa", type=int, help="só os gráficos desta etapa")
    parser.add_argument("--saida", type=Path, default=REPO / "public", help="pasta de saída (padrão: public/)")
    parser.add_argument("--lista", action="store_true", help="só lista os gráficos, sem gerar")
    args = parser.parse_args()

    escolhidos = [(nome, etapa, funcao)
                  for nome, (etapa, funcao) in sorted(tema.GRAFICOS.items(), key=lambda g: (g[1][0], g[0]))
                  if (args.etapa is None or etapa == args.etapa)
                  and (not args.nomes or any(trecho in nome for trecho in args.nomes))]
    if not escolhidos:
        sys.exit("Nenhum gráfico com esse filtro; veja os nomes com --lista.")
    if args.lista:
        for nome, etapa, _ in escolhidos:
            print(f"etapa {etapa}  {nome}")
        return

    base = carregar_base()
    print(f"base: {len(base)} viagens ({base['duracao_min'].notna().sum()} com duração)")
    publico = REPO / "public"
    saida = args.saida.resolve()
    saida.mkdir(parents=True, exist_ok=True)
    for nome, _, funcao in escolhidos:
        destino = saida / nome
        tema.salvar(funcao(base), destino)
        situacao = ""
        if saida != publico:
            atual = publico / nome
            situacao = ("  (novo)" if not atual.exists()
                        else "  (igual ao public/)" if atual.read_bytes() == destino.read_bytes()
                        else "  (diferente do public/)")
        print(f"ok {destino.relative_to(REPO) if destino.is_relative_to(REPO) else destino}{situacao}")


if __name__ == "__main__":
    main()
