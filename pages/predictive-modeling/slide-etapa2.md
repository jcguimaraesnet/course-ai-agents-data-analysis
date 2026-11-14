---
layout: section
routeAlias: etapa2
---

## **Etapa 2:** Pipeline e Seleção de Hiperparâmetros

---
layout: section
---

## Divisão **estratificada**
**Treino e teste com a proporção das classes, e sem vazamento**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: train_test_split
source: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
---

# train_test_split estratificado

#### **O teste precisa ter a mesma proporção de classes da base**

::left::

```python [etapa2.ipynb]
from sklearn.model_selection import train_test_split

num = ["idade", "viagens_30d",
       "distancia_media_km", "avaliacao_media"]
cat = ["regiao", "canal", "pagamento"]
X, y = df[num + cat], df["virou_assinante"]

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y,
    random_state=42)
y_tr.mean(), y_te.mean()    # (0.285, 0.285)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Sem `stratify`** — na etapa 1, o teste ficou com 26,8% de positivos e o treino, com 28,9%.
- **Com `stratify=y`** — o sorteio é feito dentro de cada classe, e os dois ficam com 28,5%.
- **Por que importa** — com a classe minoritária pequena, um teste desequilibrado distorce a métrica.

</div>

<!--
- agora o X tem as sete features: quatro numéricas (avaliacao_media com 230 ausentes) e três categóricas. O usuario_id fica de fora: só identifica a linha.
- confira com y_tr.value_counts(normalize=True) e y_te.value_counts(normalize=True).
- no livro (Hands-On ML, cap. 2), a estratificação é por faixas de renda, porque a renda é importante para prever o preço; aqui, é pela própria classe.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Stratification
source: https://scikit-learn.org/stable/modules/cross_validation.html#stratification
---

# Demo: o sorteio sem estratificar

#### **Com poucos dados, a proporção do teste pode variar muito**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np
from sklearn.model_selection import train_test_split

y = np.array([1] * 30 + [0] * 120)   # 20% positivos
X = np.arange(150).reshape(-1, 1)
for estratificar in [False, True]:
    props = []
    for s in range(1000):
        *_, y_te = train_test_split(
            X, y, test_size=0.2, random_state=s,
            stratify=y if estratificar else None)
        props.append(y_te.mean())
    print(f"stratify={estratificar}: positivos "
          f"no teste de {min(props):.0%} a {max(props):.0%}")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **O experimento** — 150 usuários, 20% positivos, e 1.000 divisões com sementes diferentes.
- **Sem estratificar** — o teste de 30 linhas pode sair com quase nenhum positivo.
- **Antes de executar** — qual a faixa de proporções em cada caso?

</div>

<!--
- saída esperada: stratify=False de 3% a 43%; stratify=True de 20% a 20%.
- o *_ descarta as três primeiras saídas do train_test_split (X_tr, X_te e y_tr).
- com 3.000 linhas o efeito é menor (26,8% contra 28,9% na etapa 1), mas ainda muda a métrica.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Data leakage
source: https://scikit-learn.org/stable/common_pitfalls.html#data-leakage
---

# Data leakage: a ordem das operações

#### **Divida primeiro; todo fit de pré-processamento vem depois, só com o treino**

::left::

```python [errado.py]
# o imputer e o scaler veem o teste
Z = SimpleImputer().fit_transform(X[num])
Z = StandardScaler().fit_transform(Z)
X_tr, X_te, y_tr, y_te = train_test_split(
    Z, y, test_size=0.2, stratify=y)
```

```python [certo.py]
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y)
imp = SimpleImputer().fit(X_tr[num])  # só treino
imp.transform(X_te[num])              # aplica
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Vazamento** — informação do teste entra no treino, e a métrica deixa de ser uma estimativa honesta.
- **Onde acontece** — no `fit` de imputer, scaler ou encoder antes da divisão: a média e o desvio já incluem o teste.
- **A regra** — o teste é o futuro: nada do pré-processamento pode aprender com ele.

</div>

<!--
- na DR1, o vazamento veio de uma feature calculada a partir do alvo (velocidade_kmh); aqui, vem da ordem das operações.
- com um StandardScaler, a diferença numérica costuma ser pequena; o problema é de método e cresce com transformações que aprendem mais dos dados (demo depois da validação cruzada).
- o SimpleImputer preenche ausentes com uma estatística do treino (média por padrão; mediana com strategy="median"): é o fillna da DR1 dentro do scikit-learn.
- os dois trechos são esquemáticos: o random_state foi omitido para caber.
-->

---
layout: section
---

## **ColumnTransformer**
**Um pré-processamento para cada tipo de coluna**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: ColumnTransformer
source: https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html
---

# Pré-processamento heterogêneo

#### **Numéricas e categóricas pedem transformações diferentes, num objeto só**

::left::

```python [etapa2.ipynb]
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder, StandardScaler)

pre = ColumnTransformer([
    ("num", make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler()), num),
    ("cat", OneHotEncoder(
        handle_unknown="ignore"), cat),
])
pre.fit_transform(X_tr).shape    # (2400, 13)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Numéricas** — preenche a avaliação ausente com a mediana do treino e padroniza.
- **Categóricas** — uma coluna 0 ou 1 por categoria: 4 regiões, 3 canais e 2 pagamentos.
- **13 colunas** — 4 numéricas e 9 de categorias; as fora da lista são descartadas.

</div>

> [!CAUTION]
> Um `StandardScaler` no `X` inteiro falha nas colunas de texto: `ValueError`.

<!--
- o erro completo: ValueError: could not convert string to float: 'zona_norte'.
- remainder="drop" é o padrão; remainder="passthrough" mantém as colunas fora da lista sem transformar.
- cada transformador é uma tupla (nome, transformador, colunas); o nome serve para achar o passo depois.
- pre.get_feature_names_out() mostra as 13 colunas: num__idade, ..., cat__canal_convenio_empresa, ...
- o fit acontece só no X_tr: a mediana da avaliação e as categorias vêm do treino.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: OneHotEncoder
source: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
---

# OneHotEncoder e as categorias novas

#### **O encoder lembra as categorias do treino e aplica as mesmas colunas aos dados novos**

::left::

```python [etapa2.ipynb]
novo = X_te.head(1).copy()
novo["canal"] = "parceiro_novo"

pre.transform(novo).shape    # (1, 13)
# canal: as três colunas ficam com 0
```

<div class="text-left w-full [&_li]:mb-3">

- **`handle_unknown="ignore"`** — uma categoria que só aparece em produção vira zeros, em vez de parar o sistema.
- **Sem ele** — `ValueError: Found unknown categories ['parceiro_novo']`.

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`pd.get_dummies` (DR1)** — cria as colunas a partir dos dados que recebe: um lote novo pode sair com outras colunas.
- **`OneHotEncoder`** — aprende as categorias no `fit` e sempre devolve as mesmas colunas, na mesma ordem.
- **Para produção** — o modelo precisa receber exatamente as colunas com que foi treinado.

</div>

<!--
- teste em aula: pd.get_dummies(X_te.head(3)["canal"]) devolve só as categorias presentes nessas 3 linhas.
- o drop="first" do OneHotEncoder equivale ao drop_first=True do get_dummies (DR1, regressão múltipla); para a regressão logística regularizada, manter todas as colunas é o comum.
-->

---
layout: section
---

## **Pipeline** e validação cruzada
**Pré-processamento e modelo num objeto só, avaliado sem vazamento**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Pipeline
source: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
---

# Pipeline: pré-processamento e modelo juntos

#### **Um fit treina tudo; um predict aplica tudo, na mesma ordem**

::left::

```python [etapa2.ipynb]
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("pre", pre),
    ("clf", LogisticRegression()),
])
pipe.fit(X_tr, y_tr)
pipe.score(X_te, y_te)       # 0.832
pipe.predict(X_te.head(3))   # [0, 1, 1]
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`fit`** — ajusta o `ColumnTransformer` no treino, transforma e treina o classificador.
- **`predict`** — aplica a mesma transformação aos dados novos e prevê.
- **Resultado** — 83,2% no teste, contra 71,5% da referência.

</div>

> [!NOTE]
> A regressão logística entra como um classificador pronto: como ela funciona é assunto da etapa 3.

<!--
- os nomes "pre" e "clf" servem para acessar cada parte: pipe["clf"], pipe["pre"]; e para a grade do GridSearchCV.
- sem o Pipeline, é preciso lembrar de chamar pre.transform antes de cada predict: em produção, um passo esquecido ou diferente gera previsões erradas sem nenhum erro.
- make_pipeline(pre, LogisticRegression()) cria os nomes sozinho ("columntransformer" e "logisticregression").
- erro comum: chamar pre.fit_transform à mão e depois pipe.fit, transformando duas vezes.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: cross_val_score
source: https://scikit-learn.org/stable/modules/cross_validation.html
---

# Validação cruzada

#### **Cinco avaliações no treino, sem tocar no teste**

::left::

```python [etapa2.ipynb]
from sklearn.model_selection import cross_val_score

notas = cross_val_score(pipe, X_tr, y_tr, cv=5)
notas.round(3)
# [0.79  0.796 0.827 0.81  0.829]
notas.mean(), notas.std()   # 0.810, 0.016
```

<div class="grid grid-cols-5 gap-1 text-xs text-center mt-4">
  <div class="bg-orange-600/70 rounded py-1">validação</div><div class="bg-blue-600/50 rounded py-1">treino</div><div class="bg-blue-600/50 rounded py-1">treino</div><div class="bg-blue-600/50 rounded py-1">treino</div><div class="bg-blue-600/50 rounded py-1">treino</div>
  <div class="bg-blue-600/50 rounded py-1">treino</div><div class="bg-orange-600/70 rounded py-1">validação</div><div class="bg-blue-600/50 rounded py-1">treino</div><div class="bg-blue-600/50 rounded py-1">treino</div><div class="bg-blue-600/50 rounded py-1">treino</div>
  <div class="col-span-5 text-gray-400">… cinco rodadas, cada parte é validação uma vez</div>
</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Cinco partes (folds)** — treina com quatro e valida na quinta, cinco vezes.
- **Média e desvio** — a nota esperada e o quanto ela varia com a amostra.
- **Com o Pipeline** — o pré-processamento é reajustado dentro de cada rodada, só com as quatro partes de treino.
- **O teste fica guardado** — para a avaliação final, uma única vez.

</div>

<!--
- para classificadores, cv=5 usa StratifiedKFold: cada fold mantém a proporção de 28,5%.
- se o pré-processamento fosse ajustado antes, no X_tr inteiro, a validação também vazaria: o fold de validação teria ajudado a calcular a mediana e o desvio. A demo seguinte mostra um caso extremo.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Common pitfalls
source: https://scikit-learn.org/stable/common_pitfalls.html
---

# Demo: o vazamento que engana

#### **Com dados aleatórios, um passo fora do Pipeline inventa 85% de acerto**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
rng = np.random.default_rng(0)
X = rng.normal(size=(100, 5000))   # ruído puro
y = rng.integers(0, 2, 100)        # alvo ao acaso
X_sel = SelectKBest(k=20).fit_transform(X, y)
antes = cross_val_score(LogisticRegression(),
                        X_sel, y, cv=5)
pipe = make_pipeline(SelectKBest(k=20),
                     LogisticRegression())
dentro = cross_val_score(pipe, X, y, cv=5)
print(f"seleção antes: {antes.mean():.2f}")
print(f"seleção no pipeline: {dentro.mean():.2f}")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Os dados** — 5.000 colunas de ruído e um alvo sorteado: não há nada para aprender.
- **`SelectKBest`** — escolhe as 20 colunas mais associadas ao alvo.
- **Antes da validação** — a escolha usou o alvo de todas as linhas, inclusive as de validação.
- **Antes de executar** — quanto deveria acertar um modelo com dados aleatórios?

</div>

<!--
- saída esperada: seleção antes 0,85; seleção no pipeline 0,48 (o acaso, como deve ser).
- é o mesmo erro do scaler ajustado antes da divisão, só que com uma transformação que aprende muito com o alvo: aí o vazamento fica gritante.
- o SelectKBest é só a ferramenta da demo; seleção de features não é conteúdo desta etapa.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Model persistence
source: https://scikit-learn.org/stable/model_persistence.html
---

# Salvar e recarregar o pipeline

#### **O arquivo leva o pré-processamento e o modelo, prontos para dados novos**

::left::

```python [etapa2.ipynb]
import joblib

joblib.dump(pipe, "pipeline_assinatura.joblib")

# em outro script, ou em produção
pipe2 = joblib.load("pipeline_assinatura.joblib")
pipe2.predict(X_te.head(3))    # [0, 1, 1]
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`joblib.dump`** — salva o objeto inteiro: mediana, médias, categorias e coeficientes.
- **`joblib.load`** — devolve o mesmo pipeline, com as mesmas previsões.
- **Versões** — carregue com a mesma versão do scikit-learn que salvou.

</div>

> [!CAUTION]
> O `joblib.load` executa código ao carregar: só abra arquivos `.joblib` de fonte confiável.

<!--
- o joblib vem instalado com o scikit-learn.
- o .joblib usa o pickle por baixo: um arquivo malicioso pode executar comandos na máquina. Num bloco de segurança de agentes de IA, vale insistir.
- é o arquivo que um serviço de previsão carrega na inicialização.
-->

---
layout: section
---

## Seleção de **hiperparâmetros**
**GridSearchCV: busca exaustiva em grade**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: GridSearchCV
source: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
---

# GridSearchCV

#### **Testa cada valor da grade com validação cruzada e fica com o melhor**

::left::

```python [etapa2.ipynb]
from sklearn.model_selection import GridSearchCV

grade = {"clf__C": [0.001, 0.01, 0.1, 1, 10, 100]}
busca = GridSearchCV(pipe, grade, cv=5)
busca.fit(X_tr, y_tr)

busca.best_params_    # {'clf__C': 0.1}
busca.best_score_     # 0.811
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **A grade** — o nome do passo, dois sublinhados e o hiperparâmetro: `clf__C`.
- **Exaustiva** — 6 valores × 5 folds = 30 treinos, cada um com o pré-processamento reajustado.
- **Métrica** — a acurácia média da validação cruzada, o padrão para classificadores.

</div>

> [!CAUTION]
> Sem o prefixo, `{"C": [...]}`, a busca falha com `ValueError`.

<!--
- o erro completo: ValueError: Invalid parameter 'C' for estimator Pipeline(...).
- duas ou mais chaves na grade multiplicam as combinações: os 6 valores de C e as estratégias "mean" e "median" do imputer (pre__num__simpleimputer__strategy) dão 12 combinações, 60 treinos com cv=5.
- n_jobs=-1 usa todos os núcleos da máquina.
- a busca também pode testar passos inteiros: {"pre__num": [make_pipeline(...), "passthrough"]}.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: cv_results_
source: https://scikit-learn.org/stable/modules/grid_search.html
---

# Lendo o resultado da busca

#### **O melhor C é o que importa, mas a diferença entre os C também**

::left::

```python [etapa2.ipynb]
res = pd.DataFrame(busca.cv_results_)
res[["param_clf__C", "mean_test_score",
     "std_test_score"]].round(3)
```

<div class="text-left w-full [&_li]:mb-3">

- **`C = 0.001`** — 0,722, perto da referência: regularização demais, bias alto.
- **De 0,1 a 100** — de 0,810 a 0,811, dentro da variação entre os folds (±0,013 a 0,016).

</div>

::right::

<AssetImg src="pm-busca-c.png" class="rounded-lg w-full" />

<!--
- a faixa sombreada é a média ± o desvio padrão dos cinco folds.
- leitura de negócio: qualquer C a partir de 0,1 serve; o 0,1 venceu por menos de um ponto em mil.
- é o mesmo diagnóstico de bias e variância da etapa 1, agora medido pela validação cruzada.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Hands-On ML, cap. 2
source: https://github.com/ageron/handson-mlp/blob/main/02_end_to_end_machine_learning_project.ipynb
---

# O pipeline final

#### **O melhor modelo já vem treinado; o teste é usado uma única vez**

::left::

```python [etapa2.ipynb]
final = busca.best_estimator_   # refit=True
final.score(X_te, y_te)         # 0.832

joblib.dump(final, "pipeline_assinatura.joblib")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`best_estimator_`** — com `refit=True`, o padrão, a busca retreina o melhor pipeline com todo o `X_tr`.
- **Teste uma vez só** — 0,832, perto da validação (0,811): a escolha não foi otimista.
- **`RandomizedSearchCV`** — sorteia combinações em vez de testar todas: útil quando a grade cresce demais.

</div>

<!--
- não retreine à mão com o melhor C: o best_estimator_ já é esse modelo.
- se a nota do teste ficasse bem abaixo da validação, desconfie de vazamento ou de uma divisão infeliz.
- o RandomizedSearchCV aparece no capítulo 2 do Hands-On ML, logo depois do GridSearchCV.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** `usuarios_avulsos.csv`, gerado na etapa 1, agora com as sete features

🧩 &nbsp;**Análise:** o pipeline completo, da divisão estratificada ao `GridSearchCV`, salvo para produção

<!--
Projeto: o mesmo da etapa 1 (pandas, numpy, scikit-learn; o joblib vem com o scikit-learn).

=================================================================
ARQUIVO 1 — pipeline_assinatura.py (as funções; o notebook só chama e comenta)

```python
"""Pipeline de previsão de assinatura: divisão, pré-processamento, busca e modelo final."""
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM = ["idade", "viagens_30d", "distancia_media_km", "avaliacao_media"]
CAT = ["regiao", "canal", "pagamento"]


def dividir(df):
    """Treino e teste estratificados pelo alvo, antes de qualquer pré-processamento."""
    X, y = df[NUM + CAT], df["virou_assinante"]
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


def montar_pipeline():
    """ColumnTransformer (mediana + padronização; one-hot) e regressão logística."""
    pre = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
    ])
    return Pipeline([("pre", pre), ("clf", LogisticRegression())])


def buscar(pipe, X_tr, y_tr):
    """GridSearchCV no C da regressão logística, com validação cruzada de 5 folds."""
    grade = {"clf__C": [0.001, 0.01, 0.1, 1, 10, 100]}
    return GridSearchCV(pipe, grade, cv=5).fit(X_tr, y_tr)


if __name__ == "__main__":
    X_tr, X_te, y_tr, y_te = dividir(pd.read_csv("usuarios_avulsos.csv"))
    busca = buscar(montar_pipeline(), X_tr, y_tr)
    final = busca.best_estimator_
    print(busca.best_params_, round(busca.best_score_, 3), round(final.score(X_te, y_te), 3))
    joblib.dump(final, "pipeline_assinatura.joblib")
```

=================================================================
ARQUIVO 2 — etapa2.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Divisão estratificada e conferência das proporções
import joblib
import pandas as pd
from sklearn.model_selection import cross_val_score
from pipeline_assinatura import buscar, dividir, montar_pipeline

df = pd.read_csv("usuarios_avulsos.csv")
X_tr, X_te, y_tr, y_te = dividir(df)
y_tr.value_counts(normalize=True), y_te.value_counts(normalize=True)

# 2. O ColumnTransformer sozinho: shape e nomes das colunas
pipe = montar_pipeline()
pre = pipe["pre"].fit(X_tr)
pre.transform(X_tr).shape, pre.get_feature_names_out()

# 3. Categoria nova em produção
novo = X_te.head(1).copy()
novo["canal"] = "parceiro_novo"
pre.transform(novo)

# 4. Pipeline: treino, teste e validação cruzada
pipe.fit(X_tr, y_tr)
pipe.score(X_te, y_te)
notas = cross_val_score(montar_pipeline(), X_tr, y_tr, cv=5)
notas, notas.mean(), notas.std()

# 5. GridSearchCV no C e a tabela de resultados
busca = buscar(montar_pipeline(), X_tr, y_tr)
busca.best_params_, busca.best_score_
pd.DataFrame(busca.cv_results_)[["param_clf__C", "mean_test_score", "std_test_score"]]

# 6. Pipeline final: teste uma vez, salvar e recarregar
final = busca.best_estimator_
final.score(X_te, y_te)
joblib.dump(final, "pipeline_assinatura.joblib")
joblib.load("pipeline_assinatura.joblib").predict(X_te.head(3))
```

>>> Resultados esperados: treino 2.400 e teste 600 linhas, os dois com 28,5% de positivos.
>>> ColumnTransformer: (2400, 13); categoria nova vira três zeros nas colunas de canal.
>>> Pipeline com C = 1: 0,810 no treino e 0,832 no teste (referência: 0,715).
>>> Validação cruzada: [0,790 0,796 0,827 0,810 0,829], média 0,810, desvio 0,016.
>>> GridSearchCV: médias 0,722 (C 0,001), 0,796 (0,01), 0,811 (0,1), 0,810 (1), 0,810 (10 e 100); melhor C = 0,1 com 0,811.
>>> Final: 0,832 no teste; previsões dos três primeiros do teste [0, 1, 1].
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para montar o pipeline de previsão de assinaturas**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um engenheiro de machine learning especialista em scikit-learn.

# Tarefa
Monte um pipeline de classificação que preveja se um usuário avulso
vira assinante, do CSV ao modelo salvo.

# Contexto
1. Em "pipeline_assinatura.py", crie as funções dividir, montar_pipeline
   e buscar, a partir de @usuarios_avulsos.csv (alvo: virou_assinante).
2. dividir: train_test_split estratificado, test_size=0.2, random_state=42,
   antes de qualquer pré-processamento.
3. montar_pipeline: ColumnTransformer com SimpleImputer(median) e
   StandardScaler nas numéricas e OneHotEncoder(handle_unknown="ignore")
   nas categóricas, e LogisticRegression no passo "clf".
4. buscar: GridSearchCV com cv=5 no clf__C (0.001 a 100).
5. Em "etapa2.ipynb", use as funções, mostre a validação cruzada e a
   tabela da busca, avalie o best_estimator_ uma vez no teste e salve-o
   com joblib.
6. Antes de cada passo do notebook, crie uma célula de markdown.

# Saída e Verificação
- Execute o script e o notebook do início ao fim, sem erros.
- Confira que nenhum fit acontece antes da divisão.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: procure qualquer fit ou fit_transform antes do train_test_split, e qualquer pré-processamento fora do Pipeline.

# 2 - se a grade vier como {"C": [...]}, o erro do slide do GridSearchCV aparece; se o agente retreinar à mão com o melhor C, mostre o best_estimator_.

# 3 - peça a interpretação da tabela de resultados: o melhor C é muito melhor que os vizinhos?
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** No Titanic, divida com e sem `stratify` e compare os sobreviventes.

🛠️ &nbsp;**Exercício \#2:** Monte um `ColumnTransformer` com imputação para as sete colunas.

🛠️ &nbsp;**Exercício \#3:** Junte-o à regressão logística num `Pipeline` e use `cross_val_score`.

🛠️ &nbsp;**Exercício \#4:** Busque o `C` com `GridSearchCV`, teste uma vez e salve com `joblib`.

- [ ] dividir antes de qualquer `fit` de pré-processamento
- [ ] imputar dentro do `ColumnTransformer`, com a estatística do treino
- [ ] usar `handle_unknown="ignore"` no `OneHotEncoder`
- [ ] escrever a grade com o prefixo do passo (`clf__C`)
- [ ] usar o teste uma única vez, no pipeline final

<br/>

<!--
# Exercício #1 — Estratificação
titanic = sns.load_dataset("titanic"); X com age, fare, sibsp, parch, sex, pclass e embarked; y = survived (38,4%).
test_size=0.2, random_state=42: sem stratify, 37,6% no treino e 41,3% no teste; com stratify, 38,3% e 38,5%.

# Exercício #2 — ColumnTransformer
Numéricas (age, fare, sibsp, parch): SimpleImputer(median) + StandardScaler; age tem 177 ausentes.
Categóricas (sex, pclass, embarked): SimpleImputer(most_frequent) + OneHotEncoder(handle_unknown="ignore"); embarked tem 2 ausentes.
Shape do treino transformado: (712, 12).

# Exercício #3 — Pipeline e validação cruzada
cross_val_score com cv=5: [0,797 0,762 0,803 0,810 0,817], média 0,798.

# Exercício #4 — GridSearchCV
C de 0,001 a 100: médias 0,621, 0,774, 0,796, 0,798, 0,798, 0,798; melhor C = 10 (empate prático a partir de 1).
Teste: 0,805, contra 0,615 da referência (sempre "não sobreviveu").

## os exercícios preparam os Exercícios 3 a 8 do TP1
-->
