"""Gráficos da etapa 2 de Modelagem Preditiva: a busca em grade do C da regressão logística.

Mesma divisão, pré-processamento e grade do slide e do live coding da etapa 2: estratificada,
80/20, random_state=42; GridSearchCV com cv=5.
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from tema import AZUL, MUDA, TINTA, grafico, virgula

NUM = ["idade", "viagens_30d", "distancia_media_km", "avaliacao_media"]
CAT = ["regiao", "canal", "pagamento"]
GRADE_C = [0.001, 0.01, 0.1, 1, 10, 100]


def rotulo_c(c):
    return virgula(c, 3).rstrip("0").rstrip(",")


@grafico("pm-busca-c.png")
def busca_c(base):
    X, y = base[NUM + CAT], base["virou_assinante"]
    X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    pre = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), NUM),
                             ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
    busca = GridSearchCV(Pipeline([("pre", pre), ("clf", LogisticRegression())]),
                         {"clf__C": GRADE_C}, cv=5).fit(X_tr, y_tr)
    media = busca.cv_results_["mean_test_score"]
    dp = busca.cv_results_["std_test_score"]
    referencia = 1 - y_tr.mean()
    x = np.arange(len(GRADE_C))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(referencia, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(len(GRADE_C) - 1, referencia - 0.006, f"sempre \"não vira\": {virgula(referencia)}",
            color=MUDA, fontsize=10, ha="right", va="top")
    ax.fill_between(x, media - dp, media + dp, color=AZUL, alpha=0.18, linewidth=0)
    ax.plot(x, media, color=AZUL, marker="o", markersize=6)
    i = int(np.argmax(media))
    ax.annotate(f"melhor: C = {rotulo_c(GRADE_C[i])}\n{virgula(media[i], 3)}", xy=(x[i], media[i]),
                xytext=(x[i] + 0.4, media[i] - 0.045), color=TINTA, fontsize=10,
                arrowprops={"arrowstyle": "-", "color": MUDA})
    ax.set_xticks(x, [rotulo_c(c) for c in GRADE_C])
    ax.set_ylim(0.69, 0.84)
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v))
    ax.set_xlabel("C (menor = mais regularização)")
    ax.set_ylabel("acurácia média na validação cruzada")
    return fig
