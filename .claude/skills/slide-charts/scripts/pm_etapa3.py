"""Gráficos da etapa 3 de Modelagem Preditiva: o pipeline final da etapa 2 avaliado no teste.

Mesma divisão (estratificada, 80/20, random_state=42), mesmo pré-processamento e mesmo C do slide e
do live coding: o melhor da busca da etapa 2 (C = 0,1). Precisão e recall por threshold, a curva ROC
contra o modelo das três numéricas da etapa 1 e a sigmoid com os três primeiros usuários do teste.
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from tema import AZUL, LARANJA, MUDA, TINTA, TINTA_2, grafico, virgula

NUM = ["idade", "viagens_30d", "distancia_media_km", "avaliacao_media"]
CAT = ["regiao", "canal", "pagamento"]
NUM3 = ["idade", "viagens_30d", "distancia_media_km"]


def montar_pipeline():
    """O montar_pipeline() da etapa 2: mediana e padronização nas numéricas, one-hot nas categóricas."""
    pre = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), NUM),
                             ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
    return Pipeline([("pre", pre), ("clf", LogisticRegression())])


def pipeline_final(base):
    """A divisão e o pipeline final da etapa 2 (GridSearchCV no C): X_tr, X_te, y_tr, y_te e o modelo."""
    X, y = base[NUM + CAT], base["virou_assinante"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    busca = GridSearchCV(montar_pipeline(), {"clf__C": [0.001, 0.01, 0.1, 1, 10, 100]}, cv=5).fit(X_tr, y_tr)
    return X_tr, X_te, y_tr, y_te, busca.best_estimator_


@grafico("pm-precisao-recall.png")
def precisao_recall(base):
    _, X_te, _, y_te, pipe = pipeline_final(base)
    proba = pipe.predict_proba(X_te)[:, 1]
    cortes = np.round(np.arange(0.05, 0.951, 0.01), 2)
    previsoes = [(proba >= t).astype(int) for t in cortes]
    precisao = [precision_score(y_te, p, zero_division=0) for p in previsoes]
    recall = [recall_score(y_te, p) for p in previsoes]

    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.axvline(0.5, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(0.515, 0.12, "padrão do\npredict (0,5)", color=MUDA, fontsize=10, va="bottom")
    ax.plot(cortes, precisao, color=AZUL, label="precisão")
    ax.plot(cortes, recall, color=LARANJA, label="recall")
    for t in (0.3, 0.7):
        i = int(np.argmin(np.abs(cortes - t)))
        ax.plot([t, t], [precisao[i], recall[i]], "o", color=TINTA_2, markersize=5)
    ax.set_xlim(0.05, 0.95)
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    ax.set_xlabel("threshold sobre o predict_proba")
    ax.set_ylabel("valor no teste")
    ax.legend(loc="lower left")
    return fig


@grafico("pm-roc.png")
def roc(base):
    X_tr, X_te, y_tr, y_te, pipe = pipeline_final(base)
    simples = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr[NUM3], y_tr)
    curvas = [("pipeline da etapa 2", pipe.predict_proba(X_te)[:, 1], AZUL),
              ("só as três numéricas", simples.predict_proba(X_te[NUM3])[:, 1], LARANJA)]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([0, 1], [0, 1], color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(0.62, 0.55, "acaso (AUC 0,5)", color=MUDA, fontsize=10, rotation=33)
    for nome, proba, cor in curvas:
        fpr, tpr, _ = roc_curve(y_te, proba)
        ax.plot(fpr, tpr, color=cor, label=f"{nome}: AUC {virgula(roc_auc_score(y_te, proba), 3)}")
    proba = curvas[0][1]
    negativos, positivos = (y_te == 0).sum(), (y_te == 1).sum()
    for t, dx in ((0.5, 0.03), (0.3, 0.03)):
        prev = proba >= t
        fpr_t = (prev & (y_te == 0)).sum() / negativos
        tpr_t = (prev & (y_te == 1)).sum() / positivos
        ax.plot(fpr_t, tpr_t, "o", color=TINTA, markersize=6)
        ax.text(fpr_t + dx, tpr_t - 0.035, f"threshold {virgula(t, 1)}", color=TINTA, fontsize=10, va="top")
    ax.grid(axis="x")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.01)
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    ax.set_xlabel("taxa de falsos positivos")
    ax.set_ylabel("recall")
    ax.legend(loc="lower right")
    return fig


@grafico("pm-sigmoid.png")
def sigmoid(base):
    _, X_te, _, _, pipe = pipeline_final(base)
    clf = pipe[-1]
    z_usuarios = pipe[:-1].transform(X_te.head(3)) @ clf.coef_[0] + clf.intercept_[0]
    z = np.linspace(-6, 6, 300)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(0.5, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.axvline(0, color=MUDA, linewidth=1.5, linestyle=(0, (4, 3)))
    ax.text(-5.8, 0.53, "p = 0,5", color=MUDA, fontsize=10)
    ax.text(0.15, 0.03, "z = 0", color=MUDA, fontsize=10)
    ax.plot(z, 1 / (1 + np.exp(-z)), color=AZUL)
    deslocamentos = [(-1.2, 0.13, "right"), (-0.25, 0.17, "right"), (0.45, -0.17, "left")]
    for i, (zi, (dx, dy, ha)) in enumerate(zip(z_usuarios, deslocamentos), start=1):
        p = 1 / (1 + np.exp(-zi))
        ax.plot(zi, p, "o", color=LARANJA, markersize=7)
        ax.annotate(f"usuário {i}: {virgula(p, 3)}", xy=(zi, p), xytext=(zi + dx, p + dy), color=TINTA,
                    fontsize=10, ha=ha, arrowprops={"arrowstyle": "-", "color": MUDA})
    ax.set_xlim(-6, 6)
    ax.set_ylim(-0.02, 1.02)
    ax.xaxis.set_major_formatter(lambda v, _: virgula(v, 0))
    ax.yaxis.set_major_formatter(lambda v, _: virgula(v, 1))
    ax.set_xlabel("z (combinação linear das features)")
    ax.set_ylabel("p = σ(z)")
    return fig
