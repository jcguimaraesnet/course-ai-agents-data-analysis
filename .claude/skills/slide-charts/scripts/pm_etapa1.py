"""Gráficos da etapa 1 de Modelagem Preditiva: underfitting e overfitting pela profundidade da árvore.

Mesma divisão e mesmas colunas do slide e do live coding da etapa 1: as três colunas numéricas sem
ausentes, 80% para treino e 20% para teste, random_state=42 (sem estratificar: a estratificação é da etapa 2).
"""
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from tema import AZUL, LARANJA, MUDA, TINTA_2, grafico, virgula

NUMERICAS = ["idade", "viagens_30d", "distancia_media_km"]


@grafico("pm-complexidade-arvore.png")
def complexidade_arvore(base):
    X_tr, X_te, y_tr, y_te = train_test_split(base[NUMERICAS], base["virou_assinante"],
                                              test_size=0.2, random_state=42)
    profundidades = list(range(1, 21))
    treino, teste = [], []
    for d in profundidades:
        arvore = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_tr, y_tr)
        treino.append(arvore.score(X_tr, y_tr))
        teste.append(arvore.score(X_te, y_te))
    referencia = max(y_te.mean(), 1 - y_te.mean())

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(referencia, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(6.2, referencia - 0.012, f"sempre \"não vira\": {virgula(referencia)}", color=MUDA,
            fontsize=10, ha="left", va="top")
    ax.plot(profundidades, treino, color=AZUL, marker="o", markersize=4, label="treino")
    ax.plot(profundidades, teste, color=LARANJA, marker="o", markersize=4, label="teste")
    ax.text(1.3, 0.7, "underfitting", color=TINTA_2, fontsize=11)
    ax.text(19.7, 0.9, "overfitting", color=TINTA_2, fontsize=11, ha="right")
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_ylim(0.65, 1.01)
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v))
    ax.set_xlabel("profundidade máxima da árvore (max_depth)")
    ax.set_ylabel("acurácia")
    ax.legend(loc="upper left")
    return fig
