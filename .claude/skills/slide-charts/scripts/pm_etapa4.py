"""Gráficos da etapa 4 de Modelagem Preditiva: curvas de aprendizado e SVM.

As curvas de aprendizado usam a divisão e o pipeline da etapa 2 (learning_curve com cv=5 e cinco
tamanhos de treino), com o C de 0,001, 0,01 e 1, como no slide e no live coding. Os gráficos do SVM
usam dados sintéticos com semente fixa: os 40 pontos do exemplo de margem máxima do scikit-learn
(os mesmos da demo dos vetores de suporte), uma versão mais espalhada deles para o C e as luas
(make_moons) para o kernel RBF.
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs, make_moons
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.svm import SVC

from pm_etapa3 import CAT, NUM, montar_pipeline
from tema import AZUL, LARANJA, MUDA, SUPERFICIE, TINTA, TINTA_2, grafico, virgula

CORES = np.array([AZUL, LARANJA])


@grafico("pm-curvas-aprendizado.png")
def curvas_aprendizado(base):
    X, y = base[NUM + CAT], base["virou_assinante"]
    X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    referencia = 1 - y_tr.mean()

    fig, eixos = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, C in zip(eixos, [0.001, 0.01, 1]):
        tam, treino, valid = learning_curve(montar_pipeline().set_params(clf__C=C), X_tr, y_tr, cv=5,
                                            train_sizes=np.linspace(0.1, 1, 5))
        ax.axhline(referencia, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
        ax.plot(tam, treino.mean(axis=1), color=AZUL, marker="o", markersize=5, label="treino")
        ax.plot(tam, valid.mean(axis=1), color=LARANJA, marker="o", markersize=5, label="validação")
        ax.set_title(f"C = {virgula(C, 3).rstrip('0').rstrip(',')}")
        ax.set_xticks([500, 1000, 1500])
        ax.xaxis.set_major_formatter(lambda v, _: f"{v:,.0f}".replace(",", "."))
        ax.set_xlabel("usuários no treino")
    eixos[0].text(1900, referencia - 0.004, f"referência {virgula(referencia, 3)}", color=MUDA, fontsize=10,
                  ha="right", va="top")
    eixos[0].set_ylim(0.68, 0.84)
    eixos[0].set_yticks([0.70, 0.74, 0.78, 0.82])
    eixos[0].yaxis.set_major_formatter(lambda v, _: virgula(v))
    eixos[0].set_ylabel("acurácia")
    eixos[0].legend(loc="upper left")
    fig.tight_layout()
    return fig


def desenhar_svm(ax, modelo, X, y, margem=True, vetores=True):
    """Pontos, fronteira, margens e vetores de suporte de um SVC já treinado em 2D."""
    x0, x1 = X[:, 0].min() - 1, X[:, 0].max() + 1
    y0, y1 = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x0, x1, 300), np.linspace(y0, y1, 300))
    nota = modelo.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, (nota > 0).astype(int), levels=[-0.5, 0.5, 1.5], colors=[AZUL, LARANJA], alpha=0.12)
    ax.contour(xx, yy, nota, levels=[0], colors=[TINTA], linewidths=2)
    if margem:
        ax.contour(xx, yy, nota, levels=[-1, 1], colors=[MUDA], linewidths=1.5, linestyles=[(0, (4, 3))])
    ax.scatter(X[:, 0], X[:, 1], c=CORES[y], s=28, edgecolors=SUPERFICIE, linewidths=0.8, zorder=3)
    if vetores:
        sv = X[modelo.support_]
        ax.scatter(sv[:, 0], sv[:, 1], s=140, facecolors="none", edgecolors=TINTA, linewidths=1.6, zorder=4)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)


@grafico("pm-svm-margem.png")
def svm_margem(base):
    X, y = make_blobs(40, centers=2, random_state=6)
    modelo = SVC(kernel="linear", C=1000).fit(X, y)

    fig, ax = plt.subplots(figsize=(6, 4))
    desenhar_svm(ax, modelo, X, y)
    ax.set_xlabel("feature 1")
    ax.set_ylabel("feature 2")
    i = modelo.support_[np.argmax(X[modelo.support_, 1])]
    ax.annotate("vetor de suporte", xy=X[i], xytext=(X[i, 0] + 1.6, X[i, 1] + 1.2), color=TINTA, fontsize=10,
                arrowprops={"arrowstyle": "-", "color": MUDA})
    return fig


@grafico("pm-svm-c.png")
def svm_c(base):
    X, y = make_blobs(80, centers=2, random_state=6, cluster_std=1.8)

    fig, eixos = plt.subplots(1, 2, figsize=(6, 3.4))
    for ax, C in zip(eixos, [0.01, 100]):
        modelo = SVC(kernel="linear", C=C).fit(X, y)
        desenhar_svm(ax, modelo, X, y)
        ax.set_title(f"C = {virgula(C, 2).rstrip('0').rstrip(',')}: {modelo.n_support_.sum()} vetores")
    fig.tight_layout()
    return fig


@grafico("pm-rbf-gamma.png")
def rbf_gamma(base):
    X, y = make_moons(300, noise=0.25, random_state=0)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)
    modelos = [("linear", SVC(kernel="linear")),
               ("RBF, γ = 0,1", SVC(kernel="rbf", gamma=0.1)),
               ("RBF, γ = 1", SVC(kernel="rbf", gamma=1)),
               ("RBF, γ = 100", SVC(kernel="rbf", gamma=100))]

    fig, eixos = plt.subplots(2, 2, figsize=(6, 4.6))
    for ax, (nome, modelo) in zip(eixos.ravel(), modelos):
        modelo.fit(X_tr, y_tr)
        desenhar_svm(ax, modelo, X_tr, y_tr, margem=False, vetores=False)
        ax.set_title(f"{nome}: {virgula(modelo.score(X_tr, y_tr))} / {virgula(modelo.score(X_te, y_te))}",
                     fontsize=11)
    fig.text(0.5, 0.005, "acurácia no treino / no teste", color=TINTA_2, fontsize=10, ha="center")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    return fig
