---
layout: section
routeAlias: etapa3
---

## **Etapa 3:** Avaliação de Classificadores IA

---
layout: section
---

## Matriz de **confusão**
**Acertos e erros, separados por tipo**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Model evaluation
source: https://scikit-learn.org/stable/modules/model_evaluation.html
---

# Medir antes de ajustar

#### **O pipeline salvo na etapa 2 volta, com a mesma divisão**

::left::

```python [etapa3.ipynb]
import joblib
import pandas as pd
from pipeline_assinatura import dividir

df = pd.read_csv("usuarios_avulsos.csv")
X_tr, X_te, y_tr, y_te = dividir(df)
pipe = joblib.load("pipeline_assinatura.joblib")

pipe.score(X_te, y_te)    # 0.832
y_te.sum()                # 171 assinantes
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Mesma divisão** — o `dividir` da etapa 2 refaz treino e teste com `stratify` e `random_state=42`.
- **Mesmo modelo** — o pipeline final, com `C = 0,1`, carregado do `.joblib`: nada é retreinado.
- **A pergunta** — 83,2% de acerto. Mas quantos dos 171 assinantes do teste o modelo encontra?

</div>

<!--
- "medir antes de treinar": a etapa avalia o modelo pronto antes de qualquer ajuste. É o mesmo fluxo do TP2, que recarrega o pipeline do TP1.
- o teste tem 600 usuários: 429 não viraram assinantes e 171 viraram.
- a referência (sempre "não vira") acerta 71,5% e não encontra nenhum assinante: a acurácia sozinha não mostra isso.
- se o .joblib não existir, rode o pipeline_assinatura.py da etapa 2.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: confusion_matrix
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
---

# Matriz de confusão

#### **Cada previsão cai numa de quatro células: dois acertos e dois tipos de erro**

::left::

```python [etapa3.ipynb]
from sklearn.metrics import confusion_matrix

y_pred = pipe.predict(X_te)
confusion_matrix(y_te, y_pred)
# [[404,  25],
#  [ 76,  95]]
```

<div class="grid grid-cols-[auto_1fr_1fr] gap-1 text-sm text-center mt-4">
  <div></div><div class="text-gray-400">previsto 0</div><div class="text-gray-400">previsto 1</div>
  <div class="text-gray-400 text-right pr-2 self-center">real 0</div><div class="bg-blue-600/50 rounded py-2"><b>VN</b> 404</div><div class="bg-orange-600/70 rounded py-2"><b>FP</b> 25</div>
  <div class="text-gray-400 text-right pr-2 self-center">real 1</div><div class="bg-orange-600/70 rounded py-2"><b>FN</b> 76</div><div class="bg-blue-600/50 rounded py-2"><b>VP</b> 95</div>
</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Linhas e colunas** — a linha é a classe real; a coluna, a prevista: `[[VN, FP], [FN, VP]]`.
- **VP e VN** — os acertos: 95 assinantes encontrados e 404 não assinantes descartados.
- **FP** — 25 alarmes falsos: o modelo disse "vira", e o usuário não virou.
- **FN** — 76 assinantes que passaram despercebidos.

</div>

<!--
- 404 + 25 + 76 + 95 = 600, o tamanho do teste; 76 + 95 = 171 assinantes.
- vn, fp, fn, vp = confusion_matrix(y_te, y_pred).ravel() dá nome às quatro células, nessa ordem.
- erro comum: ler a matriz com linhas e colunas trocadas. Outros livros e ferramentas põem a previsão nas linhas.
- ConfusionMatrixDisplay.from_estimator(pipe, X_te, y_te) desenha a mesma matriz.
-->

---
layout: default
sourceLabel: Hands-On ML, cap. 3
source: https://github.com/ageron/handson-mlp/blob/main/03_classification.ipynb
---

# A matriz em termos de negócio

#### **O time comercial liga para quem o modelo aponta como futuro assinante**

<div class="h-4" />

| Célula | Usuários | O que aconteceu | Custo para a empresa |
|--------|----------|-----------------|----------------------|
| **VP** | 95 | ligou, e o usuário assinou | uma ligação, que vira receita |
| **FP** | 25 | ligou para quem não ia assinar | uma ligação desperdiçada |
| **FN** | 76 | não ligou para quem assinaria | uma venda que pode não acontecer |
| **VN** | 404 | não ligou, e ele não ia assinar | nenhum |

<div class="h-2" />

> [!NOTE]
> A referência acerta 71,5% com 171 FN e nenhum VP: o time comercial nunca ligaria para ninguém.

<!--
- os custos não são simétricos: aqui, um FN (uma assinatura perdida) costuma custar mais que um FP (uma ligação).
- pergunta para a turma: se o contato fosse caro, como uma visita presencial, qual erro pesaria mais?
- é a leitura que o Exercício 1 do TP2 pede: o significado de cada célula em termos de negócio.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Hands-On ML, cap. 3
source: https://github.com/ageron/handson-mlp/blob/main/03_classification.ipynb
---

# Demo: a acurácia que engana

#### **Com 1% de fraudes, quem nunca acusa fraude acerta 99%**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    confusion_matrix, recall_score)
rng = np.random.default_rng(0)
y = (rng.random(10_000) < 0.01).astype(int)
X = np.zeros((10_000, 1))   # nem olha os dados
ref = DummyClassifier().fit(X, y)
prev = ref.predict(X)
print("acurácia:", ref.score(X, y))
print("recall:", recall_score(y, prev))
print(confusion_matrix(y, prev))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Os dados** — 10.000 transações, cerca de 1% de fraudes.
- **O modelo** — o `DummyClassifier`, que responde sempre a classe mais comum: "não é fraude".
- **Antes de executar** — qual a acurácia? E quantas fraudes ele encontra?

</div>

<!--
- saída esperada: acurácia 0,9911; recall 0,0; matriz [[9911 0] [89 0]]: as 89 fraudes estão todas na segunda linha, na coluna do 0.
- no capítulo 3 do Hands-On ML, o mesmo truque acerta 91% dizendo que nenhuma imagem é um 5.
- com classes desbalanceadas, a acurácia mede sobretudo a classe comum: por isso precisão e recall.
-->

---
layout: section
---

## Precisão, recall e **threshold**
**Quanto confiar nos alertas e quantos casos escapam**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Precision, recall and F-measures
source: https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics
---

# Precisão e recall

#### **Duas perguntas diferentes sobre os mesmos alertas**

::left::

```python [etapa3.ipynb]
from sklearn.metrics import (
    f1_score, precision_score, recall_score)

precision_score(y_te, y_pred)   # 0.792
recall_score(y_te, y_pred)      # 0.556
f1_score(y_te, y_pred)          # 0.653
```

$$
\text{precisão} = \frac{VP}{VP + FP} = \frac{95}{120} \qquad \text{recall} = \frac{VP}{VP + FN} = \frac{95}{171}
$$

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Precisão** — dos 120 apontados, 79% assinaram: mede o desperdício de ligações.
- **Recall** — dos 171 assinantes, o modelo achou 56%: mede quem escapa.
- **F1** — a média harmônica das duas: só é alta se as duas forem altas.

</div>

<!--
- recall também se chama sensibilidade ou taxa de verdadeiros positivos: é o eixo vertical da curva ROC.
- F1 = 2 · P · R / (P + R) = 0,653. Ele favorece modelos com precisão e recall parecidos, o que nem sempre é o que o negócio quer.
- classification_report(y_te, y_pred) mostra as três métricas de cada classe; a etapa 4 usa no caso de três classes.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: predict_proba
source: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
---

# O threshold de decisão

#### **O predict corta a probabilidade em 0,5, mas o corte pode ser outro**

::left::

```python [etapa3.ipynb]
proba = pipe.predict_proba(X_te)[:, 1]

y_03 = (proba >= 0.3).astype(int)
y_03.sum()                      # 212 ligações
precision_score(y_te, y_03)     # 0.608
recall_score(y_te, y_03)        # 0.754
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **Threshold menor** — mais ligações: o recall sobe e a precisão cai.
- **Threshold maior** — menos ligações, mais certeiras, mas mais assinantes escapam.

</div>

::right::

<AssetImg src="pm-precisao-recall.png" class="rounded-lg w-full" />

<!--
- predict_proba devolve uma coluna por classe; [:, 1] é a probabilidade de virar assinante.
- pipe.predict(X_te) é o mesmo que (proba >= 0.5).astype(int).
- os pontos no gráfico marcam os thresholds 0,3 e 0,7 da tabela do próximo slide.
- desde o scikit-learn 1.5, o TunedThresholdClassifierCV escolhe o threshold por validação cruzada: fica como leitura.
-->

---
layout: default
sourceLabel: Hands-On ML, cap. 3
source: https://github.com/ageron/handson-mlp/blob/main/03_classification.ipynb
---

# Escolhendo o ponto de operação

#### **O threshold sai da prioridade do negócio, não do padrão de 0,5**

<div class="h-2" />

| Threshold | Ligações | Precisão | Recall | Assinantes sem ligação (FN) |
|-----------|----------|----------|--------|-----------------------------|
| 0,2 | 291 | 0,51 | 0,87 | 22 |
| 0,3 | 212 | 0,61 | 0,75 | 42 |
| 0,5 | 120 | 0,79 | 0,56 | 76 |
| 0,7 | 66 | 0,94 | 0,36 | 109 |

<div class="text-left w-full [&_li]:mb-1 mt-2">

- **Não desperdiçar ligações** — 0,7: 94% das ligações dão certo, mas 109 assinantes ficam sem contato.
- **Não perder assinantes** — 0,2: só 22 escapam, ao custo de 291 ligações.

</div>

<!--
- a tabela no teste serve para analisar o tradeoff. Para fixar o threshold de produção, o certo é estimar as probabilidades no treino com cross_val_predict(pipe, X_tr, y_tr, cv=5, method="predict_proba"), como no capítulo 3 do Hands-On ML, e confirmar no teste uma vez: escolher o threshold pelo teste é o mesmo erro de escolher o C pelo teste.
- o número de ligações é o que o time comercial consegue fazer: o orçamento também escolhe o threshold.
- é a análise do Exercício 2 do TP2, com uma recomendação para cada prioridade.
-->

---
layout: section
---

## Curva **ROC** e AUC
**Comparar classificadores antes de escolher o threshold**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: RocCurveDisplay
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.RocCurveDisplay.html
---

# A curva ROC

#### **Recall contra alarmes falsos, em todos os thresholds de uma vez**

::left::

```python [etapa3.ipynb]
from sklearn.metrics import RocCurveDisplay

num3 = ["idade", "viagens_30d",
        "distancia_media_km"]
simples = make_pipeline(StandardScaler(),
    LogisticRegression()).fit(X_tr[num3], y_tr)

fig, ax = plt.subplots()
RocCurveDisplay.from_estimator(
    pipe, X_te, y_te, ax=ax)
RocCurveDisplay.from_estimator(
    simples, X_te[num3], y_te, ax=ax)
```

<div class="text-left w-full [&_li]:mb-2 mt-4">

- **Vertical** — o recall: VP ÷ (VP + FN).
- **Horizontal** — falsos positivos: FP ÷ (FP + VN).

</div>

::right::

<AssetImg src="pm-roc.png" class="rounded-lg w-full" />

<!--
- cada ponto da curva é um threshold: no canto inferior esquerdo, ninguém recebe ligação; no superior direito, todos recebem.
- a diagonal é o classificador que sorteia: um modelo útil fica acima dela.
- simples é o modelo da etapa 1: só as três numéricas, sem as categóricas e sem a avaliação.
- o mesmo ax põe as duas curvas no mesmo gráfico, como pede o Exercício 3 do TP2; name="..." troca o nome na legenda e plot_chance_level=True desenha a diagonal.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: roc_auc_score
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
---

# AUC: a área sob a curva

#### **Um número para comparar modelos antes de fixar o threshold**

::left::

```python [etapa3.ipynb]
from sklearn.metrics import roc_auc_score

roc_auc_score(y_te, proba)        # 0.864

p_simples = simples.predict_proba(
    X_te[num3])[:, 1]
roc_auc_score(y_te, p_simples)    # 0.825
```

> [!CAUTION]
> Com as previsões 0 ou 1 no lugar das probabilidades, a AUC sai errada.

::right::

<div class="text-left w-full [&_li]:mb-4">

- **De 0,5 a 1** — 0,5 é o acaso; 1 separa todos os assinantes dos demais.
- **O que mede** — a chance de um assinante sorteado receber uma probabilidade maior que a de um não assinante sorteado.
- **Sem threshold** — avalia a ordem dos usuários: serve para escolher o modelo antes do corte.
- **Classe rara** — com poucos positivos, a curva de precisão e recall mostra melhor a diferença entre modelos.

</div>

<!--
- o pipeline completo ordena melhor: 0,864 contra 0,825 do modelo só com as numéricas. A diferença vem das categóricas e da avaliação.
- roc_auc_score(y_te, y_pred), com as previsões 0 ou 1, dá 0,749: a curva vira um ponto só.
- a AUC não substitui a escolha do threshold: dois modelos com a mesma AUC podem ter precisões bem diferentes no corte escolhido.
- Hands-On ML, cap. 3: prefira a curva de precisão e recall quando a classe positiva é rara ou quando os falsos positivos importam mais que os falsos negativos.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: roc_auc_score
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
---

# Demo: a AUC é uma questão de ordem

#### **A AUC conta os pares de usuários na ordem certa**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(1)
pos = rng.normal(1, 1, 300)    # assinantes
neg = rng.normal(0, 1, 700)    # os demais
y = np.r_[np.ones(300), np.zeros(700)]
nota = np.r_[pos, neg]
pares = (pos[:, None] > neg[None, :]).mean()
print("pares na ordem:", round(pares, 3))
print("AUC:", round(roc_auc_score(y, nota), 3))
cubo = roc_auc_score(y, nota ** 3)
print("notas ao cubo:", round(cubo, 3))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Os dados** — notas de 300 assinantes e 700 não assinantes; as dos assinantes são um pouco maiores.
- **Os pares** — cada assinante comparado com cada não assinante: 210.000 pares.
- **Antes de executar** — elevar as notas ao cubo muda a AUC?

</div>

<!--
- saída esperada: 0,753 nas três linhas.
- elevar ao cubo mantém a ordem das notas, e a AUC só depende da ordem: por isso ela aceita qualquer pontuação, não só probabilidades. Na etapa 4, o SVM usa isso.
- pos[:, None] > neg[None, :] monta a tabela 300 × 700 de comparações; a média é a fração de pares na ordem certa.
-->

---
layout: section
---

## Regressão logística: a **sigmoid**
**Como uma combinação linear vira probabilidade**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Logistic regression
source: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
---

# A função sigmoid

#### **Uma nota linear, espremida entre 0 e 1**

::left::

$$
z = b + w_1 x_1 + w_2 x_2 + \dots + w_n x_n
$$

$$
p = \sigma(z) = \frac{1}{1 + e^{-z}}
$$

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **z** — a combinação linear das features: pode ser qualquer número.
- **σ(z)** — a probabilidade de virar assinante, entre 0 e 1.
- **z = 0** — dá p = 0,5: o threshold padrão.

</div>

::right::

<AssetImg src="pm-sigmoid.png" class="rounded-lg w-full" />

<!--
- logit (log das chances): z = ln(p / (1 − p)). Somar 1 ao z multiplica as chances p / (1 − p) por e ≈ 2,72.
- a regressão linear da DR1 devolve o próprio z; a logística passa o z pela sigmoid para obter uma probabilidade.
- os três pontos laranja são os três primeiros usuários do teste: o slide "A sigmoid à mão" refaz essa conta.
- Machine Learning Foundations, cap. 5: a derivação probabilística da regressão logística (chances, log das chances e entropia cruzada).
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: LogisticRegression
source: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
---

# Os coeficientes do modelo

#### **Um peso por coluna transformada, mais o intercepto**

::left::

```python [etapa3.ipynb]
clf = pipe[-1]           # a regressão logística
nomes = pipe[:-1].get_feature_names_out()
coefs = pd.Series(clf.coef_[0], index=nomes)
coefs.sort_values().round(2)
# num__viagens_30d               1.41
# cat__canal_convenio_empresa    0.55
# num__distancia_media_km       -0.01
# cat__canal_loja_de_apps       -0.71
clf.intercept_           # [-1.01]
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Sinal** — as viagens (+1,41) aumentam a chance; vir pela loja de apps (−0,71) diminui.
- **Tamanho** — com as features padronizadas, os pesos são comparáveis: as viagens pesam mais.
- **Chances** — e<sup>1,41</sup> ≈ 4,1: um desvio padrão a mais de viagens multiplica as chances por 4.
- **Perto de zero** — a distância média (−0,01) quase não muda nada.

</div>

<!--
- pipe[-1] é o último passo, a LogisticRegression; pipe[:-1] é o pré-processamento sozinho, já ajustado.
- coef_ tem 13 valores, um por coluna que sai do ColumnTransformer, na ordem do get_feature_names_out(); o trecho mostra 4 dos 13.
- e^coef é a razão de chances (odds ratio), a leitura mais usada em análise de risco.
- confere com o gerar_dados.py: a distância não entra na conta de quem vira assinante.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: predict_proba
source: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
---

# A sigmoid à mão

#### **A probabilidade do predict_proba, refeita com os coeficientes**

::left::

```python [etapa3.ipynb]
import numpy as np

Z = pipe[:-1].transform(X_te.head(3))
z = Z @ clf.coef_[0] + clf.intercept_[0]
p = 1 / (1 + np.exp(-z))
p.round(3)              # [0.171 0.591 0.517]

pipe.predict_proba(X_te.head(3))[:, 1]
# [0.171 0.591 0.517]
```

> [!CAUTION]
> Com o `X_te` cru, de 7 colunas, a conta dá erro de dimensão (`ValueError`).

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`pipe[:-1].transform`** — aplica o pré-processamento: as mesmas 13 colunas do `coef_`.
- **`@`** — soma o produto das 13 colunas pelos 13 pesos; com o intercepto, dá o `z`.
- **Conferência** — as três probabilidades batem com o `predict_proba`.

</div>

<!--
- os z dos três usuários: −1,577; 0,367 e 0,067. O terceiro fica perto do threshold: 0,517.
- se a probabilidade sair levemente diferente do predict_proba, faltou o intercepto ou a ordem das colunas está trocada.
- clf.decision_function(Z) devolve o mesmo z.
- é a demonstração que o Exercício 4 do TP2 pede.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: log_loss
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html
---

# Como o modelo aprende

#### **O fit procura os pesos que dão probabilidade alta ao que aconteceu**

::left::

$$
J(\mathbf{w}) = -\frac{1}{m}\sum_{i=1}^{m}\Big[y_i \ln p_i + (1-y_i)\ln(1-p_i)\Big]
$$

```python [etapa3.ipynb]
from sklearn.dummy import DummyClassifier
from sklearn.metrics import log_loss

ref = DummyClassifier().fit(X_tr, y_tr)
log_loss(y_te, proba)                  # 0.396
log_loss(y_te, ref.predict_proba(X_te)[:, 1])
# 0.598
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Log loss (entropia cruzada)** — pune a probabilidade baixa para o que aconteceu: dar 0,9 a um assinante custa 0,11; dar 0,1 custa 2,30.
- **Regularização** — o `fit` minimiza a log loss mais uma penalidade sobre os pesos, controlada pelo `C`.
- **Probabilidades úteis** — por isso a saída serve para escolher thresholds e ordenar usuários.

</div>

<!--
- −ln(0,9) = 0,105 e −ln(0,1) = 2,303: o erro confiante custa cerca de 22 vezes mais.
- a referência dá 0,285 de probabilidade a todo mundo: log loss de 0,598.
- a penalidade dos pesos ganha nome na etapa 4: Ridge (L2).
- o fit minimiza J com um método numérico (o padrão é o lbfgs); o gradiente descendente está no capítulo 4 do Hands-On ML.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** `usuarios_avulsos.csv` e o `pipeline_assinatura.joblib`, salvos na etapa 2

📏 &nbsp;**Análise:** o pipeline avaliado antes de qualquer ajuste: matriz de confusão, thresholds, curva ROC contra o modelo da etapa 1 e a sigmoid refeita à mão

<!--
Projeto: o mesmo das etapas 1 e 2 (pandas, numpy, scikit-learn e matplotlib). O pipeline_assinatura.py e o pipeline_assinatura.joblib são os da etapa 2: se o .joblib não existir, rode o script antes.

=================================================================
ARQUIVO 1 — etapa3.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. O pipeline da etapa 2, a mesma divisão e a acurácia contra a referência
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (RocCurveDisplay, confusion_matrix, f1_score, log_loss,
                             precision_score, recall_score, roc_auc_score)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from pipeline_assinatura import dividir

df = pd.read_csv("usuarios_avulsos.csv")
X_tr, X_te, y_tr, y_te = dividir(df)
pipe = joblib.load("pipeline_assinatura.joblib")
ref = DummyClassifier().fit(X_tr, y_tr)
pipe.score(X_te, y_te), ref.score(X_te, y_te)

# 2. Matriz de confusão do pipeline e da referência
y_pred = pipe.predict(X_te)
vn, fp, fn, vp = confusion_matrix(y_te, y_pred).ravel()
confusion_matrix(y_te, y_pred), confusion_matrix(y_te, ref.predict(X_te))

# 3. Precisão, recall e F1 no threshold padrão (0,5)
precision_score(y_te, y_pred), recall_score(y_te, y_pred), f1_score(y_te, y_pred)

# 4. Tabela de thresholds: ligações, precisão, recall e assinantes sem ligação
proba = pipe.predict_proba(X_te)[:, 1]
linhas = []
for t in [0.2, 0.3, 0.5, 0.7]:
    prev = (proba >= t).astype(int)
    linhas.append({"threshold": t, "ligacoes": prev.sum(),
                   "precisao": precision_score(y_te, prev), "recall": recall_score(y_te, prev),
                   "sem_ligacao": ((prev == 0) & (y_te == 1)).sum()})
pd.DataFrame(linhas).round(3)

# 5. Curva ROC e AUC: o pipeline contra o modelo das três numéricas da etapa 1
num3 = ["idade", "viagens_30d", "distancia_media_km"]
simples = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_tr[num3], y_tr)
fig, ax = plt.subplots()
RocCurveDisplay.from_estimator(pipe, X_te, y_te, ax=ax, name="pipeline da etapa 2")
RocCurveDisplay.from_estimator(simples, X_te[num3], y_te, ax=ax, name="só as três numéricas",
                               plot_chance_level=True)
plt.show()
roc_auc_score(y_te, proba), roc_auc_score(y_te, simples.predict_proba(X_te[num3])[:, 1])

# 6. Os coeficientes do modelo, com os nomes das colunas transformadas
clf = pipe[-1]
coefs = pd.Series(clf.coef_[0], index=pipe[:-1].get_feature_names_out())
coefs.sort_values(), clf.intercept_

# 7. A sigmoid à mão para três usuários, comparada com o predict_proba
Z = pipe[:-1].transform(X_te.head(3))
z = Z @ clf.coef_[0] + clf.intercept_[0]
1 / (1 + np.exp(-z)), pipe.predict_proba(X_te.head(3))[:, 1]

# 8. Log loss do pipeline e da referência
log_loss(y_te, proba), log_loss(y_te, ref.predict_proba(X_te)[:, 1])

# 9. Recomendação (markdown): um threshold para cada prioridade do time comercial
```

>>> Resultados esperados: acurácia 0,832 no teste, contra 0,715 da referência.
>>> Matriz do pipeline [[404, 25], [76, 95]] (VN 404, FP 25, FN 76, VP 95); da referência [[429, 0], [171, 0]].
>>> Threshold 0,5: precisão 0,792, recall 0,556, F1 0,653.
>>> Thresholds (ligações, precisão, recall, sem ligação): 0,2 → 291, 0,512, 0,871, 22; 0,3 → 212, 0,608, 0,754, 42; 0,5 → 120, 0,792, 0,556, 76; 0,7 → 66, 0,939, 0,363, 109.
>>> AUC: 0,864 do pipeline e 0,825 do modelo só com as três numéricas.
>>> Coeficientes: viagens_30d 1,409; canal_convenio_empresa 0,553; avaliacao_media 0,470; regiao_centro 0,355; idade −0,397; canal_loja_de_apps −0,709; distancia_media_km −0,014; intercepto −1,009.
>>> Sigmoid à mão: z = −1,577, 0,367 e 0,067 → 0,171, 0,591 e 0,517, iguais ao predict_proba.
>>> Log loss: 0,396 do pipeline e 0,598 da referência.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para avaliar o pipeline de assinaturas e escolher o threshold**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um engenheiro de machine learning especialista em avaliação de classificadores.

# Tarefa
Avalie, sem retreinar, o pipeline que prevê se um usuário avulso vira
assinante e recomende um threshold para o time comercial.

# Contexto
1. Em "etapa3.ipynb", carregue @pipeline_assinatura.joblib e refaça a divisão
   com a função dividir de @pipeline_assinatura.py.
2. Monte a matriz de confusão no teste e nomeie VN, FP, FN e VP.
3. Calcule precisão, recall e F1 no threshold 0.5.
4. Monte uma tabela com os thresholds 0.2, 0.3, 0.5 e 0.7: ligações,
   precisão, recall e assinantes sem ligação.
5. Num mesmo gráfico ROC, compare o pipeline com uma regressão logística só
   com idade, viagens_30d e distancia_media_km, e calcule as duas AUCs.
6. Refaça à mão, com coef_, intercept_ e a sigmoid, a probabilidade dos três
   primeiros usuários do teste e compare com o predict_proba.
7. Antes de cada passo, crie uma célula de markdown explicando o passo.

# Saída e Verificação
- Execute o notebook do início ao fim, sem erros.
- No fim, recomende um threshold para cada prioridade: poucas ligações
  desperdiçadas ou poucos assinantes sem ligação.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: confira se o agente não retreinou o pipeline nem dividiu os dados de outro jeito; a matriz precisa somar 600.

# 2 - se a tabela usar o predict no lugar do predict_proba, todos os thresholds dão o mesmo resultado: é a deixa para mostrar a diferença.

# 3 - se a AUC vier das previsões 0 ou 1, o número cai para 0,749: a AUC precisa das probabilidades.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** Recarregue o pipeline do Titanic da etapa 2 e monte a matriz de confusão no teste.

🛠️ &nbsp;**Exercício \#2:** Calcule precisão, recall e sobreviventes previstos com os thresholds 0,3, 0,5 e 0,7.

🛠️ &nbsp;**Exercício \#3:** Compare pela AUC o pipeline e um modelo só com `sex` e `pclass`.

🛠️ &nbsp;**Exercício \#4:** Calcule à mão, com a sigmoid, a probabilidade de três passageiros do teste.

- [ ] ler a matriz com a classe real nas linhas
- [ ] dizer o que cada célula significa no problema
- [ ] aplicar os thresholds sobre o `predict_proba`, não sobre o `predict`
- [ ] comparar os modelos pela AUC antes de escolher o threshold
- [ ] calcular a sigmoid sobre as features transformadas pelo pipeline

<br/>

<!--
# Exercício #1 — Matriz de confusão
O pipeline do Exercício 4 da etapa 2 (sete colunas, C = 10), com a mesma divisão estratificada (test_size=0.2, random_state=42): acurácia 0,804 no teste, que tem 179 passageiros, 69 sobreviventes.
Matriz [[98, 12], [23, 46]]: VN 98, FP 12, FN 23 (sobreviventes que o modelo deu como mortos), VP 46. Precisão 0,793, recall 0,667, F1 0,724.

# Exercício #2 — Thresholds
0,3 → precisão 0,671, recall 0,797, 82 previstos (14 FN); 0,5 → 0,793, 0,667, 58 (23 FN); 0,7 → 0,897, 0,507, 39 (34 FN).

# Exercício #3 — ROC e AUC
AUC 0,843 do pipeline contra 0,822 do modelo só com sex e pclass (OneHotEncoder nas duas, sem as numéricas): o sexo e a classe já explicam quase tudo. Só com as quatro numéricas, a AUC cai para 0,664.

# Exercício #4 — Sigmoid à mão
pipe[:-1].transform(X_te.head(3)) tem 12 colunas. Os três primeiros do teste são homens da terceira classe: z = −2,695, −3,082 e −1,736 → 0,063, 0,044 e 0,150, iguais ao predict_proba.
Pesos de destaque: sex_female 1,41, sex_male −1,27, pclass_1 1,12, pclass_3 −1,11, age −0,51.

## os exercícios preparam os Exercícios 1 a 4 do TP2
-->
