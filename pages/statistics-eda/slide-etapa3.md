---
layout: section
routeAlias: etapa3
---

## **Etapa 3:** Probabilidades e Análise Gráfica

---
layout: section
---

## Pensamento **probabilístico**
**Do valor único à distribuição de valores**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Statistics Every Programmer Needs, cap. 2
source: https://www.manning.com/books/statistics-every-programmer-needs
---

# Do determinístico ao probabilístico

#### **A mesma pergunta pode ter uma resposta única ou uma distribuição de respostas**

::left::

<div class="text-left w-full [&_li]:mb-4">

**Pensamento determinístico**

- "Uma viagem leva 12 minutos."
- Um número só: a média.
- Esconde a variação e o risco.

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

**Pensamento probabilístico**

- "Metade das viagens leva até 10 minutos."
- "Uma em cada 20 passa de 30 minutos."
- Descreve a variação e quantifica o risco.

</div>

<!--
- é o objetivo central da disciplina: trocar o valor único pela distribuição de valores.
- números da base de viagens: média 12,23 min, mediana 9,95 min e P(duração > 30) = 4,9%.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Statistics Every Programmer Needs, cap. 2
source: https://www.manning.com/books/statistics-every-programmer-needs
---

# Três formas de chegar a uma probabilidade

#### **Em análise de dados, a mais usada é a frequência observada**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| tipo | como se calcula | exemplo |
| --- | --- | --- |
| clássica | casos favoráveis ÷ possíveis | dado: P(6) = 1/6 |
| empírica | frequência relativa nos dados | P(avulso) = 29,4% |
| subjetiva | julgamento de quem conhece o negócio | "1 viagem em 10 atrasa" |

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Probabilidade** — um número entre 0 e 1 que mede a chance de um evento.
- **Empírica** — com dados reais, a chance é estimada pela proporção observada.
- **Complemento** — P(não A) = 1 − P(A).

</div>

<!--
- a empírica (ou frequentista) é a base de tudo o que vem a seguir: proporção de casos nos dados.
- a subjetiva aparece no dia a dia de negócio ("acho que..."); os dados servem para conferi-la.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: value_counts
source: https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html
---

# Probabilidade como frequência relativa

#### **A média de uma condição verdadeira ou falsa é a proporção de casos verdadeiros**

::left::

```python [etapa3.ipynb]
avulso = base["tipo_usuario"] == "avulso"
avulso.mean()                    # 0.294

base["tipo_usuario"].value_counts(normalize=True)
# assinante    0.706
# avulso       0.294
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`True` vale 1 e `False` vale 0** — por isso `mean()` devolve a proporção.
- **`value_counts(normalize=True)`** — a frequência relativa de cada categoria.
- **Soma 1** — as probabilidades de todas as categorias somam 1.

</div>

<!--
- base: a base limpa da etapa 2 (3.119 viagens), carregada por carregar_base() do live coding.
- P(avulso) = 0,294: quase 3 em cada 10 viagens são de usuários avulsos.
-->

---
layout: two-cols-header
layoutClass: gap-8
---

# Regra da adição

#### **Para "A ou B", some as chances e desconte a sobreposição**

::left::

$$
P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

```python [etapa3.ipynb]
chuva = base["choveu"]       # chuva_mm > 5 no dia

(avulso.mean() + chuva.mean()
 - (avulso & chuva).mean())  # 0.294 + 0.184 - 0.055
(avulso | chuva).mean()      # 0.423: confere
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **A ∪ B (ou)** — a viagem é avulsa, foi num dia de chuva ou as duas coisas.
- **A ∩ B (e)** — as duas ao mesmo tempo: 5,5% das viagens.
- **Sem o desconto** — a interseção seria contada duas vezes.

</div>

<!--
- 0,294 + 0,184 − 0,055 = 0,423, igual à contagem direta com | (ou).
- & é o "e" e | é o "ou" entre máscaras, como nos filtros da etapa 2.
-->

---
layout: two-cols-header
layoutClass: gap-8
---

# Condicional e regra da multiplicação

#### **"Dado que choveu" muda o denominador: só os dias de chuva entram na conta**

::left::

$$
P(B \mid A) = \frac{P(A \cap B)}{P(A)} \qquad P(A \cap B) = P(A) \cdot P(B \mid A)
$$

```python [etapa3.ipynb]
reg = base.dropna(subset=["duracao_min"])
longa = reg["duracao_min"] > 30

longa[reg["choveu"]].mean()     # 0.070
longa[~reg["choveu"]].mean()    # 0.044
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **P(longa \| chuva)** — entre as viagens em dias de chuva, 7,0% passam de 30 min.
- **Sem chuva** — a chance cai para 4,4%.
- **Multiplicação** — P(chuva e longa) = P(chuva) × P(longa \| chuva).

</div>

<!--
- reg: só as viagens com duração registrada (a duração ausente não pode virar "curta").
- erro comum: dividir pelo total de viagens em vez de dividir só pelas viagens em dias de chuva.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: crosstab
source: https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html
---

# Eventos independentes

#### **Se saber A não muda a chance de B, os eventos são independentes**

::left::

$$
P(A \cap B) = P(A) \cdot P(B)
$$

```python [etapa3.ipynb]
pd.crosstab(base["tipo_usuario"], base["choveu"],
            normalize="all")
# choveu      False   True
# assinante   0.577  0.130
# avulso      0.239  0.055

avulso.mean() * chuva.mean()    # 0.054
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Tipo de usuário e chuva** — conjunta 0,055 e produto 0,054: na prática, independentes.
- **Viagem longa e chuva** — 7,0% com chuva contra 4,4% sem: dependentes.
- **`normalize="all"`** — a tabela mostra as probabilidades conjuntas.

</div>

> [!NOTE]
> Comparar números é uma verificação, não um teste formal: o teste de hipótese vem na etapa 6.

<!--
- independência: P(avulso | chuva) = 0,297 é quase igual a P(avulso) = 0,294.
- a chuva não muda quem pedala, mas muda quanto tempo a viagem dura.
-->

---
layout: section
---

## Variáveis aleatórias e **distribuições**
**PMF, PDF e CDF**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Statistics Every Programmer Needs, cap. 2
source: https://www.manning.com/books/statistics-every-programmer-needs
---

# Variáveis aleatórias discretas e contínuas

#### **O tipo da variável define a função que descreve a sua distribuição**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| coluna | tipo | descrita por |
| --- | --- | --- |
| `avaliacao` | discreta (notas de 1 a 5) | PMF |
| `duracao_min` | contínua | PDF e CDF |
| `distancia_km` | contínua | PDF e CDF |
| `tipo_usuario` | categórica | proporção por categoria |

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Discreta** — valores contáveis e separados: P(nota = 4) faz sentido.
- **Contínua** — qualquer valor num intervalo: pergunta-se pela chance de uma faixa.
- **Categórica** — rótulos, sem valor numérico; descrita pela proporção de cada categoria.

</div>

<!--
- numa variável contínua, a chance de um valor exato (12,0000 min) é zero: por isso se usa a faixa.
- a categórica não é uma variável aleatória numérica; ainda assim, cada categoria tem a sua probabilidade.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Statistics Every Programmer Needs, cap. 2
source: https://www.manning.com/books/statistics-every-programmer-needs
---

# PMF: a probabilidade de cada valor

#### **Numa variável discreta, cada valor tem a sua probabilidade, e todas somam 1**

::left::

```python [etapa3.ipynb]
pmf = (base["avaliacao"].dropna()
       .value_counts(normalize=True)
       .sort_index())

pmf.sum()           # 1.0
pmf.loc[4:].sum()   # P(nota >= 4) = 0.954
```

<div class="text-left w-full [&_li]:mb-2">

- **PMF** — função de massa de probabilidade: $P(X = x)$.
- **Faixas** — somam-se os valores: P(nota ≥ 4) = 29,3% + 66,1%.

</div>

::right::

<AssetImg src="eda-pmf-avaliacao.png" class="rounded-lg w-full" />

<!--
- nenhuma viagem recebeu nota 1; a nota 5 sozinha tem 66,1%.
- dropna: 482 viagens não foram avaliadas e ficam fora da PMF.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: ecdfplot
source: https://seaborn.pydata.org/generated/seaborn.ecdfplot.html
---

# PDF e CDF

#### **Numa variável contínua, a probabilidade está numa faixa de valores**

::left::

<div class="text-left w-full [&_li]:mb-2">

- **PDF** — densidade: a probabilidade é a área sob a curva numa faixa.
- **CDF** — F(x) = P(X ≤ x): a proporção acumulada até x.
- **Cauda** — P(X > x) = 1 − F(x).

</div>

```python [etapa3.ipynb]
f30 = (reg["duracao_min"] <= 30).mean()  # 0.951
1 - f30                                  # 0.049
sns.ecdfplot(data=reg, x="duracao_min")
```

::right::

<AssetImg src="eda-ecdf-duracao.png" class="rounded-lg w-full" />

<!--
- CDF empírica: a proporção das viagens observadas até cada valor.
- leitura para o negócio: 95,1% das viagens terminam em até 30 min; o risco de passar disso é de 4,9%.
- erro comum: ler F(30) como "a chance de durar exatamente 30 min".
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.random
source: https://numpy.org/doc/stable/reference/random/generator.html
---

# Demo: probabilidade por simulação

#### **Gerar muitos casos e contar é um jeito direto de estimar uma probabilidade**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

rng = np.random.default_rng(42)
duracao = rng.gamma(2.0, 6.0, size=10_000)

print("F(30)            =", (duracao <= 30).mean())
print("P(duração > 30)  =", (duracao > 30).mean())
print("P(10 < dur ≤ 20) =", ((duracao > 10) & (duracao <= 20)).mean())
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Simulação** — 10 mil viagens sorteadas de uma distribuição assimétrica.
- **Faixas** — P(10 < X ≤ 20) = F(20) − F(10).
- **Antes de executar** — qual faixa deve ter mais viagens?

</div>

<!--
- a gama(2; 6) tem média 12 min, perto da duração média da base de viagens.
- o valor exato de P(X > 30) para essa gama é 0,040: a simulação chega perto.
-->

---
layout: section
---

## Análise **gráfica**
**Histogramas e boxplots**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: histplot
source: https://seaborn.pydata.org/generated/seaborn.histplot.html
---

# Histograma: a forma da distribuição

#### **Muitas viagens curtas e uma cauda de viagens longas: assimetria à direita**

::left::

```python [etapa3.ipynb]
sns.histplot(data=reg, x="duracao_min", bins=30)

reg["duracao_min"].describe()
# mean 12.23 | 50% 9.95 | std 9.17
reg["duracao_min"].skew()        # 1.66
```

<div class="text-left w-full [&_li]:mb-2">

- **Assimetria à direita** — a cauda puxa a média (12,23) para cima da mediana (9,95).
- **`skew()`** — mede a assimetria: 0 é simétrica, positivo tem cauda à direita.

</div>

::right::

<AssetImg src="eda-hist-duracao.png" class="rounded-lg w-full" />

<!--
- describe() mostra média, desvio padrão, mínimo, quartis e máximo de uma vez.
- em dados assimétricos, a mediana representa melhor a viagem típica do que a média.
-->

---
layout: default
---

# Quantos bins?

#### **Poucos bins escondem a forma; bins demais transformam ruído em forma**

<div class="h-4" />

<AssetImg src="eda-bins-duracao.png" class="rounded-lg w-full" />

<div class="h-4" />

- **5 bins** só mostram que a maioria das viagens é curta; **30 bins** revelam a cauda; **200 bins** exibem o ruído da amostra.

<!--
- não existe número certo de bins: teste alguns e justifique a escolha.
- o seaborn escolhe um número de bins automaticamente quando bins não é informado.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: boxplot
source: https://seaborn.pydata.org/generated/seaborn.boxplot.html
---

# Boxplot: quartis e outliers

#### **Cinco números resumem a distribuição e apontam os valores atípicos**

::left::

```python [etapa3.ipynb]
sns.boxplot(data=reg, x="tipo_usuario",
            y="duracao_min")

q1, q3 = reg["duracao_min"].quantile([0.25, 0.75])
limite = q3 + 1.5 * (q3 - q1)          # 31.81
(reg["duracao_min"] > limite).sum()    # 119
```

<div class="text-left w-full [&_li]:mb-2">

- **Caixa** — do Q1 ao Q3, os 50% centrais; a linha é a mediana.
- **Outlier** — além de 1,5 × IQR a partir da caixa, com $\text{IQR} = Q_3 - Q_1$.

</div>

::right::

<AssetImg src="eda-boxplot-duracao.png" class="rounded-lg w-full" />

<!--
- avulsos têm mediana maior (11,2 contra 9,6 min): pedalam mais devagar.
- outlier não é erro: é uma viagem atípica que merece ser olhada antes de qualquer decisão.
- o seaborn 0.13 pode emitir um aviso de depreciação do matplotlib 3.11 no boxplot; vem da biblioteca, não do código do aluno.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: scipy.stats.norm
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
---

# Assimetria e a curva normal

#### **Supor normalidade sem olhar os dados pode errar justamente a cauda**

::left::

<div class="text-left w-full [&_li]:mb-2">

- **Cauda** — a normal com a mesma média e desvio prevê 2,6% de viagens acima de 30 min; nos dados, são 4,9%.
- **Valores impossíveis** — ela põe 9% das viagens com duração negativa.
- **Alternativas** — dados positivos e assimétricos costumam seguir famílias como a gama.

</div>

```python [etapa3.ipynb]
from scipy import stats

m, s = reg["duracao_min"].mean(), reg["duracao_min"].std()
1 - stats.norm.cdf(30, m, s)   # 0.026
```

::right::

<AssetImg src="eda-normal-duracao.png" class="rounded-lg w-full" />

<!--
- stats.norm.cdf é a CDF da normal: o mesmo F(x) do slide de CDF, agora para uma curva teórica.
- o desenho: histograma com stat="density" e a curva stats.norm.pdf sobreposta.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** a base de viagens limpa da etapa 2, agora carregada por um módulo `preparar_base.py`

🌧️ &nbsp;**Análise:** a chuva muda a chance de uma viagem longa? Probabilidades e gráficos da duração

<!--
Projeto: uv add matplotlib seaborn scipy (além do que já foi instalado nas etapas 1 e 2).

=================================================================
ARQUIVO 1 — preparar_base.py (na mesma pasta dos dados)

```python
import pandas as pd


def carregar_base() -> pd.DataFrame:
    """Repete o pipeline da etapa 2 (concat, tipos, duplicatas e merge), sem preencher duracao_min."""
    viagens = pd.concat([pd.read_csv("viagens.csv"), pd.read_csv("viagens_abril.csv")],
                        ignore_index=True)
    viagens["duracao_min"] = viagens["duracao_min"].str.replace(",", ".").astype(float)
    viagens["data_inicio"] = viagens["data_inicio"].astype("datetime64[ns]")
    viagens["tipo_usuario"] = viagens["tipo_usuario"].astype("category")
    viagens = viagens.drop_duplicates(subset="viagem_id")

    estacoes = pd.read_excel("estacoes.xlsx")
    clima = pd.read_json("clima.json")
    clima["data"] = clima["data"].astype("datetime64[ns]")

    base = (viagens
            .merge(estacoes, left_on="estacao_origem", right_on="estacao_id", how="left")
            .merge(clima, left_on="data_inicio", right_on="data", how="left"))
    base["choveu"] = base["chuva_mm"] > 5
    return base
```

>>> Sem preencher a duração: a mediana preenchida criaria um pico artificial no histograma e na CDF.

=================================================================
ARQUIVO 2 — etapa3.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Carga
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from preparar_base import carregar_base

base = carregar_base()

# 2. Probabilidades: avulso e chuva
avulso = base["tipo_usuario"] == "avulso"
chuva = base["choveu"]
avulso.mean(), chuva.mean(), (avulso & chuva).mean()
avulso.mean() + chuva.mean() - (avulso & chuva).mean(), (avulso | chuva).mean()
avulso[chuva].mean(), avulso.mean()
pd.crosstab(base["tipo_usuario"], base["choveu"], normalize="all")

# 3. Viagem longa, entre as viagens com duração registrada
reg = base.dropna(subset=["duracao_min"])
longa = reg["duracao_min"] > 30
longa.mean(), longa[reg["choveu"]].mean(), longa[~reg["choveu"]].mean()

# 4. PMF da avaliação e CDF da duração
base["avaliacao"].dropna().value_counts(normalize=True).sort_index()
(reg["duracao_min"] <= 30).mean()
sns.ecdfplot(data=reg, x="duracao_min")

# 5. Histograma, boxplot e outliers
sns.histplot(data=reg, x="duracao_min", bins=30)
reg["duracao_min"].describe()
sns.boxplot(data=reg, x="tipo_usuario", y="duracao_min")
q1, q3 = reg["duracao_min"].quantile([0.25, 0.75])
(reg["duracao_min"] > q3 + 1.5 * (q3 - q1)).sum()

# 6. Assimetria e normal
m, s = reg["duracao_min"].mean(), reg["duracao_min"].std()
reg["duracao_min"].skew(), 1 - stats.norm.cdf(30, m, s), stats.norm.cdf(0, m, s)
sns.histplot(data=reg, x="duracao_min", bins=40, stat="density")
x = np.linspace(-20, 80, 300)
plt.plot(x, stats.norm.pdf(x, m, s))
```

>>> Resultados esperados: P(avulso) 0,294; P(chuva) 0,184; P(avulso e chuva) 0,055; P(avulso ou chuva) 0,423;
>>> P(avulso | chuva) 0,297 (independentes); P(longa) 0,049, com chuva 0,070, sem chuva 0,044 (dependentes);
>>> PMF: nota 5 = 66,1%, nota 4 = 29,3%; F(30) = 0,951; média 12,23, mediana 9,95, skew 1,66;
>>> limite 31,81 e 119 outliers; normal: P(>30) = 0,026 e P(<0) = 0,091.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para investigar a chuva com probabilidades e gráficos**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um analista de dados especialista em Python, pandas e estatística.

# Tarefa
Investigue, num notebook, se a chuva muda a chance de uma viagem longa,
usando probabilidades, distribuições e gráficos da duração das viagens.

# Contexto
1. Crie "preparar_base.py" com uma função carregar_base() que repete o
   pipeline do @etapa2.ipynb (concat, tipos, duplicatas e merge com
   estações e clima), sem preencher duracao_min, e cria a coluna
   choveu (chuva_mm > 5).
2. Em "etapa3.ipynb", importe carregar_base() e calcule, por frequência
   relativa, P(avulso), P(chuva), a regra da adição para "avulso ou
   chuva" e P(avulso | chuva), verificando se os eventos são
   independentes.
3. Entre as viagens com duração registrada, compare P(duração > 30 min)
   com e sem chuva.
4. Mostre a PMF de avaliacao e a CDF empírica de duracao_min (F(30)).
5. Faça o histograma da duração (bins=30) e o boxplot da duração por
   tipo_usuario, e conte os outliers pela regra de 1,5 × IQR.
6. Calcule a assimetria e compare o histograma com uma normal de mesma
   média e desvio padrão.
7. Antes de cada passo, crie uma célula de markdown explicando o passo.

# Saída e Verificação
- Gere preparar_base.py e etapa3.ipynb.
- Instale com uv add as dependências que faltarem.
- Execute o notebook do início ao fim, sem erros.
```
</WindowMockup>

<!--
# 1 - o @ dá ao agente o pipeline pronto da etapa 2; o módulo preparar_base.py evita repetir código nos notebooks seguintes.

# 2 - human-in-the-loop: confira se o agente usou só as viagens com duração registrada no passo 3, e se não preencheu a duração.

# 3 - se o agente concluir independência ou dependência "de olho", peça a comparação numérica.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** No Gapminder de 2007, calcule P(lifeExp > 70) no mundo e por continente.

🛠️ &nbsp;**Exercício \#2:** Faça o histograma da expectativa de vida de 2007 e descreva a assimetria.

🛠️ &nbsp;**Exercício \#3:** Faça o boxplot da expectativa de vida por continente e identifique os outliers.

🛠️ &nbsp;**Exercício \#4:** Na sua base, calcule uma probabilidade condicional e a CDF de uma coluna.

- [ ] calcular probabilidades com `mean()` sobre condições
- [ ] aplicar as regras da adição e da multiplicação
- [ ] comparar P(A e B) com P(A) × P(B)
- [ ] descrever uma variável discreta pela PMF e uma contínua pela CDF
- [ ] ler a assimetria no histograma e os outliers no boxplot

<br/>

<!--
# Exercício #1 — Probabilidade no Gapminder
g7 = df[df["year"] == 2007]; (g7["lifeExp"] > 70).mean() -> 0,585 (142 países).
Por continente: África 13,5%, Américas 88%, Ásia 66,7%, Europa e Oceania 100%.
É uma probabilidade condicional: P(lifeExp > 70 | continente).

# Exercício #2 — Histograma
Média 67,0 e mediana 71,9: assimetria à ESQUERDA (skew −0,69), o contrário da duração das viagens.
Bom para mostrar que a média fica do lado da cauda.

# Exercício #3 — Boxplot por continente
sns.boxplot(data=g7, x="continent", y="lifeExp"). Outliers pela regra do IQR: Haiti (Américas) e Afeganistão (Ásia).

# Exercício #4 — Base própria
Reaproveite a base gerada no hands-on das etapas 1 e 2: uma condicional "dado que..." e a CDF empírica de uma coluna contínua.

## os exercícios preparam o TP2 (Exercícios 1 a 4 e 8 a 10)
-->
