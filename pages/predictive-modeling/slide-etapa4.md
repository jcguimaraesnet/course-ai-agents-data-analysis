---
layout: section
routeAlias: etapa4
---

## **Etapa 4:** Classificadores Avançados em IA

---
layout: section
---

## Regressão logística **multiclasse**
**Uma probabilidade para cada classe**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Multiclass
source: https://scikit-learn.org/stable/modules/multiclass.html
---

# Três classes: o motivo de uso

#### **Prever o motivo de quem pulou essa pergunta no cadastro**

::left::

```python [etapa4.ipynb]
df = pd.read_csv("usuarios_avulsos.csv").merge(
    pd.read_csv("motivos_uso.csv"), on="usuario_id")
com = df.dropna(subset=["motivo_uso"])
num3 = ["idade", "viagens_30d",
        "distancia_media_km"]
Xm_tr, Xm_te, ym_tr, ym_te = train_test_split(
    com[num3], com["motivo_uso"], test_size=0.2,
    stratify=com["motivo_uso"], random_state=42)
modelo = make_pipeline(StandardScaler(),
    LogisticRegression()).fit(Xm_tr, ym_tr)
modelo.score(Xm_te, ym_te)    # 0.663
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **O alvo** — o motivo declarado no cadastro: lazer (49%), trabalho (33%) ou estudo (18%).
- **O uso** — preencher o motivo dos 303 usuários que pularam a pergunta.
- **Resultado** — 66,3% no teste, contra 48,9% de responder sempre "lazer".
- **O código** — o mesmo do caso binário: o `LogisticRegression` percebe as três classes sozinho.

</div>

<!--
- o motivos_uso.csv sai do trecho que esta etapa acrescenta ao gerar_dados.py (notas do Live Coding); o usuarios_avulsos.csv não muda.
- o merge é o da DR1: junta as duas tabelas pela chave usuario_id.
- as features são as três numéricas sem ausentes da etapa 1; os nomes com m (Xm_tr, ym_tr) separam este problema do de assinatura, que continua em X_tr e y_tr.
- a referência: DummyClassifier().fit(Xm_tr, ym_tr).score(Xm_te, ym_te) dá 0,489.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Hands-On ML, cap. 4
source: https://github.com/ageron/handson-mlp/blob/main/04_training_linear_models.ipynb
---

# A função softmax

#### **Uma nota linear por classe, transformada em probabilidades que somam 1**

::left::

$$
p_k = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}
$$

```python [etapa4.ipynb]
clf = modelo[-1]
clf.classes_    # ['estudo' 'lazer' 'trabalho']
clf.coef_.shape          # (3, 3): classe × feature
modelo.predict_proba(Xm_te.head(1)).round(3)
# [[0.102 0.27  0.629]] → trabalho
```

> [!CAUTION]
> O `multi_class` de material antigo dá `TypeError` desde o scikit-learn 1.8: a softmax já é o padrão.

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Uma linha de pesos por classe** — cada classe calcula o seu `z`: o do estudo cai com a idade.
- **Softmax** — transforma as três notas em probabilidades que somam 1; a previsão é a maior.
- **Com duas classes** — a softmax vira a sigmoid da etapa 3.

</div>

<!--
- o primeiro usuário do teste (30 anos, 7 viagens, 0,8 km) tem z = −0,93, 0,04 e 0,89 para estudo, lazer e trabalho: 0,102, 0,270 e 0,629.
- coeficientes de destaque: idade −1,58 no estudo; viagens +0,56 e idade +0,97 no trabalho; distância +0,68 no lazer.
- a regressão softmax (ou multinomial) está no capítulo 4 do Hands-On ML; a derivação, no capítulo 5 do Machine Learning Foundations.
- o parâmetro multi_class foi descontinuado na versão 1.5 e removido na 1.8.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: classification_report
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
---

# Avaliando cada classe

#### **A acurácia geral esconde a classe que o modelo mais erra**

::left::

```python [etapa4.ipynb]
from sklearn.metrics import classification_report

ym_pred = modelo.predict(Xm_te)
print(classification_report(ym_te, ym_pred))
```

| | precisão | recall | f1 | casos |
|---|---|---|---|---|
| estudo | 0,70 | 0,62 | 0,66 | 99 |
| lazer | 0,69 | 0,75 | 0,72 | 264 |
| trabalho | 0,60 | 0,56 | 0,58 | 177 |

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Uma linha por classe** — cada classe é a positiva da vez, contra as outras duas.
- **Pior classe** — trabalho: recall de 0,56. O modelo confunde trabalho com lazer.
- **`macro avg`** — a média simples das classes (f1 de 0,65): cada classe pesa igual, grande ou pequena.

</div>

<!--
- confusion_matrix(ym_te, ym_pred, labels=["lazer", "trabalho", "estudo"]) dá [[197 54 13] [64 100 13] [26 12 61]]: 64 usuários de trabalho previstos como lazer.
- weighted avg pondera cada classe pelo número de casos.
- preencher os 303 sem motivo: modelo.predict(df[df["motivo_uso"].isna()][num3]) → 155 lazer, 91 trabalho e 57 estudo.
- é o que o Exercício 5 do TP2 pede: relatório por classe, comparação com a referência e a pior classe.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Hands-On ML, cap. 4
source: https://github.com/ageron/handson-mlp/blob/main/04_training_linear_models.ipynb
---

# Demo: da sigmoid à softmax

#### **A softmax só olha as diferenças entre as notas**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()

z = np.array([2.0, 1.0, -1.0])  # uma por classe
print(softmax(z).round(3))
print(softmax(z + 10).round(3))  # somar 10
z2 = np.array([1.5, 0.0])        # duas classes
print(softmax(z2).round(3))
print(round(1 / (1 + np.exp(-1.5)), 3))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Três classes** — as notas 2, 1 e −1 viram probabilidades.
- **Somar 10 a todas** — muda alguma coisa?
- **Duas classes** — as notas 1,5 e 0, comparadas com a sigmoid de 1,5.
- **Antes de executar** — qual classe fica com mais da metade da probabilidade?

</div>

<!--
- saída esperada: [0,705 0,259 0,035] duas vezes; [0,818 0,182] e 0,818.
- somar o mesmo valor a todas as notas não muda nada: só as diferenças importam. Por isso a função subtrai o máximo antes do exp, o que evita estouro numérico (np.exp(1000) é infinito).
- com duas classes, a softmax de [z, 0] é a sigmoid de z: a regressão logística binária é um caso particular.
-->

---
layout: section
---

## Regularização **Ridge** e curvas de aprendizado
**Falta dado ou falta modelo?**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Logistic regression
source: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
---

# Ridge: a penalidade L2

#### **O C das etapas 1 e 2 controla a força dessa penalidade**

::left::

$$
J(\mathbf{w}) = \text{log loss} + \frac{\lVert \mathbf{w} \rVert^2}{2\,m\,C}
$$

```python [etapa4.ipynb]
X_tr, X_te, y_tr, y_te = dividir(df)  # etapa 2
for C in [0.001, 0.01, 1]:
    p = montar_pipeline().set_params(clf__C=C)
    p.fit(X_tr, y_tr)
    print(C, np.abs(p[-1].coef_).max().round(2))
# 0.001 0.35 | 0.01 1.01 | 1 1.49
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Ridge (L2)** — soma o quadrado dos pesos ao custo da etapa 3: pesos grandes custam caro.
- **`penalty="l2"`** — o padrão do `LogisticRegression`; o `C` é o inverso da força.
- **Efeito** — com `C = 0,001`, nenhum peso passa de 0,35; com `C = 1`, o das viagens chega a 1,49.
- **Lasso (L1)** — `penalty="l1"` leva pesos a zero e funciona como seleção de features.

</div>

<!--
- m é o número de exemplos de treino; a fórmula é a do guia do scikit-learn, com a log loss como média.
- a penalidade não inclui o intercepto.
- na regressão linear, a mesma penalidade dá a Ridge do scikit-learn, cujo alpha faz o papel inverso do C.
- set_params(clf__C=C) troca o C dentro do pipeline, com o prefixo do passo, como na grade do GridSearchCV.
- a L1 exige um solver compatível (liblinear ou saga).
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: learning_curve
source: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html
---

# Curvas de aprendizado

#### **O desempenho conforme o treino cresce, medido com validação cruzada**

::left::

```python [etapa4.ipynb]
from sklearn.model_selection import learning_curve

for C in [0.001, 0.01, 1]:
    tam, treino, valid = learning_curve(
        montar_pipeline().set_params(clf__C=C),
        X_tr, y_tr, cv=5,
        train_sizes=np.linspace(0.1, 1, 5))
    print(C, valid.mean(axis=1).round(3))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`train_sizes`** — de 10% a 100% do treino de cada fold: de 192 a 1.920 usuários.
- **Duas curvas** — a nota no próprio treino e na validação, em cada tamanho.
- **A pergunta** — se a validação ainda sobe no fim, mais dados ajudam; se as curvas já se encontraram, não.

</div>

<!--
- treino e valid têm uma linha por tamanho e uma coluna por fold: a média é por linha (axis=1).
- LearningCurveDisplay.from_estimator(...) desenha o gráfico direto.
- o X_tr da etapa 2 tem 2.400 usuários; com cv=5, cada treino tem no máximo 1.920.
- é o diagnóstico do Exercício 6 do TP2: decidir entre coletar mais dados e mexer no modelo.
-->

---
layout: default
sourceLabel: Learning curve
source: https://scikit-learn.org/stable/modules/learning_curve.html
---

# Lendo as curvas de aprendizado

#### **Treino e validação do pipeline de assinatura com três valores de C**

<AssetImg src="pm-curvas-aprendizado.png" class="rounded-lg w-5/6 mx-auto block" />

<div class="text-left w-full [&_li]:mb-1 mt-2">

- **`C = 0,001`** — as curvas na altura da referência: bias alto, e mais dados não ajudam.
- **`C = 0,01`** — a validação ainda sobe no fim (0,796): mais dados ajudariam um pouco.
- **`C = 1`** — as curvas se encontram em 0,81: quem limita é o modelo, não os dados.

</div>

<!--
- validação média com 192, 624, 1.056, 1.488 e 1.920 usuários: C = 0,001 → 0,715 a 0,722; C = 0,01 → 0,716 a 0,796; C = 1 → 0,781 a 0,810.
- no C = 0,001, o treino cai conforme os dados crescem: com poucos exemplos é fácil acertar o treino, e o modelo regularizado demais não acompanha os novos.
- um modelo com variância alta mostraria o treino bem acima da validação, com a distância diminuindo conforme os dados crescem.
- com C = 1, melhorar exige outra coisa: features novas ou um modelo diferente.
-->

---
layout: section
---

## SVM: **margem máxima**
**A fronteira mais afastada das duas classes**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: SVM: maximum margin
source: https://scikit-learn.org/stable/auto_examples/svm/plot_separating_hyperplane.html
---

# A maior margem

#### **Entre as retas que separam as classes, o SVM escolhe a mais afastada de ambas**

::left::

<AssetImg src="pm-svm-margem.png" class="rounded-lg w-full" />

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Margem** — a faixa entre as linhas tracejadas: o SVM a deixa a mais larga possível.
- **Vetores de suporte** — os pontos na borda da margem (circulados): só eles definem a fronteira.
- **Regressão logística** — usa todos os pontos: mexer num ponto longe da fronteira ainda muda a reta.
- **Escala** — a margem é uma distância: padronize as features antes.

</div>

<!--
- os 40 pontos são do exemplo de margem máxima do scikit-learn (make_blobs, random_state=6): os mesmos da demo seguinte.
- margem rígida (hard margin): nenhum ponto dentro da faixa. Só existe quando as classes são linearmente separáveis.
- com features em escalas diferentes (idade em anos e renda em reais), a margem é dominada pela de maior escala: por isso o StandardScaler vem antes do SVC.
- Hands-On ML, apêndice C, e Machine Learning Foundations, cap. 11.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: SVC
source: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
---

# SVC linear no scikit-learn

#### **Um protótipo separável: usuários de perfil bem definido**

::left::

```python [etapa4.ipynb]
from sklearn.svm import SVC

assinou = df["virou_assinante"] == 1
v, idade = df["viagens_30d"], df["idade"]
perfil = (assinou & (v >= 9) & (idade <= 30)) | (
    ~assinou & (v <= 4) & (idade >= 36))
Xp = df.loc[perfil, ["viagens_30d", "idade"]]
yp = df.loc[perfil, "virou_assinante"]
svm = make_pipeline(StandardScaler(),
    SVC(kernel="linear", C=1000)).fit(Xp, yp)
svm[-1].n_support_          # [1 1]
Xp.iloc[svm[-1].support_]   # (4, 36) e (9, 30)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **O protótipo** — 499 usuários de perfis opostos, separáveis por uma reta.
- **`C=1000`** — um `C` alto quase não tolera erros: aproxima a margem rígida.
- **2 vetores de suporte** — dos 499 pontos, só as duas "quinas" definem a fronteira.
- **`support_`** — os índices dos vetores; os `support_vectors_` vêm padronizados.

</div>

<!--
- o protótipo tem 106 assinantes e 393 não assinantes; a acurácia no treino é 1,0.
- os vetores: 4 viagens e 36 anos (não assinou) e 9 viagens e 30 anos (assinou).
- para desenhar: DecisionBoundaryDisplay.from_estimator(svm, Xp, response_method="decision_function", plot_method="contour", levels=[-1, 0, 1]) e os pontos de Xp.iloc[svm[-1].support_] circulados (código nas notas do Live Coding).
- é o mesmo caminho do Exercício 7 do TP2: um recorte separável antes dos dados reais.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Hands-On ML, apêndice C
source: https://github.com/ageron/handson-mlp/blob/main/Appendix_C_support_vector_machines.ipynb
---

# Demo: só os vetores de suporte importam

#### **Tire pontos longe da margem e veja se a fronteira muda**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.svm import SVC
X, y = make_blobs(40, centers=2, random_state=6)
svm = SVC(kernel="linear", C=1000).fit(X, y)
print("vetores de suporte:", svm.support_)
print("original:", svm.coef_.round(3))
comuns = np.setdiff1d(range(40), svm.support_)
testes = {"sem 20 comuns": comuns[:20],
          "sem 1 vetor": svm.support_[:1]}
for nome, fora in testes.items():
    m = SVC(kernel="linear", C=1000).fit(
        np.delete(X, fora, 0), np.delete(y, fora))
    print(f"{nome}:", m.coef_.round(3))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Os dados** — os 40 pontos do gráfico da margem.
- **`coef_`** — os pesos da fronteira: se não mudam, a reta é a mesma.
- **Antes de executar** — o que muda mais: tirar 20 pontos comuns ou tirar 1 vetor de suporte?

</div>

<!--
- saída esperada: vetores de suporte [16 21 30]; original [[-0,254 -0,838]]; sem 20 comuns, o mesmo; sem 1 vetor, [[-0,161 -0,773]].
- 20 pontos fora da margem saem e nada muda; um único vetor de suporte sai e a fronteira se move.
- na regressão logística, os dois testes mudariam os coeficientes: todos os pontos entram na log loss.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: SVM margins
source: https://scikit-learn.org/stable/auto_examples/svm/plot_svm_margin.html
---

# Soft margin: o C do SVM

#### **Com as classes misturadas, o C decide quanto custa invadir a margem**

::left::

```python [etapa4.ipynb]
X2 = X_tr[["viagens_30d", "idade"]]
for C in [0.001, 0.01, 1]:
    m = make_pipeline(StandardScaler(),
        SVC(kernel="linear", C=C))
    nota = cross_val_score(m, X2, y_tr, cv=5)
    m.fit(X2, y_tr)
    print(C, m[-1].n_support_.sum(),
          nota.mean().round(3))
# 0.001 1366 0.715
# 0.01  1281 0.774
# 1     1208 0.781
```

::right::

<AssetImg src="pm-svm-c.png" class="rounded-lg w-full" />

<div class="text-left w-full [&_li]:mb-1 mt-1">

- **`C` pequeno** — margem larga, mais vetores: bias.
- **`C` grande** — margem estreita: variância.

</div>

<!--
- com todos os 2.400 usuários do treino, as classes se misturam: não existe reta sem erros.
- com C = 0,001, 1.366 vetores: a margem engole quase todos os pontos, e a nota cai para a referência (0,715).
- mais vetores de suporte não é sinal de modelo melhor: é sinal de margem mais larga.
- é o mesmo C da regressão logística: o inverso da força da regularização. Com C alto e classes misturadas, o treino fica lento.
- o gráfico usa dados sintéticos: 80 pontos, com 29 vetores de suporte para C = 0,01 e 3 para C = 100.
-->

---
layout: section
---

## Kernel **RBF**
**Fronteiras curvas sem criar features à mão**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Kernel functions
source: https://scikit-learn.org/stable/modules/svm.html#kernel-functions
---

# O truque do kernel

#### **O SVM compara cada ponto com os vetores de suporte por uma medida de semelhança**

::left::

$$
K(\mathbf{x}, \mathbf{x}') = e^{-\gamma \lVert \mathbf{x} - \mathbf{x}' \rVert^2}
$$

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **Semelhança** — 1 para pontos iguais, perto de 0 para pontos distantes.
- **A fronteira** — uma soma ponderada das semelhanças com os vetores de suporte: pode ser curva.
- **Sem mapeamento explícito** — equivale a trabalhar num espaço de dimensão infinita, sem nunca calculá-lo.

</div>

::right::

<AssetImg src="pm-rbf-gamma.png" class="rounded-lg w-full" />

<!--
- na etapa 1, o PolynomialFeatures criou as 165 colunas de verdade; o kernel faz o efeito de um mapeamento sem criar coluna nenhuma.
- as luas (make_moons, 300 pontos com ruído) não se separam com uma reta: o linear fica em 0,81 no treino e 0,86 no teste.
- γ = 0,1 quase repete a reta; γ = 1 acompanha as luas (0,97 e 0,98); γ = 100 contorna cada ponto (0,99 no treino e 0,91 no teste): overfitting.
- Hands-On ML, apêndice C, e Machine Learning Foundations, cap. 11.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: RBF SVM parameters
source: https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
---

# C e gamma com GridSearchCV

#### **Os dois hiperparâmetros do RBF, escolhidos juntos pela validação cruzada**

::left::

```python [etapa4.ipynb]
grade = {"svc__C": [0.1, 1, 10],
         "svc__gamma": ["scale", 0.1, 1, 10]}
rbf = GridSearchCV(make_pipeline(StandardScaler(),
    SVC(kernel="rbf")), grade, cv=5)
rbf.fit(X2, y_tr)
rbf.best_params_    # C = 1, gamma = 10
rbf.best_score_     # 0.785 (linear: 0.781)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`gamma`** — o alcance de cada ponto: pequeno, fronteira suave; grande, fronteira recortada.
- **`C`** — o mesmo papel do SVC linear: quanto custa errar no treino.
- **Busca conjunta** — 3 × 4 combinações × 5 folds = 60 treinos.
- **Aqui** — o RBF quase empata com o linear: a fronteira verdadeira é quase reta.

</div>

<!--
- "scale", o padrão, usa gamma = 1 / (número de features × variância de X): com o StandardScaler e 2 features, 0,5.
- make_pipeline chama o passo de "svc": daí o prefixo svc__ na grade.
- gamma alto com C alto é a combinação de maior variância: a fronteira decora o treino.
- é o ajuste do Exercício 9 do TP2.
-->

---
layout: section
---

## Qual classificador **vai para produção**?
**As mesmas métricas, no mesmo teste**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Scores and probabilities
source: https://scikit-learn.org/stable/modules/svm.html#scores-and-probabilities
---

# Regressão logística ou SVM?

#### **O SVC entra no mesmo pipeline; a AUC usa a decision_function**

::left::

```python [etapa4.ipynb]
svc = montar_pipeline().set_params(
    clf=SVC(kernel="rbf"))
busca = GridSearchCV(svc, {"clf__C": [0.1, 1, 10]},
                     cv=5).fit(X_tr, y_tr)
nota = busca.decision_function(X_te)
roc_auc_score(y_te, nota)        # 0.819
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **Sem `predict_proba`** — o SVC devolve a distância à fronteira; para a AUC, basta a ordem (demo da etapa 3).
- **O mais complexo não ganhou** — com a relação quase linear, o RBF não tem o que capturar.

</div>

::right::

| | Regressão logística | SVC (RBF) |
|---|---|---|
| acurácia | 0,832 | 0,827 |
| precisão | 0,792 | 0,825 |
| recall | 0,556 | 0,497 |
| AUC | 0,864 | 0,819 |

<div class="text-left w-full [&_li]:mb-3 mt-3">

- **Veredito** — a regressão logística ordena melhor, acha mais assinantes e dá probabilidades para o threshold.

</div>

<!--
- a regressão logística é o pipeline_assinatura.joblib da etapa 2 (C = 0,1); o SVC ficou com C = 1 (validação 0,804, contra 0,811).
- matrizes: regressão logística [[404 25] [76 95]]; SVC [[411 18] [86 85]]: menos alarmes falsos e mais assinantes perdidos.
- busca.predict_proba(X_te) dá AttributeError. SVC(probability=True) calcula probabilidades com uma validação cruzada interna: mais lento, e elas podem discordar do predict.
- a decisão amarra as métricas ao custo da etapa 3: um assinante perdido (FN) custa mais que uma ligação a mais. É a recomendação do Exercício 10 do TP2.
-->

---
layout: section
---

## Do notebook para a **API**
**O pipeline escolhido passa a atender pedidos HTTP**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: FastAPI: request body
source: https://fastapi.tiangolo.com/tutorial/body/
---

# Servindo o pipeline com FastAPI

#### **O contrato da entrada em Pydantic; o modelo carregado uma vez, na subida**

::left::

```python [api.py]
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Previsão de assinatura")
modelo = joblib.load("pipeline_assinatura.joblib")

class Usuario(BaseModel):
    idade: int
    viagens_30d: int
    distancia_media_km: float
    avaliacao_media: float | None = None
    regiao: str
    canal: str
    pagamento: str
```

::right::

```python [api.py]
@app.post("/prever")
def prever(usuario: Usuario):
    X = pd.DataFrame([usuario.model_dump()])
    p = modelo.predict_proba(X)[0, 1]
    return {"probabilidade": round(float(p), 3),
            "ligar": bool(p >= 0.3)}
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **`Usuario`** — o contrato: as sete features, com tipo; a avaliação pode faltar.
- **`/prever`** — monta uma linha com as colunas do treino; `ligar` usa o threshold 0,3 da etapa 3.

</div>

<!--
- a FastAPI é a da DR2; o arquivo .joblib é o da etapa 2, e o servidor o carrega uma vez, na inicialização.
- o joblib.load executa código: o servidor só deve carregar arquivos .joblib gerados pelo próprio time.
- model_dump() transforma o objeto Pydantic num dicionário; [ ... ] faz dele uma lista com um registro, que vira uma linha.
- float(p) e bool(...) convertem os tipos do numpy para tipos que o JSON aceita.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: FastAPI CLI
source: https://fastapi.tiangolo.com/fastapi-cli/
---

# Testando a API

#### **Um pedido HTTP com os dados do usuário; a resposta em JSON**

::left::

```bash
uv add "fastapi[standard]" requests
uv run fastapi dev api.py
```

```python [testar_api.py]
import requests

usuario = {"idade": 26, "viagens_30d": 7,
           "distancia_media_km": 1.4,
           "avaliacao_media": 4.2,
           "regiao": "zona_sul",
           "canal": "indicacao",
           "pagamento": "cartao"}
r = requests.post("http://127.0.0.1:8000/prever",
                  json=usuario)
print(r.status_code, r.json())
# 200 {'probabilidade': 0.591, 'ligar': True}
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`fastapi dev`** — sobe o servidor em `127.0.0.1:8000` e recarrega a cada mudança no código.
- **`/docs`** — a documentação gerada pela FastAPI, com um formulário para testar o `/prever`.
- **Validação** — sem a idade, ou com texto no lugar do número, a resposta é 422, antes do modelo.

</div>

<!--
- rode o servidor num terminal e o teste em outro: uv run python testar_api.py.
- o usuário do teste é o segundo do X_te da etapa 3: 0,591, a mesma probabilidade do usuário 2 no slide da sigmoid.
- sem a "avaliacao_media", a resposta continua 0,591: o SimpleImputer preenche com a mediana do treino, 4,2, a mesma nota desse usuário.
- com um canal novo ("parceiro_novo"), a resposta sai normalmente (0,553): é o handle_unknown="ignore" da etapa 2.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** `usuarios_avulsos.csv`, o novo `motivos_uso.csv` e o `pipeline_assinatura.joblib` da etapa 2

🧭 &nbsp;**Análise:** o motivo de uso com a softmax, as curvas de aprendizado, o SVM do protótipo ao kernel RBF, a comparação final e o pipeline servido por uma API

<!--
Projeto: o mesmo das etapas anteriores. Para a API: uv add "fastapi[standard]" requests

=================================================================
ARQUIVO 1 — acrescentar ao final do gerar_dados.py (e rodar de novo: o usuarios_avulsos.csv sai igual, e o motivos_uso.csv é novo)

```python

# motivo de uso declarado no cadastro (etapa 4): os mais jovens usam para estudar, quem viaja mais
# usa para trabalhar e as viagens longas são de lazer; 10% pularam a pergunta
MOTIVOS = ["lazer", "trabalho", "estudo"]
pontos = np.column_stack([
    0.45 * distancia_media_km,                                # lazer
    -1.2 + 0.35 * viagens_30d + 0.03 * (idade - 31),          # trabalho
    1.5 - 0.22 * (idade - 22) - 0.2 * distancia_media_km,     # estudo
])
prob = np.exp(pontos) / np.exp(pontos).sum(axis=1, keepdims=True)
motivo_uso = pd.Series([rng.choice(MOTIVOS, p=p) for p in prob])
motivo_uso[rng.random(n) < 0.10] = np.nan
pd.DataFrame({"usuario_id": df["usuario_id"], "motivo_uso": motivo_uso}).to_csv("motivos_uso.csv", index=False)
```

=================================================================
ARQUIVO 2 — etapa4.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Motivo de uso: três classes, divisão estratificada e a regressão logística com softmax
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import GridSearchCV, cross_val_score, learning_curve, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from pipeline_assinatura import dividir, montar_pipeline

df = pd.read_csv("usuarios_avulsos.csv").merge(pd.read_csv("motivos_uso.csv"), on="usuario_id")
com = df.dropna(subset=["motivo_uso"])
num3 = ["idade", "viagens_30d", "distancia_media_km"]
Xm_tr, Xm_te, ym_tr, ym_te = train_test_split(com[num3], com["motivo_uso"], test_size=0.2,
                                              stratify=com["motivo_uso"], random_state=42)
modelo = make_pipeline(StandardScaler(), LogisticRegression()).fit(Xm_tr, ym_tr)
modelo.score(Xm_te, ym_te), DummyClassifier().fit(Xm_tr, ym_tr).score(Xm_te, ym_te)

# 2. A softmax à mão para o primeiro usuário do teste, comparada com o predict_proba
z = modelo[-1].decision_function(modelo[:-1].transform(Xm_te.head(1)))
np.exp(z) / np.exp(z).sum(), modelo.predict_proba(Xm_te.head(1))

# 3. O relatório por classe e o motivo de quem pulou a pergunta
print(classification_report(ym_te, modelo.predict(Xm_te)))
sem = df[df["motivo_uso"].isna()]
pd.Series(modelo.predict(sem[num3])).value_counts()

# 4. Curvas de aprendizado do pipeline da etapa 2 com três valores de C (Ridge)
X_tr, X_te, y_tr, y_te = dividir(df)
fig, eixos = plt.subplots(1, 3, figsize=(12, 3.5), sharey=True)
for ax, C in zip(eixos, [0.001, 0.01, 1]):
    tam, treino, valid = learning_curve(montar_pipeline().set_params(clf__C=C), X_tr, y_tr, cv=5,
                                        train_sizes=np.linspace(0.1, 1, 5))
    ax.plot(tam, treino.mean(axis=1), "o-", label="treino")
    ax.plot(tam, valid.mean(axis=1), "o-", label="validação")
    ax.set_title(f"C = {C}")
eixos[0].legend()
plt.show()

# 5. SVM de margem máxima num protótipo separável: fronteira, margens e vetores de suporte
assinou = df["virou_assinante"] == 1
v, idade = df["viagens_30d"], df["idade"]
perfil = (assinou & (v >= 9) & (idade <= 30)) | (~assinou & (v <= 4) & (idade >= 36))
Xp, yp = df.loc[perfil, ["viagens_30d", "idade"]], df.loc[perfil, "virou_assinante"]
svm = make_pipeline(StandardScaler(), SVC(kernel="linear", C=1000)).fit(Xp, yp)
vetores = Xp.iloc[svm[-1].support_]
disp = DecisionBoundaryDisplay.from_estimator(svm, Xp, response_method="decision_function",
                                              plot_method="contour", levels=[-1, 0, 1],
                                              linestyles=["--", "-", "--"], colors="gray")
disp.ax_.scatter(Xp["viagens_30d"], Xp["idade"], c=yp, cmap="coolwarm", s=15)
disp.ax_.scatter(vetores["viagens_30d"], vetores["idade"], s=150, facecolors="none", edgecolors="k")
plt.show()
svm[-1].n_support_, vetores

# 6. Soft margin: o C do SVC linear com todos os usuários do treino
X2 = X_tr[["viagens_30d", "idade"]]
for C in [0.001, 0.01, 1]:
    m = make_pipeline(StandardScaler(), SVC(kernel="linear", C=C))
    nota = cross_val_score(m, X2, y_tr, cv=5).mean()
    print(C, m.fit(X2, y_tr)[-1].n_support_.sum(), round(nota, 3))

# 7. Kernel RBF: C e gamma com GridSearchCV
grade = {"svc__C": [0.1, 1, 10], "svc__gamma": ["scale", 0.1, 1, 10]}
rbf = GridSearchCV(make_pipeline(StandardScaler(), SVC(kernel="rbf")), grade, cv=5).fit(X2, y_tr)
rbf.best_params_, rbf.best_score_

# 8. Regressão logística ou SVM: o SVC com kernel RBF no pipeline completo
lr = joblib.load("pipeline_assinatura.joblib")
svc = GridSearchCV(montar_pipeline().set_params(clf=SVC(kernel="rbf")), {"clf__C": [0.1, 1, 10]},
                   cv=5).fit(X_tr, y_tr)
for nome, m, nota in [("regressão logística", lr, lr.predict_proba(X_te)[:, 1]),
                      ("SVC RBF", svc, svc.decision_function(X_te))]:
    prev = m.predict(X_te)
    print(nome, m.score(X_te, y_te), confusion_matrix(y_te, prev).ravel(),
          precision_score(y_te, prev), recall_score(y_te, prev), roc_auc_score(y_te, nota))

# 9. Recomendação (markdown): qual modelo vai para produção e por quê
```

=================================================================
ARQUIVO 3 — api.py (o pipeline escolhido, servido com FastAPI: uv run fastapi dev api.py)

```python
"""API de previsão de assinatura: recebe um usuário avulso e devolve a probabilidade."""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Previsão de assinatura")
# o joblib.load executa código ao carregar: só o arquivo gerado pelo próprio time, na etapa 2
modelo = joblib.load("pipeline_assinatura.joblib")


class Usuario(BaseModel):
    idade: int
    viagens_30d: int
    distancia_media_km: float
    avaliacao_media: float | None = None
    regiao: str
    canal: str
    pagamento: str


@app.post("/prever")
def prever(usuario: Usuario):
    X = pd.DataFrame([usuario.model_dump()])
    p = modelo.predict_proba(X)[0, 1]
    return {"probabilidade": round(float(p), 3), "ligar": bool(p >= 0.3)}
```

=================================================================
ARQUIVO 4 — testar_api.py (com o servidor no ar, em outro terminal: uv run python testar_api.py)

```python
import requests

usuario = {"idade": 26, "viagens_30d": 7, "distancia_media_km": 1.4, "avaliacao_media": 4.2,
           "regiao": "zona_sul", "canal": "indicacao", "pagamento": "cartao"}
r = requests.post("http://127.0.0.1:8000/prever", json=usuario)
print(r.status_code, r.json())
```

>>> Resultados esperados: motivos_uso.csv com 3.000 linhas, 303 sem motivo; dos 2.697 com motivo, 48,8% lazer, 32,8% trabalho e 18,4% estudo. Treino 2.157 e teste 540.
>>> Motivo de uso: 0,663 no teste, contra 0,489 da referência. Softmax do primeiro usuário do teste [0,102 0,270 0,629] (estudo, lazer, trabalho), igual ao predict_proba.
>>> classification_report: estudo 0,70 / 0,62 / 0,66; lazer 0,69 / 0,75 / 0,72; trabalho 0,60 / 0,56 / 0,58 (precisão, recall e f1; a pior classe é trabalho). Os 303 sem motivo: 155 lazer, 91 trabalho e 57 estudo.
>>> Curvas de aprendizado (validação, de 192 a 1.920 usuários): C = 0,001 → 0,715 a 0,722 (bias alto); C = 0,01 → 0,716 a 0,796 (ainda subindo); C = 1 → 0,781 a 0,810 (curvas juntas).
>>> Protótipo: 499 usuários (106 assinantes), 2 vetores de suporte: 4 viagens e 36 anos; 9 viagens e 30 anos.
>>> Soft margin (vetores e validação): C = 0,001 → 1.366 e 0,715; C = 0,01 → 1.281 e 0,774; C = 1 → 1.208 e 0,781.
>>> RBF nas duas features: melhor C = 1 e gamma = 10, validação 0,785.
>>> Comparação no teste: regressão logística 0,832, [404 25 76 95], precisão 0,792, recall 0,556, AUC 0,864; SVC RBF (C = 1) 0,827, [411 18 86 85], precisão 0,825, recall 0,497, AUC 0,819.
>>> API: 200 {'probabilidade': 0.591, 'ligar': True}.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para comparar classificadores e escolher o modelo de produção**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um engenheiro de machine learning especialista em scikit-learn.

# Tarefa
Treine e compare classificadores para a empresa de bicicletas e decida qual
modelo de assinatura vai para produção.

# Contexto
1. Em "etapa4.ipynb", junte @usuarios_avulsos.csv e @motivos_uso.csv pelo
   usuario_id e preveja o motivo_uso (três classes) com StandardScaler e
   LogisticRegression; mostre o classification_report e a referência.
2. Com dividir e montar_pipeline de @pipeline_assinatura.py, gere curvas de
   aprendizado (cv=5) para C = 0.001, 0.01 e 1 e diagnostique cada uma.
3. Num protótipo separável (assinantes com 9 ou mais viagens e até 30 anos,
   não assinantes com até 4 viagens e 36 anos ou mais), treine um SVC linear
   com C=1000 e plote a fronteira, as margens e os vetores de suporte.
4. Troque o classificador do pipeline por um SVC com kernel RBF, busque o C
   com GridSearchCV e compare-o com @pipeline_assinatura.joblib no teste:
   matriz de confusão, precisão, recall e AUC.
5. Antes de cada passo, crie uma célula de markdown explicando o passo.

# Saída e Verificação
- Execute o notebook do início ao fim, sem erros.
- No fim, recomende o modelo para produção com os números do teste.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: se o agente escrever multi_class="multinomial", o código quebra no scikit-learn 1.8 ou mais novo: a softmax já é o padrão.

# 2 - confira se o SVC vem depois do StandardScaler e se os vetores de suporte foram marcados pelos índices do support_, não pelos support_vectors_ padronizados.

# 3 - se o agente chamar predict_proba no SVC, vem o AttributeError: a AUC sai da decision_function.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** Nos pinguins, preveja a espécie pela nadadeira e pela massa e ache a pior classe.

🛠️ &nbsp;**Exercício \#2:** No Titanic, gere curvas de aprendizado com `C` de 0,001, 0,01 e 1 e diagnostique.

🛠️ &nbsp;**Exercício \#3:** Separe Adelie de Gentoo pela altura do bico e pela nadadeira com um `SVC` linear.

🛠️ &nbsp;**Exercício \#4:** No teste, compare a regressão logística do Titanic com um `SVC` de kernel RBF.

- [ ] comparar a acurácia multiclasse com a da classe mais comum
- [ ] trocar o `C` dentro do pipeline com `set_params(clf__C=...)`
- [ ] colocar o `StandardScaler` antes do `SVC`
- [ ] marcar os vetores de suporte pelos índices de `support_`
- [ ] calcular a AUC do `SVC` com a `decision_function`

<br/>

<!--
# Exercício #1 — Softmax nos pinguins
penguins = sns.load_dataset("penguins"): 344 pinguins, 2 sem medidas (342). Features flipper_length_mm e body_mass_g; alvo species; test_size=0.2, stratify, random_state=42 (69 no teste).
make_pipeline(StandardScaler(), LogisticRegression()): 0,768 no teste, contra 0,435 de responder sempre Adelie.
Recall: Adelie 0,83, Chinstrap 0,21 (a pior: 11 dos 14 viram Adelie, que tem o mesmo tamanho), Gentoo 1,00. Com bill_length_mm e bill_depth_mm no lugar, a acurácia vai a 0,942 e o recall do Chinstrap, a 0,86.

# Exercício #2 — Curvas de aprendizado
O pipeline do Titanic da etapa 2, com set_params(clf__C=C), learning_curve(cv=5, train_sizes=np.linspace(0.1, 1, 5)) no treino (de 56 a 569 passageiros).
C = 0,001: treino e validação em 0,62, a referência: bias. C = 0,01: os dois sobem até 0,776 e 0,775: mais dados ajudariam. C = 1: treino 0,807 e validação 0,798, já juntos: mais dados não ajudam.

# Exercício #3 — Margem máxima
Adelie e Gentoo com bill_depth_mm (altura do bico) e flipper_length_mm: 274 pinguins (151 Adelie, 123 Gentoo), separáveis. Com um C alto, como no protótipo da aula, make_pipeline(StandardScaler(), SVC(kernel="linear", C=1000)): acurácia 1,0 com 3 vetores de suporte (Adelie com 18,0 mm de bico e 210 mm de nadadeira; Gentoo com 17,3 e 219 e com 15,7 e 208). Com C = 1, 7 vetores; com C = 0,01, 102.

# Exercício #4 — SVC contra regressão logística
GridSearchCV no pipeline com clf=SVC(kernel="rbf"), C em [0,1, 1, 10] e gamma em ["scale", 0,01, 0,1, 1]: melhor C = 10 e gamma = 0,1, validação 0,827 (a regressão logística tem 0,798).
No teste: SVC 0,799, [[100 10] [26 43]], precisão 0,811, recall 0,623, AUC 0,831; regressão logística 0,804, [[98 12] [23 46]], precisão 0,793, recall 0,667, AUC 0,843. A validação favoreceu o SVC, mas o teste não confirmou: a diferença está dentro da variação entre os folds.

## os exercícios preparam os Exercícios 5 a 10 do TP2
-->
