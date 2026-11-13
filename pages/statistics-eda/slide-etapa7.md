---
layout: section
routeAlias: etapa7
---

## **Etapa 7:** Regressão Linear e Avaliação

---
layout: section
---

## Da correlação à **reta**
**Relação linear e a equação da reta**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: corr
source: https://pandas.pydata.org/docs/reference/api/pandas.Series.corr.html
---

# Relação linear: o ponto de partida

#### **Antes de ajustar uma reta, confira se a relação é mesmo linear**

::left::

```python [etapa7.ipynb]
base = carregar_base()
reg = base.dropna(subset=["duracao_min"])

reg["distancia_km"].corr(reg["duracao_min"])
# 0.947
```

<div class="text-left w-full [&_li]:mb-3">

- **Forte e linear** — r = 0,95, e a nuvem segue uma reta.
- **Pergunta nova** — quantos minutos cada quilômetro acrescenta à viagem?

</div>

::right::

<AssetImg src="eda-scatter-distancia-duracao.png" class="rounded-lg w-full" />

<!--
- é o scatter da etapa 4: olhe o gráfico antes de ajustar a reta (o y = x² tem r ≈ 0).
- reg: as 2.970 viagens com duração registrada; a duração ausente não é preenchida.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: cov
source: https://pandas.pydata.org/docs/reference/api/pandas.Series.cov.html
---

# A equação da reta

#### **Dois números resumem a relação: a inclinação e o ponto de partida**

::left::

$$
\hat{y} = a + b\,x
$$

$$
b = \frac{\operatorname{cov}(x, y)}{\operatorname{var}(x)} \qquad a = \bar{y} - b\,\bar{x}
$$

```python [etapa7.ipynb]
x, y = reg["distancia_km"], reg["duracao_min"]
b = x.cov(y) / x.var()          # 4.669
a = y.mean() - b * x.mean()     # 0.106
```

<div class="text-left w-full [&_li]:mb-2">

- **b, coeficiente angular** — 4,67 min a mais por km.
- **a, coeficiente linear** — 0,11 min com 0 km: quase zero, como faz sentido.

</div>

::right::

<AssetImg src="eda-reta-duracao.png" class="rounded-lg w-full" />

<!--
- 4,67 min por km equivale a uma velocidade média de 12,8 km/h (60 / 4,67).
- previsões: 2 km → 9,4 min; 5 km → 23,5 min.
- a covariância (16,17) e a variância (3,46) são as da etapa 4.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Linear Models
source: https://scikit-learn.org/stable/modules/linear_model.html
---

# Mínimos quadrados: a reta que erra menos

#### **Entre todas as retas possíveis, a escolhida minimiza a soma dos erros ao quadrado**

::left::

<div class="text-left w-full [&_li]:mb-4">

- **Resíduo** — o observado menos o previsto: a distância vertical até a reta.
- **Mínimos quadrados** — a reta com a menor soma dos resíduos ao quadrado.
- **As fórmulas** — $b = \operatorname{cov}/\operatorname{var}$ e $a = \bar{y} - b\,\bar{x}$ dão exatamente essa reta.

</div>

::right::

<AssetImg src="eda-minimos-quadrados.png" class="rounded-lg w-full" />

<!--
- ao quadrado: os erros para cima e para baixo não se anulam, e os erros grandes pesam mais.
- o gráfico mostra 16 viagens de até 6 km, com a reta da base toda.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.polyfit
source: https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
---

# Demo: a reta de mínimos quadrados

#### **A fórmula, o polyfit e a soma dos quadrados contam a mesma história**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

rng = np.random.default_rng(7)
x = rng.uniform(0.5, 6, 30)          # km
y = 4.7 * x + rng.normal(0, 2, 30)   # min
b = np.cov(x, y)[0, 1] / np.var(x, ddof=1)
a = y.mean() - b * x.mean()
print(f"fórmula: a = {a:.2f}  b = {b:.2f}")
print("polyfit:", np.polyfit(x, y, 1).round(2))
for inc in [b - 0.5, b, b + 0.5]:
    a_inc = y.mean() - inc * x.mean()
    sq = ((y - (a_inc + inc * x)) ** 2).sum()
    print(f"b = {inc:.2f}: soma {sq:.1f}")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Fórmula e polyfit** — chegam aos mesmos a e b (o polyfit devolve [b, a]).
- **Mexer na inclinação** — com b meio ponto acima ou abaixo, a soma dos quadrados sobe.
- **Antes de executar** — os dados foram gerados com 4,7 min por km: quanto o b vai dar?

</div>

<!--
- saída esperada: a = −0,61 e b = 4,88; polyfit [4,88 −0,61]; a soma dos quadrados dos resíduos vai de 93,0 (no b da fórmula) a 111,9 com ±0,5.
- o b não sai 4,7 exato por causa do ruído da amostra de 30 viagens.
-->

---
layout: section
---

## Regressão com **scikit-learn**
**fit, predict e a separação em treino e teste**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: LinearRegression
source: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
---

# LinearRegression: fit e predict

#### **O scikit-learn encontra a mesma reta e aplica a equação a novos dados**

::left::

```python [etapa7.ipynb]
from sklearn.linear_model import LinearRegression

X = reg[["distancia_km"]]    # 2D: DataFrame
y = reg["duracao_min"]       # 1D: Series

modelo = LinearRegression().fit(X, y)
modelo.intercept_, modelo.coef_   # 0.106, [4.669]

novas = pd.DataFrame({"distancia_km": [2, 5]})
modelo.predict(novas)             # [9.44, 23.45]
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **fit** — calcula a e b por mínimos quadrados: os mesmos da fórmula.
- **predict** — aplica a equação a distâncias novas.
- **X em duas dimensões** — uma tabela de colunas, mesmo com uma variável só.

</div>

> [!CAUTION]
> Com `reg["distancia_km"]`, uma Series, no lugar de `reg[["distancia_km"]]`, o `fit` dá `ValueError: Expected a 2-dimensional container`.

<!--
- intercept_ é o a; coef_ é a lista dos b, um por coluna do X (na etapa 8, serão vários).
- instale com uv add scikit-learn; o import vem de sklearn.linear_model.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: train_test_split
source: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
---

# Treino e teste

#### **O erro que importa é o das viagens que o modelo não viu**

::left::

```python [etapa7.ipynb]
from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42)
len(X_tr), len(X_te)            # (2376, 594)

modelo = LinearRegression().fit(X_tr, y_tr)
prev = modelo.predict(X_te)     # só no teste
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Treino (80%)** — onde o modelo calcula a e b.
- **Teste (20%)** — viagens que o modelo não viu: é ali que se mede o erro.
- **`random_state`** — fixa o sorteio, e o resultado se repete a cada execução.

</div>

> [!NOTE]
> Medir o erro nas mesmas linhas do `fit` dá uma nota otimista: o modelo foi ajustado justamente a elas.

<!--
- no treino, a = 0,144 e b = 4,659: quase a reta da base toda.
- com 80/20 e random_state=42, ficam 2.376 viagens no treino e 594 no teste.
-->

---
layout: section
---

## Avaliação: **RMSE** e **R²**
**Quanto o modelo erra e quanto ele explica**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: root_mean_squared_error
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html
---

# RMSE: o erro típico em minutos

#### **A raiz da média dos erros ao quadrado, na mesma unidade do alvo**

::left::

$$
\text{RMSE} = \sqrt{\frac{1}{n} \sum (y_i - \hat{y}_i)^2}
$$

```python [etapa7.ipynb]
from sklearn.metrics import root_mean_squared_error

root_mean_squared_error(y_te, prev)   # 2.47
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Mesma unidade** — no teste, a previsão erra tipicamente 2,5 min.
- **Ao quadrado** — os erros grandes pesam mais que os pequenos.
- **Referência** — prever sempre a duração média erraria 9,0 min.

</div>

> [!CAUTION]
> `mean_squared_error(..., squared=False)`, comum em código gerado, saiu do scikit-learn 1.6: dá `TypeError`.

<!--
- no treino, o RMSE é 3,04 min: o sorteio deixou menos viagens muito longas no teste (4,0% acima de 30 min, contra 5,1% no treino), e é nelas que o erro é maior.
- o MAE (erro absoluto médio) seria 1,78 min: menor, porque não eleva os erros ao quadrado.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: r2_score
source: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
---

# R²: a variação que o modelo explica

#### **Quanto da variação da duração a distância explica, comparada à média**

::left::

$$
R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}
$$

```python [etapa7.ipynb]
from sklearn.metrics import r2_score

r2_score(y_te, prev)     # 0.92
```

<div class="text-left w-full [&_li]:mb-2">

- **De 0 a 1** — 0 não explica nada além da média; 1 explica tudo.
- **Pode ser negativo** — no teste, um modelo pior que a média dá R² < 0.

</div>

::right::

<AssetImg src="eda-previsto-observado.png" class="rounded-lg w-full" />

<!--
- no teste, R² = 0,92: a distância explica 92% da variação da duração.
- na regressão simples, R² = r²: 0,947² = 0,90 na base toda.
- o R² de teste varia com o sorteio: de 0,87 a 0,92 com as sementes 0 a 19.
- quanto mais perto da diagonal, melhor a previsão.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Model evaluation
source: https://scikit-learn.org/stable/modules/model_evaluation.html
---

# Demo: R² e RMSE à mão

#### **As duas métricas comparam o erro do modelo com o de prever a média**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

y = np.array([8.0, 12.5, 9.1, 20.3, 15.2, 6.4])
prev = np.array([8.9, 11.7, 9.8, 18.6, 16.1, 6.0])
media = np.full_like(y, y.mean())

def avaliar(p):
    rmse = np.sqrt(((y - p) ** 2).mean())
    sq_res = ((y - p) ** 2).sum()
    sq_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - sq_res / sq_tot
    return f"RMSE {rmse:.2f} | R² {r2:.3f}"

print("modelo:", avaliar(prev))
print("média: ", avaliar(media))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Modelo** — erra cerca de 1 min e explica 96% da variação.
- **Prever a média** — R² = 0: é a referência mínima de qualquer modelo.
- **Antes de executar** — qual dos dois RMSE vai ser maior?

</div>

<!--
- saída esperada: modelo RMSE 0,98 e R² 0,957; média RMSE 4,75 e R² 0,000.
- o RMSE da média é o desvio padrão de y: por isso ele serve de régua.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** a base de viagens, carregada pelo `preparar_base.py` da etapa 3

⏱️ &nbsp;**Análise:** quanto tempo leva uma viagem de X km? A reta da duração, à mão e com scikit-learn, avaliada no teste

<!--
Projeto: uv add scikit-learn (além do que já foi instalado nas etapas anteriores).

=================================================================
ARQUIVO — etapa7.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Carga: só as viagens com duração registrada
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from preparar_base import carregar_base

base = carregar_base()
reg = base.dropna(subset=["duracao_min"])

# 2. Relação linear
reg["distancia_km"].corr(reg["duracao_min"])

# 3. A reta pelas fórmulas de mínimos quadrados
x, y = reg["distancia_km"], reg["duracao_min"]
b = x.cov(y) / x.var()
a = y.mean() - b * x.mean()
a, b

# 4. A mesma reta com o scikit-learn, ajustada no treino
X = reg[["distancia_km"]]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = LinearRegression().fit(X_tr, y_tr)
modelo.intercept_, modelo.coef_

# 5. Avaliação no teste e no treino
prev = modelo.predict(X_te)
r2_score(y_te, prev), root_mean_squared_error(y_te, prev)
r2_score(y_tr, modelo.predict(X_tr)), root_mean_squared_error(y_tr, modelo.predict(X_tr))

# 6. Previsões para 2 e 5 km
modelo.predict(pd.DataFrame({"distancia_km": [2, 5]}))
```

>>> Resultados esperados: r = 0,947; base toda a = 0,106 e b = 4,669;
>>> treino a = 0,144 e b = 4,659 (2.376 viagens; teste com 594);
>>> teste R² = 0,925 e RMSE = 2,47 min; treino R² = 0,891 e RMSE = 3,04 min;
>>> previsões: 9,46 min (2 km) e 23,44 min (5 km).
>>> O R² de teste muda com a semente (0,87 a 0,92 com random_state de 0 a 19): bom gancho para discutir o sorteio.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para ajustar e avaliar a reta da duração das viagens**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um analista de dados especialista em Python, pandas e scikit-learn.

# Tarefa
Num notebook, ajuste uma regressão linear simples que estime a duração
de uma viagem a partir da distância e avalie o modelo.

# Contexto
1. Em "etapa7.ipynb", carregue a base com carregar_base() do
   @preparar_base.py, só com as viagens que têm duração registrada.
2. Calcule a correlação entre distancia_km e duracao_min.
3. Calcule a reta à mão: b = cov(x, y) / var(x) e a = ȳ − b·x̄.
4. Separe treino e teste (test_size=0.2, random_state=42) e ajuste
   LinearRegression, de sklearn.linear_model, no treino.
5. Calcule R² e RMSE (root_mean_squared_error) no teste e no treino.
6. Preveja a duração de viagens de 2 e 5 km.
7. Antes de cada passo, crie uma célula de markdown explicando o passo.

# Saída e Verificação
- Gere etapa7.ipynb e instale o scikit-learn com uv add.
- Execute o notebook do início ao fim, sem erros.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: confira se os coeficientes do sklearn batem com os da fórmula e se as métricas foram calculadas no teste.

# 2 - se o agente usar mean_squared_error(..., squared=False), é a deixa para o slide do RMSE: o parâmetro saiu do scikit-learn 1.6.

# 3 - peça a interpretação do coeficiente angular em minutos por km e confira a unidade.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** No Gapminder de 2007, calcule à mão a reta da expectativa de vida pelo log10 do PIB.

🛠️ &nbsp;**Exercício \#2:** Ajuste a mesma reta com `LinearRegression` em treino e teste e calcule R² e RMSE.

🛠️ &nbsp;**Exercício \#3:** Compare o R² com o PIB per capita em log e sem log.

🛠️ &nbsp;**Exercício \#4:** Na sua base, ajuste uma regressão simples e interprete o coeficiente angular.

- [ ] calcular a e b com `cov`, `var` e médias
- [ ] passar o X como DataFrame, em duas dimensões
- [ ] separar treino e teste com `random_state` fixo
- [ ] calcular R² e RMSE no teste
- [ ] interpretar o coeficiente na unidade dos dados

<br/>

<!--
# Exercício #1 — A reta à mão
g7 = df[df["year"] == 2007]; x = np.log10(g7["gdpPercap"]); r = 0,81.
lifeExp = 4,95 + 16,59 × log10(PIB): 16,6 anos a mais a cada PIB 10 vezes maior.
PIB de 1.000 → 54,7 anos; PIB de 10.000 → 71,3 anos.

# Exercício #2 — scikit-learn
142 países; com test_size=0.2 e random_state=42, o teste tem 29: R² 0,72 e RMSE 6,4 anos (desvio padrão de 12,0).
Com tão poucos países, o R² de teste muda bastante com a semente: bom para discutir o tamanho do teste.

# Exercício #3 — Log ou não
Sem log: r = 0,68 e R² = 0,46. A relação é curva, e o log a deixa reta (como na etapa 4).

# Exercício #4 — Base própria
Escolha um par com relação linear visível no scatter, ajuste e escreva o coeficiente numa frase com unidade.

## os exercícios preparam o AT (Exercícios 4, 6 e 13)
-->
