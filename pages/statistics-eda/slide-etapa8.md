---
layout: section
routeAlias: etapa8
---

## **Etapa 8:** Avaliação e Modelagem de Regressão

---
layout: section
---

## Interpretar a **avaliação**
**R², RMSE e resíduos**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Model evaluation
source: https://scikit-learn.org/stable/modules/model_evaluation.html
---

# O modelo é bom o bastante?

#### **Uma métrica sozinha não responde: compare com uma referência e com o uso**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| modelo | R² no teste | RMSE no teste |
| --- | --- | --- |
| prever sempre a média | 0,00 | 9,0 min |
| reta da distância (etapa 7) | 0,92 | 2,5 min |

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Referência** — compare com o modelo mais simples possível: a média.
- **RMSE no uso** — errar 2,5 min basta para estimar a chegada? Depende de quem usa.
- **R² alto não basta** — ele não mostra onde o modelo erra: veja os resíduos.

</div>

<!--
- prever a média do treino para todas as viagens de teste: R² ≈ 0 e RMSE = 8,99 min, o desvio padrão da duração.
- a pergunta "é bom?" sempre tem um "para quê?" do lado.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: residplot
source: https://seaborn.pydata.org/generated/seaborn.residplot.html
---

# Resíduos: onde o modelo erra

#### **O gráfico dos resíduos mostra o que o R² resume num número só**

::left::

<div class="text-left w-full [&_li]:mb-4">

- **Sem padrão** — resíduos espalhados em volta do zero indicam que a reta capturou a relação.
- **Em leque** — o erro cresce com a viagem: desvio de 1,5 min até 2 km e de 3,9 min acima de 4 km.
- **Padrão é informação** — falta ao modelo algo que pesa mais nas viagens longas, como a velocidade de quem pedala.

</div>

::right::

<AssetImg src="eda-residuos-previsto.png" class="rounded-lg w-full" />

<!--
- resíduo = observado − previsto, no conjunto de teste do modelo da etapa 7.
- o leque aparece porque a duração é distância dividida por velocidade: a diferença de velocidade pesa mais quanto maior a distância.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Statistics Every Programmer Needs, cap. 2
source: https://www.manning.com/books/statistics-every-programmer-needs
---

# A chance de errar

#### **Os resíduos têm uma distribuição, e ela diz quanto confiar numa previsão**

::left::

```python [etapa8.ipynb]
res = y_te - prev
(res.abs() > 5).mean()           # 0.059
res.quantile([0.025, 0.975])     # -4.71 e 5.63
```

<div class="text-left w-full [&_li]:mb-3">

- **Resíduo como variável** — a CDF empírica da etapa 3, agora aplicada ao erro.
- **P(\|erro\| > 5 min)** — 5,9% das viagens de teste.
- **Assimetria** — o modelo subestima mais do que superestima: 3,9% acima de +5 min e 2,0% abaixo de −5.

</div>

::right::

<AssetImg src="eda-residuos-hist.png" class="rounded-lg w-full" />

<!--
- 95% dos erros ficam entre −4,7 e +5,6 min: uma faixa para comunicar a incerteza da previsão.
- a cauda direita vem das viagens lentas, que demoram mais do que a reta prevê.
-->

---
layout: section
---

## Regressão **múltipla**
**Várias variáveis explicando a duração**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Linear Models
source: https://scikit-learn.org/stable/modules/linear_model.html
---

# Várias variáveis no mesmo modelo

#### **O mesmo LinearRegression, agora com mais colunas no X**

::left::

```python [etapa8.ipynb]
reg["avulso"] = (reg["tipo_usuario"] == "avulso").astype(int)
reg["choveu"] = reg["choveu"].astype(int)

X = reg[["distancia_km", "avulso", "choveu"]]
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42)
modelo = LinearRegression().fit(X_tr, y_tr)
modelo.coef_     # [4.652, 1.914, 1.375]
```

::right::

$$
\hat{y} = a + b_1 x_1 + b_2 x_2 + b_3 x_3
$$

<div class="text-left w-full [&_li]:mb-4">

- **Um coeficiente por coluna** — x₁ é a distância, x₂ o avulso e x₃ o choveu.
- **Categóricas viram 0 e 1** — avulso = 1 e assinante = 0: uma variável indicadora.
- **Muitas categorias** — `pd.get_dummies(..., drop_first=True)` cria uma coluna por categoria, menos uma.

</div>

<!--
- drop_first: com todas as categorias, uma coluna seria a soma das outras (multicolinearidade perfeita, próxima seção).
- choveu já é booleano; o astype(int) só deixa explícito o 0 e o 1.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 3
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Coeficientes: o efeito com o resto fixo

#### **Cada coeficiente compara viagens iguais nas outras variáveis**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| variável | coeficiente | leitura |
| --- | --- | --- |
| `distancia_km` | 4,65 | +4,65 min por km |
| `avulso` | 1,91 | +1,9 min para avulsos |
| `choveu` | 1,38 | +1,4 min em dia de chuva |

</div>

::right::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| modelo | R² no teste | RMSE no teste |
| --- | --- | --- |
| só a distância | 0,925 | 2,47 min |
| + tipo de usuário e chuva | 0,932 | 2,34 min |

</div>

<div class="text-left w-full mt-4 [&_li]:mb-3">

- **Ganho pequeno** — a distância já explica quase tudo.
- **Associação** — o coeficiente da chuva não prova causa (etapa 4).

</div>

<!--
- "mantidas as outras fixas": o +1,9 min compara avulsos e assinantes com a mesma distância e o mesmo clima.
- o modelo é aditivo: o efeito real de ser avulso cresce com a distância (velocidade menor); o coeficiente é uma média.
- previsões para 3 km: assinante sem chuva 13,3 min; avulso sem chuva 15,2; avulso com chuva 16,5.
-->

---
layout: section
---

## **Multicolinearidade**
**Quando duas preditoras contam a mesma história**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: corr
source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html
---

# Matriz de correlação das preditoras

#### **Antes do modelo, veja quais preditoras andam juntas**

::left::

```python [etapa8.ipynb]
cols = ["distancia_km", "avulso", "choveu",
        "chuva_mm", "temp_max"]
reg[cols].corr()
```

<div class="text-left w-full [&_li]:mb-3">

- **`choveu` × `chuva_mm`: 0,79** — `choveu` foi criada a partir de `chuva_mm`.
- **Régua de bolso** — acima de 0,7 em módulo entre preditoras, investigue.
- **As outras** — quase sem correlação entre si: cada uma traz informação própria.

</div>

::right::

<AssetImg src="eda-heatmap-preditoras.png" class="rounded-lg w-full" />

<!--
- é o heatmap da etapa 4, agora só com as candidatas a preditora (sem o alvo).
- correlação alta com o alvo é bom; correlação alta entre preditoras é que pede cuidado.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Linear Models
source: https://scikit-learn.org/stable/modules/linear_model.html
---

# O que ela faz com os coeficientes

#### **O ajuste não piora, mas o efeito se divide entre as colunas**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| modelo | R² | coef. de `choveu` | 95% em 200 reamostras |
| --- | --- | --- | --- |
| sem `chuva_mm` | 0,932 | 1,38 | 0,97 a 1,59 |
| com `chuva_mm` | 0,932 | 1,27 | 0,76 a 1,57 |

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **R² igual** — `chuva_mm` não traz informação nova.
- **Coeficiente instável** — o efeito da chuva se divide entre as duas colunas, e a incerteza cresce.
- **Decisão** — fique com uma das duas; `choveu` é a mais fácil de explicar.

</div>

<!--
- reamostras com reposição das viagens (o bootstrap da etapa 6), ajustando o modelo em cada uma.
- com correlações perto de 1, o efeito é muito maior: é a próxima demo.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.linalg.lstsq
source: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
---

# Demo: duas preditoras quase iguais

#### **Com correlação perto de 1, cada coeficiente perde o sentido, mas a soma não**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

rng = np.random.default_rng(1)
n = 200
x1 = rng.normal(0, 1, n)
x2 = x1 + rng.normal(0, 0.05, n)   # quase x1
y = 3 * x1 + rng.normal(0, 1, n)
X = np.column_stack([np.ones(n), x1, x2])

print("b1, b2 e b1 + b2 em 3 reamostras:")
for _ in range(3):
    i = rng.integers(0, n, n)
    c = np.linalg.lstsq(X[i], y[i], rcond=None)[0]
    print(*np.round([c[1], c[2], c[1] + c[2]], 2))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **x2 é quase x1** — a correlação entre as duas passa de 0,99.
- **b1 e b2 pulam** — de uma reamostra para outra, cada um muda muito.
- **A soma fica** — perto de 3, o efeito real: as previsões continuam boas.

</div>

<!--
- saída esperada: 8,0 e −4,95 (soma 3,05); 6,01 e −2,89 (3,12); 5,87 e −2,81 (3,06).
- o modelo não sabe a quem atribuir o efeito, porque as duas colunas carregam a mesma informação.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: StandardScaler
source: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
---

# Padronização: comparar os coeficientes

#### **Na mesma escala, dá para ver qual variável pesa mais**

::left::

```python [etapa8.ipynb]
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

padr = make_pipeline(StandardScaler(),
                     LinearRegression())
padr.fit(X_tr, y_tr)
padr[-1].coef_                  # [8.69, 0.88, 0.53]
r2_score(y_te, padr.predict(X_te))   # 0.932
```

> [!NOTE]
> Sem padronizar, o tamanho do coeficiente depende da unidade (km ou m), como a covariância da etapa 4.

::right::

<div class="text-left w-full [&_li]:mb-4">

- **StandardScaler** — cada coluna passa a ter média 0 e desvio padrão 1.
- **Coeficiente padronizado** — minutos por desvio padrão: a distância pesa dez vezes mais que o tipo de usuário.
- **Mesmas previsões** — padronizar não muda as previsões, o R² nem o RMSE da regressão linear.

</div>

<!--
- padr[-1] é o último passo do pipeline, o LinearRegression.
- o scaler aprende média e desvio no treino e aplica os mesmos valores no teste.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.linalg.lstsq
source: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
---

# Demo: padronizar não muda a previsão

#### **O mesmo modelo, escrito em outra escala**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

rng = np.random.default_rng(3)
x = rng.uniform(0.5, 6, 50)          # km
y = 4.7 * x + rng.normal(0, 2, 50)

def ajustar(v):
    X = np.column_stack([np.ones_like(v), v])
    coef = np.linalg.lstsq(X, y, rcond=None)[0]
    return coef, X @ coef

z = (x - x.mean()) / x.std()         # padronizado
(c1, p1), (c2, p2) = ajustar(x), ajustar(z)
print("em km:      ", c1.round(2))
print("padronizado:", c2.round(2))
print("previsões iguais?", np.allclose(p1, p2))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Os coeficientes mudam** — minutos por km viram minutos por desvio padrão.
- **As previsões não** — o modelo é o mesmo.
- **Quando padronizar** — para comparar coeficientes; na regressão linear, o ajuste não melhora.

</div>

<!--
- saída esperada: [0,9 4,35] em km e [15,32 6,6] padronizado; previsões iguais: True.
- o intercepto padronizado (15,32) é a duração prevista para a distância média.
-->

---
layout: two-cols-header
layoutClass: gap-8
---

# Cuidado: variáveis que vêm do alvo

#### **Uma preditora que carrega a resposta deixa o modelo ótimo e inútil**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| candidata | por que não entra | R² no teste |
| --- | --- | --- |
| `velocidade_kmh` | é calculada com a própria duração | 0,961 |
| `avaliacao` | só existe depois da viagem | — |

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Vazamento** — a variável traz a resposta embutida, e o R² sobe sem que o modelo preveja nada.
- **Pergunta de checagem** — eu teria esse valor antes de a viagem acontecer?
- **Código gerado** — pedir "use as colunas numéricas" leva o LLM a incluir essas colunas: revise uma a uma.

</div>

<!--
- velocidade_kmh foi criada na etapa 4 (distância dividida pela duração em horas): com ela, o R² vai de 0,932 para 0,961.
- a avaliação vem depois da viagem e ainda depende da duração (etapa 4): seria prever a causa pelo efeito.
-->

---
layout: default
sourceLabel: Starting Data Analytics with Generative AI, cap. 4
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Interpretações do modelo geradas por IA

#### **Peça a interpretação ao LLM e confira cada frase com os números**

<div class="h-2" />

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| o LLM afirma | o problema | confira com |
| --- | --- | --- |
| "R² de 0,93: o modelo acerta 93% das previsões" | R² é variação explicada, não taxa de acerto | o RMSE e os resíduos |
| "o RMSE de 2,3 indica 2,3% de erro" | o RMSE está na unidade do alvo | a unidade de y (minutos) |
| "a distância é 2,4 vezes mais importante que o tipo" | coeficientes em unidades diferentes não se comparam | os coeficientes padronizados |
| "a chuva faz a viagem durar 1,4 min a mais" | o coeficiente mede associação | o desenho da análise (etapa 4) |
| "o modelo serve para viagens de 30 km" | fora da faixa dos dados, que vai até 12 km | o mínimo e o máximo de cada preditora |

</div>

<!--
- o terceiro caso compara 4,65 (por km) com 1,91 (avulso ou não): unidades diferentes. Padronizados, são 8,69 e 0,88.
- extrapolar é aplicar a reta onde não há dados: a relação pode mudar fora da faixa observada.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** a base de viagens, carregada pelo `preparar_base.py` da etapa 3

🧮 &nbsp;**Análise:** o que explica a duração? Resíduos, modelo múltiplo, multicolinearidade e vazamento

<!--
=================================================================
ARQUIVO — etapa8.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Carga e variáveis indicadoras
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from preparar_base import carregar_base

base = carregar_base()
reg = base.dropna(subset=["duracao_min"]).copy()
reg["avulso"] = (reg["tipo_usuario"] == "avulso").astype(int)
reg["choveu"] = reg["choveu"].astype(int)
y = reg["duracao_min"]


def avaliar(colunas):
    X_tr, X_te, y_tr, y_te = train_test_split(reg[colunas], y, test_size=0.2, random_state=42)
    modelo = LinearRegression().fit(X_tr, y_tr)
    prev = modelo.predict(X_te)
    return modelo, r2_score(y_te, prev), root_mean_squared_error(y_te, prev), prev, y_te - prev


# 2. Modelo simples: resíduos no teste
simples, r2, rmse, prev, res = avaliar(["distancia_km"])
plt.scatter(prev, res, s=8)
plt.axhline(0)
plt.show()
(res.abs() > 5).mean(), res.quantile([0.025, 0.975])

# 3. Modelo múltiplo
multiplo, r2_m, rmse_m, _, _ = avaliar(["distancia_km", "avulso", "choveu"])
multiplo.coef_, r2_m, rmse_m

# 4. Multicolinearidade
cols = ["distancia_km", "avulso", "choveu", "chuva_mm", "temp_max"]
reg[cols].corr().round(2)
avaliar(["distancia_km", "avulso", "choveu", "chuva_mm"])[0].coef_

# 5. Coeficientes padronizados
X_tr, X_te, y_tr, y_te = train_test_split(reg[["distancia_km", "avulso", "choveu"]], y,
                                          test_size=0.2, random_state=42)
padr = make_pipeline(StandardScaler(), LinearRegression()).fit(X_tr, y_tr)
padr[-1].coef_, r2_score(y_te, padr.predict(X_te))

# 6. Vazamento: a velocidade sai da própria duração
reg["velocidade_kmh"] = reg["distancia_km"] / (reg["duracao_min"] / 60)
avaliar(["distancia_km", "velocidade_kmh"])[1]
```

>>> Resultados esperados: simples R² 0,925 e RMSE 2,47; P(|resíduo| > 5) = 0,059; quantis −4,71 e 5,63;
>>> múltiplo coef [4,652; 1,914; 1,375], R² 0,932 e RMSE 2,34;
>>> correlação choveu × chuva_mm 0,79; com chuva_mm, choveu 1,27 e chuva_mm 0,006, R² igual;
>>> padronizados [8,69; 0,88; 0,53] e R² 0,932; com velocidade_kmh, R² 0,961 (vazamento).
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para avaliar o modelo, ampliar as preditoras e checar o que não pode entrar**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um analista de dados especialista em Python, pandas e scikit-learn.

# Tarefa
Num notebook, avalie pelos resíduos o modelo de duração da etapa 7 e
construa um modelo múltiplo, checando multicolinearidade e vazamento.

# Contexto
1. Em "etapa8.ipynb", carregue a base com carregar_base() do
   @preparar_base.py e crie as colunas avulso e choveu como 0 e 1.
2. Use sempre train_test_split(test_size=0.2, random_state=42).
3. No modelo só com distancia_km, analise os resíduos no teste: gráfico
   contra o previsto, P(|resíduo| > 5 min) e quantis de 2,5% e 97,5%.
4. Ajuste o modelo com distancia_km, avulso e choveu e compare R² e
   RMSE com os do modelo simples.
5. Mostre a matriz de correlação das preditoras, incluindo chuva_mm e
   temp_max, e o efeito de colocar chuva_mm junto com choveu.
6. Compare os coeficientes padronizados com StandardScaler.
7. Teste velocidade_kmh como preditora e comente o R² obtido.

# Saída e Verificação
- Gere etapa8.ipynb.
- Execute o notebook do início ao fim, sem erros.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: confira se os resíduos e as métricas são do teste, e se a mesma divisão foi usada em todos os modelos.

# 2 - se o agente comemorar o R² de 0,96 com velocidade_kmh sem apontar o vazamento, é a deixa para o slide "Cuidado: variáveis que vêm do alvo".

# 3 - peça a interpretação dos coeficientes e confira cada frase com a tabela do slide de interpretações geradas por IA.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** No dataset mpg do seaborn, correlacione peso, potência e cilindrada.

🛠️ &nbsp;**Exercício \#2:** Compare o modelo só com o peso e o modelo com as três: R², RMSE e coeficientes.

🛠️ &nbsp;**Exercício \#3:** Troque potência e cilindrada pelo ano do modelo e padronize os coeficientes.

🛠️ &nbsp;**Exercício \#4:** Na sua base, ajuste um modelo múltiplo e analise os resíduos no teste.

- [ ] analisar os resíduos contra o previsto
- [ ] interpretar cada coeficiente com as outras variáveis fixas
- [ ] montar a matriz de correlação das preditoras antes do modelo
- [ ] padronizar para comparar coeficientes
- [ ] descartar as variáveis que vêm do alvo

<br/>

<!--
# Exercício #1 — Multicolinearidade no mpg
sns.load_dataset("mpg"): 398 carros, 6 sem horsepower (dropna). Peso × cilindrada 0,93; peso × potência 0,86; mpg × peso −0,83.

# Exercício #2 — Preditoras repetidas
Só o peso: R² 0,653 e RMSE 4,21 mpg (teste, random_state=42). Com peso, potência e cilindrada: R² 0,647, sem ganho.
Em 200 reamostras, o coeficiente da cilindrada vai de −0,019 a 0,008: troca de sinal.

# Exercício #3 — Uma preditora nova de verdade
Peso + ano do modelo: R² 0,794 e RMSE 3,24. Padronizados: peso −5,63 e ano 2,79 (mpg por desvio padrão).
O ano traz informação que o peso não tem (correlação de −0,31 entre os dois).

# Exercício #4 — Base própria
Duas ou três preditoras, a matriz de correlação antes e o gráfico de resíduos depois.

## os exercícios preparam o AT (Exercícios 13 e 14)
-->
