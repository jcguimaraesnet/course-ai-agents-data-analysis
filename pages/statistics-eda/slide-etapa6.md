---
layout: section
routeAlias: etapa6
---

## **Etapa 6:** Avaliação de Hipóteses com IA

---
layout: section
---

## Teste de **hipótese**
**Diferença real ou ruído da amostra?**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 3
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Diferença real ou ruído?

#### **Uma amostra nunca repete a outra: parte de qualquer diferença é acaso**

::left::

```python [etapa6.ipynb]
base = carregar_base()
av = base.dropna(subset=["avaliacao"])

(av.groupby("tipo_usuario")["avaliacao"]
   .agg(["mean", "count"]).round(2))
#              mean  count
# assinante    4.63   1867
# avulso       4.57    770
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Amostra** — as 2.637 viagens avaliadas são uma parte de todas as viagens possíveis.
- **Ruído amostral** — outra amostra daria outras médias, e uma diferença pequena pode surgir só por acaso.
- **A pergunta** — 0,05 ponto é diferença demais para ser só acaso?

</div>

<!--
- a etapa 5 terminou com essa pergunta: a diferença entre avulsos e assinantes é real ou ruído?
- a chuva também muda a nota (4,68 sem chuva e 4,32 com chuva), mas com uma diferença sete vezes maior.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: permutation_test
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html
---

# Hipótese nula e p-valor

#### **O teste supõe que não há diferença e mede quão raro seria o que você observou**

::left::

$$
H_0: \mu_{\text{avulso}} = \mu_{\text{assinante}} \qquad H_1: \mu_{\text{avulso}} \neq \mu_{\text{assinante}}
$$

<div class="text-left w-full [&_li]:mb-3">

- **Sob H₀** — embaralhar os rótulos simula as diferenças que surgem só por acaso.
- **p-valor** — a fração das simulações com diferença tão extrema quanto a observada: 3,3%.
- **α = 0,05** — a regra usual: com p abaixo de α, rejeita-se H₀.

</div>

::right::

<AssetImg src="eda-permutacao-avaliacao.png" class="rounded-lg w-full" />

<!--
- a distribuição do gráfico é a distribuição amostral da diferença sob H₀: o que se veria se o tipo de usuário não mudasse a nota.
- o p-valor é bilateral: conta as duas caudas, porque H₁ não diz quem avalia melhor.
- α é o risco aceito de rejeitar H₀ quando ela é verdadeira (falso positivo).
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.random
source: https://numpy.org/doc/stable/reference/random/generator.html
---

# Demo: p-valor por simulação

#### **Embaralhe os rótulos e conte quantas vezes o acaso alcança a diferença observada**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

notas = [2, 3, 4, 5]
avulso = np.repeat(notas, [3, 33, 253, 481])
assinante = np.repeat(notas, [4, 81, 519, 1263])
obs = avulso.mean() - assinante.mean()

rng = np.random.default_rng(42)
todas = np.concatenate([avulso, assinante])
difs = []
for _ in range(5_000):
    p = rng.permutation(todas)    # embaralha
    difs.append(p[:770].mean() - p[770:].mean())
p_valor = np.mean(np.abs(difs) >= abs(obs))
print("diferença observada:", round(obs, 3))
print("p-valor:", round(p_valor, 3))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Notas reais** — as contagens de cada nota recriam as avaliações dos dois grupos.
- **Embaralhar** — sob H₀, ser avulso ou assinante não muda a nota.
- **Antes de executar** — o p-valor vai ficar acima ou abaixo de 0,05?

</div>

<!--
- saída esperada: diferença −0,055 e p-valor 0,033, perto dos 0,030 do teste t de Welch do próximo slide.
- é um teste de permutação; o scipy.stats.permutation_test faz o mesmo em uma linha.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: ttest_ind
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
---

# Testes clássicos no SciPy

#### **Cada pergunta tem o seu teste; todos devolvem um p-valor**

::left::

```python [etapa6.ipynb]
from scipy import stats

avulso = av.loc[av["tipo_usuario"] == "avulso", "avaliacao"]
assinante = av.loc[av["tipo_usuario"] == "assinante",
                   "avaliacao"]

stats.ttest_ind(avulso, assinante, equal_var=False)
# statistic=-2.17, pvalue=0.030
stats.mannwhitneyu(avulso, assinante)
# pvalue=0.015
```

> [!CAUTION]
> Com `NaN` nos dados, o `ttest_ind` devolve `pvalue=nan`: tire os ausentes antes de testar.

::right::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| para comparar | teste |
| --- | --- |
| as médias de dois grupos independentes | `ttest_ind(a, b, equal_var=False)` |
| notas, postos ou dados assimétricos | `mannwhitneyu(a, b)` |
| duas variáveis categóricas | `chi2_contingency(tabela)` |

</div>

<!--
- equal_var=False é o teste t de Welch: não supõe que os dois grupos têm a mesma variância.
- o Mann-Whitney compara as distribuições pelos postos; serve para notas de 1 a 5, que não são contínuas.
- erro comum em código gerado: ttest_rel, que é para amostras pareadas (a mesma unidade medida duas vezes).
- alternativa ao dropna: nan_policy="omit".
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: chi2_contingency
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
---

# O teste de independência da etapa 3

#### **O qui-quadrado confirma o que as probabilidades da etapa 3 sugeriam**

::left::

```python [etapa6.ipynb]
tab = pd.crosstab(base["tipo_usuario"], base["choveu"])
stats.chi2_contingency(tab).pvalue     # 0.87

reg = base.dropna(subset=["duracao_min"])
tab = pd.crosstab(reg["duracao_min"] > 30, reg["choveu"])
stats.chi2_contingency(tab).pvalue     # 0.017
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Tipo de usuário e chuva** — p = 0,87: os dados são compatíveis com a independência.
- **Viagem longa e chuva** — p = 0,017: a chuva muda a chance de uma viagem longa.
- **Qui-quadrado** — compara as contagens observadas com as esperadas se as variáveis fossem independentes.

</div>

<!--
- na etapa 3, comparar P(A e B) com P(A) × P(B) foi só uma verificação: aqui vem o teste formal.
- P(longa | chuva) = 7,0% contra 4,4% sem chuva.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 3
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# O que o p-valor não diz

#### **Ele responde "é acaso?", e não "a diferença importa?"**

::left::

<div class="text-left w-full [&_li]:mb-3">

- **Não é a chance de H₀ ser verdadeira** — ele é calculado supondo que H₀ é verdadeira.
- **Não mede o tamanho da diferença** — p = 0,03 para uma diferença de 0,05 ponto.
- **p > 0,05 não prova igualdade** — pode faltar amostra para enxergar a diferença.
- **Depende do tamanho da amostra** — com muitos dados, até diferenças mínimas ficam "significativas".

</div>

::right::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| comparação | diferença | p-valor (Welch) |
| --- | --- | --- |
| chuva × sem chuva | −0,36 ponto | 1 × 10⁻²⁴ |
| avulso × assinante | −0,05 ponto | 0,03 |

</div>

<div class="h-4" />

> [!NOTE]
> As duas diferenças são significativas, mas só uma tem tamanho para mudar uma decisão.

<!--
- o capítulo 3 do livro critica justamente isso: a IA generativa tende a sugerir o teste com p-valor por ser o mais popular, e não o mais informativo.
- a seguir: o p-valor muda com o n, mesmo com a diferença fixa.
-->

---
layout: two-cols-header
layoutClass: gap-8
---

# Demo: a mesma diferença, outra amostra

#### **Fixe a diferença, aumente o número de viagens e veja o p-valor cair**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import math

dif = 0.05   # diferença de 0,05 ponto
dp = 0.6     # desvio padrão das notas

for n in [100, 1_000, 10_000, 100_000]:
    z = dif / (dp * math.sqrt(2 / n))
    p = math.erfc(z / math.sqrt(2))   # bilateral
    print(f"n = {n:>6} por grupo -> p = {p:.2g}")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **A diferença não muda** — 0,05 ponto em todas as linhas.
- **O p-valor despenca** — de 0,56 com 100 viagens por grupo para quase zero com 100 mil.
- **Lição** — um p-valor pequeno não quer dizer uma diferença grande.

</div>

<!--
- é a aproximação normal do teste de duas médias, que vale para amostras grandes.
- 0,6 é perto do desvio padrão das notas da base (0,58).
- peça para a turma prever a partir de qual n o p-valor fica abaixo de 0,05.
-->

---
layout: section
---

## Intervalos de **confiança**
**O tamanho da diferença e a incerteza em torno dele**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 3
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Intervalo de confiança

#### **Uma faixa de valores plausíveis, e não um número só**

::left::

<div class="text-left w-full [&_li]:mb-4">

- **Faixa plausível** — os valores da média que são compatíveis com os dados.
- **95% de confiança** — repetindo a amostragem muitas vezes, 95% dos intervalos conteriam a média real: no gráfico, 19 de 20.
- **Largura** — mais dados e menos variação deixam o intervalo mais estreito.
- **Mais que o p-valor** — mostra o tamanho da diferença e a incerteza em torno dele.

</div>

::right::

<AssetImg src="eda-ic-cobertura.png" class="rounded-lg w-full" />

<!--
- simulação: 20 amostras de 100 notas tiradas de uma população com média conhecida (4,57); cada linha é o IC 95% de uma amostra.
- a confiança é do método: um intervalo específico contém ou não contém a média real.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 3
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Bootstrap: reamostrar os próprios dados

#### **A amostra faz o papel da população, e a variação das reamostras mede a incerteza**

::left::

<div class="text-left w-full [&_li]:mb-3">

- **Reamostra** — sorteie 770 notas, com reposição, entre as 770 notas dos avulsos.
- **Repita** — 5.000 reamostras dão 5.000 médias: uma estimativa da distribuição amostral.
- **IC 95%** — dos percentis 2,5 a 97,5 dessas médias: de 4,531 a 4,614.
- **Sem fórmula** — serve para a média, a mediana ou uma diferença entre grupos.

</div>

::right::

<AssetImg src="eda-bootstrap-avaliacao.png" class="rounded-lg w-full" />

<!--
- com reposição, uma nota pode sair mais de uma vez numa reamostra, e outra pode não sair.
- é o método do capítulo 3 do livro para comparar grupos por intervalo de confiança, no lugar do teste t.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.random
source: https://numpy.org/doc/stable/reference/random/generator.html
---

# Demo: bootstrap à mão

#### **Sortear com reposição, calcular a média e repetir**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

notas = [2, 3, 4, 5]
avulso = np.repeat(notas, [3, 33, 253, 481])
rng = np.random.default_rng(42)

medias = []
for _ in range(5_000):
    r = rng.choice(avulso, size=770)
    medias.append(r.mean())

baixo, alto = np.percentile(medias, [2.5, 97.5])
print(f"média observada: {avulso.mean():.3f}")
print(f"IC 95%: de {baixo:.3f} a {alto:.3f}")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`rng.choice`** — sorteia com reposição: cada reamostra tem o tamanho da amostra original.
- **Percentis** — 2,5% e 97,5% das médias delimitam o IC 95%.
- **Antes de executar** — o intervalo dos avulsos vai conter a nota média dos assinantes (4,63)?

</div>

<!--
- saída esperada: média 4,574 e IC de 4,531 a 4,614.
- o intervalo não chega a 4,63; mesmo assim, o dos assinantes começa em 4,60: os dois se sobrepõem (slide "A sobreposição engana").
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: bootstrap
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
---

# Bootstrap com o SciPy

#### **`scipy.stats.bootstrap` faz as reamostras e corrige o intervalo**

::left::

```python [etapa6.ipynb]
import numpy as np

res = stats.bootstrap((avulso,), np.mean,
                      confidence_level=0.95,
                      rng=np.random.default_rng(42))
res.confidence_interval
# low=4.530, high=4.614
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`(avulso,)`** — os dados vão numa tupla, mesmo com um grupo só.
- **Sem `NaN`** — com ausentes, o intervalo sai `nan`: use só as viagens avaliadas.
- **BCa** — o método padrão ajusta o intervalo ao viés e à assimetria das reamostras.

</div>

> [!CAUTION]
> Sem a tupla, `stats.bootstrap(avulso, np.mean)` falha com `AxisError`.

<!--
- o padrão é n_resamples=9999; o rng existe desde o SciPy 1.15, e código mais antigo (de muitos LLMs, inclusive) usa random_state, que ainda funciona.
- com NaN, o SciPy só emite um DegenerateDataWarning e devolve (nan, nan).
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: bootstrap
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
---

# O intervalo da diferença

#### **Para comparar dois grupos, calcule o intervalo da diferença entre as médias**

::left::

```python [etapa6.ipynb]
def diferenca(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)

res = stats.bootstrap((avulso, assinante), diferenca,
                      rng=np.random.default_rng(42))
res.confidence_interval
# low=-0.105, high=-0.006
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Dois grupos na tupla** — o bootstrap reamostra cada grupo separadamente.
- **`axis`** — permite ao SciPy calcular milhares de reamostras de uma vez.
- **O zero ficou de fora** — a diferença existe, e é pequena: no máximo 0,1 ponto.

</div>

<!--
- chuva menos sem chuva: de −0,43 a −0,30. O intervalo também mostra o tamanho, e não só se a diferença existe.
- a ordem da tupla define o sinal: (avulso, assinante) dá avulso menos assinante.
-->

---
layout: default
sourceLabel: bootstrap
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
---

# A sobreposição engana

#### **Os intervalos dos grupos se sobrepõem, e mesmo assim o da diferença não contém o zero**

<div class="h-4" />

<AssetImg src="eda-sobreposicao-ic.png" class="rounded-lg w-full" />

<div class="h-4" />

- **Decida pelo intervalo da diferença** — a sobreposição dos intervalos de cada grupo não prova que a diferença é nula.

<!--
- a incerteza da diferença é menor que a soma das incertezas dos dois grupos: por isso dois intervalos de 95% podem se sobrepor com uma diferença significativa.
- o inverso vale: intervalos que não se sobrepõem indicam diferença, mas não dizem se ela é grande o bastante para importar.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 3
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Significância estatística x relevância prática

#### **A diferença é real; ela é grande o bastante para mudar uma decisão?**

::left::

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| comparação | diferença (IC 95%) | d de Cohen |
| --- | --- | --- |
| chuva × sem chuva | −0,36 (−0,43 a −0,30) | −0,64 |
| avulso × assinante | −0,05 (−0,10 a −0,01) | −0,09 |

</div>

::right::

<div class="text-left w-full [&_li]:mb-4">

- **As duas são significativas** — nenhum dos intervalos contém o zero.
- **d de Cohen** — a diferença em desvios padrão: perto de 0,2 é pequena; de 0,5, média; de 0,8, grande.
- **Relevância** — é decisão do negócio: quanto de nota justifica mudar a operação?

</div>

<!--
- d = diferença das médias dividida pelo desvio padrão combinado dos dois grupos.
- com chuva, a proporção de notas 5 cai de 71% para 44%; entre avulsos e assinantes, de 68% para 62%.
-->

---
layout: section
---

## Interpretações **geradas por IA**
**O LLM ajuda a estudar; os dados conferem**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 4
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Peça a explicação e confira

#### **Use o LLM para estudar o conceito, mas valide a resposta antes de aceitá-la**

::left::

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt" codeblock>

```md
O teste t de Welch deu p = 0,03 para a diferença de
nota entre avulsos e assinantes. Explique o que esse
p-valor representa, o que posso e o que não posso
concluir dele e como ele se relaciona com a
distribuição amostral da diferença.
```
</WindowMockup>

::right::

<div class="text-left w-full [&_li]:mb-3">

**A explicação está completa se:**

- diz que o p-valor é calculado supondo H₀ verdadeira;
- liga o p-valor à distribuição da diferença sob H₀;
- avisa que ele não mede o tamanho da diferença;
- não o trata como a chance de H₀ ser verdadeira.

</div>

<!--
- o capítulo 4 do livro trata a IA como intérprete de resultados, sempre confrontando a narrativa com os números reais.
- peça também o intervalo de confiança: compare a explicação do LLM com os slides de IC.
-->

---
layout: default
sourceLabel: Starting Data Analytics with Generative AI, cap. 4
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Erros comuns nas interpretações de um LLM

#### **Cada afirmação tem um jeito de ser conferida com os dados**

<div class="h-2" />

<div class="text-sm leading-tight [&_td]:py-2 [&_th]:py-1">

| o LLM afirma | o problema | confira com |
| --- | --- | --- |
| "p = 0,03: há só 3% de chance de não haver diferença" | o p-valor supõe H₀ verdadeira; não é a chance de H₀ | a definição do p-valor |
| "a diferença é significativa, portanto importante" | significância não mede o tamanho | o IC da diferença e o d de Cohen |
| "os intervalos se sobrepõem: não há diferença" | a sobreposição não prova igualdade | o IC da diferença |
| "os avulsos estão menos satisfeitos com o serviço" | a diferença pode vir de uma terceira variável | a comparação dentro de faixas de duração |
| "a nota média nos dias de chuva é 4,1" | um número que não saiu do código | o resultado do `groupby` |

</div>

<!--
- o último caso é a alucinação numérica: o LLM escreve um número plausível, e não o calculado.
- a terceira variável é a lição de causalidade da etapa 4, agora aplicada a uma interpretação gerada por IA.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Starting Data Analytics with Generative AI, cap. 4
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Confira cada frase com os dados

#### **Uma interpretação gerada por IA, revisada frase por frase**

::left::

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="resposta do LLM" codeblock>

```md
1. A nota média dos avulsos (4,57) é menor que
   a dos assinantes (4,63).
2. Com p = 0,03, há 97% de chance de a
   diferença ser real.
3. Os intervalos de 95% se sobrepõem, então a
   diferença pode ser só ruído.
4. A empresa deve melhorar a experiência dos
   usuários avulsos.
```
</WindowMockup>

::right::

<div class="text-left w-full [&_li]:mb-3">

- **1 ✅** — confere com o `groupby`.
- **2 ❌** — o p-valor não é a chance de a diferença ser real.
- **3 ❌** — o IC da diferença (−0,10 a −0,01) não contém o zero.
- **4 ❌** — entre as viagens de até 25 min, a diferença cai para 0,02 (p = 0,32): ela vem da duração, porque os avulsos pedalam mais devagar.

</div>

<!--
- a resposta é um exemplo montado com erros comuns, para treinar a revisão.
- a frase 4 recomenda uma ação a partir de uma diferença pequena e explicada por outra variável: a duração (avulsos fazem mais viagens acima de 25 min, 12% contra 8%).
-->

---
layout: default
sourceLabel: Starting Data Analytics with Generative AI, cap. 4
source: https://www.manning.com/books/starting-data-analytics-with-generative-ai-and-python
---

# Gráficos gerados por IA

#### **Com o eixo recortado, 0,05 ponto parece uma diferença enorme**

<div class="h-4" />

<AssetImg src="eda-eixo-recortado.png" class="rounded-lg w-full" />

<div class="h-4" />

- **Barras começam no zero** — a altura da barra é o valor; recortar o eixo distorce a comparação.
- **Mostre a incerteza** — o IC ou a distribuição das notas mostra o que a média esconde.

<!--
- confira no gráfico gerado: o tipo de gráfico, o início do eixo e o que a agregação esconde.
- para ver uma diferença pequena de perto, use pontos com o IC, e não barras com o eixo recortado.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** a base de viagens, carregada pelo `preparar_base.py` da etapa 3

🌧️ &nbsp;**Análise:** a chuva derruba a avaliação? Teste, intervalos de confiança e a interpretação do LLM conferida com os dados

<!--
Projeto: o scipy já foi instalado na etapa 3 (uv add matplotlib seaborn scipy).

=================================================================
ARQUIVO — etapa6.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Carga: só as viagens avaliadas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from preparar_base import carregar_base

base = carregar_base()
av = base.dropna(subset=["avaliacao"])
chuva = av.loc[av["choveu"], "avaliacao"]
sem = av.loc[~av["choveu"], "avaliacao"]

# 2. Médias e testes de hipótese
av.groupby("choveu")["avaliacao"].agg(["mean", "count"]).round(2)
stats.ttest_ind(chuva, sem, equal_var=False)
stats.mannwhitneyu(chuva, sem)

# 3. Intervalos de confiança por bootstrap
def diferenca(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)

ic_chuva = stats.bootstrap((chuva,), np.mean, rng=np.random.default_rng(42)).confidence_interval
ic_sem = stats.bootstrap((sem,), np.mean, rng=np.random.default_rng(42)).confidence_interval
ic_dif = stats.bootstrap((chuva, sem), diferenca, rng=np.random.default_rng(42)).confidence_interval
ic_chuva, ic_sem, ic_dif

# 4. Tamanho do efeito e distribuição das notas
dp = np.sqrt(((len(chuva) - 1) * chuva.var() + (len(sem) - 1) * sem.var())
             / (len(chuva) + len(sem) - 2))
(chuva.mean() - sem.mean()) / dp
pd.crosstab(av["choveu"], av["avaliacao"], normalize="index").round(3)

# 5. Gráfico: média com IC 95% e eixo desde o zero
medias = [sem.mean(), chuva.mean()]
erros = [[sem.mean() - ic_sem.low, chuva.mean() - ic_chuva.low],
         [ic_sem.high - sem.mean(), ic_chuva.high - chuva.mean()]]
plt.bar(["sem chuva", "com chuva"], medias, yerr=erros, capsize=6)
plt.ylim(0, 5)
plt.ylabel("nota média")
plt.show()

# 6. Avulso x assinante, na base toda e entre as viagens de até 25 min
for nome, df in [("todas", av), ("até 25 min", av[av["duracao_min"] <= 25])]:
    a = df.loc[df["tipo_usuario"] == "avulso", "avaliacao"]
    b = df.loc[df["tipo_usuario"] == "assinante", "avaliacao"]
    print(nome, round(a.mean() - b.mean(), 3), stats.ttest_ind(a, b, equal_var=False).pvalue)
stats.bootstrap((av.loc[av["tipo_usuario"] == "avulso", "avaliacao"],
                 av.loc[av["tipo_usuario"] == "assinante", "avaliacao"]),
                diferenca, rng=np.random.default_rng(42)).confidence_interval
```

>>> Resultados esperados: com chuva 4,32 (487 viagens) e sem chuva 4,68 (2150);
>>> Welch p = 1,0e-24 e Mann-Whitney p = 1,9e-32;
>>> IC 95%: com chuva 4,25 a 4,38; sem chuva 4,66 a 4,70; diferença −0,43 a −0,30; d de Cohen −0,64;
>>> notas 5: 44,1% com chuva e 71,1% sem chuva;
>>> avulso − assinante: −0,055 (p = 0,030), IC da diferença −0,105 a −0,006; até 25 min: −0,024 (p = 0,32).
>>> Conclusão: a chuva derruba a nota de forma clara e relevante; a diferença dos avulsos é pequena e vem da duração.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para testar o efeito da chuva na avaliação e interpretar o resultado**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um analista de dados especialista em Python, pandas e estatística.

# Tarefa
Verifique, num notebook, se a avaliação das viagens é menor nos dias
de chuva e se essa diferença é relevante para o negócio.

# Contexto
1. Em "etapa6.ipynb", carregue a base com carregar_base() do
   @preparar_base.py e use só as viagens avaliadas.
2. Compare a nota média dos dias com e sem chuva com o teste de
   hipótese que você recomendar, usando SciPy, e explique a escolha.
3. Calcule, com scipy.stats.bootstrap, o IC 95% da nota média de cada
   grupo e o da diferença (com chuva menos sem chuva).
4. Calcule o d de Cohen e a proporção de cada nota nos dois grupos.
5. Faça um gráfico que compare a avaliação dos dois grupos.
6. Repita o teste e o IC da diferença para avulsos e assinantes.
7. Escreva em markdown a interpretação dos resultados, frase por frase.

# Saída e Verificação
- Gere etapa6.ipynb.
- Execute o notebook do início ao fim, sem erros.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: confira o teste escolhido (grupos independentes, sem ttest_rel) e se os ausentes saíram antes dos testes e do bootstrap.

# 2 - confira o gráfico gerado: o eixo começa no zero? A média esconde a distribuição das notas?

# 3 - revise a interpretação frase por frase, com os números do notebook: p-valor, IC da diferença e d de Cohen.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** No Gapminder de 2007, teste a diferença de expectativa de vida: Américas × Ásia.

🛠️ &nbsp;**Exercício \#2:** Calcule com `scipy.stats.bootstrap` o IC 95% de cada continente e o da diferença.

🛠️ &nbsp;**Exercício \#3:** Peça ao LLM a interpretação desses resultados e confira cada frase com os números.

🛠️ &nbsp;**Exercício \#4:** Na sua base, compare uma métrica entre dois grupos e revise o gráfico que o LLM gerar.

- [ ] escolher o teste e tirar os ausentes antes de testar
- [ ] registrar o p-valor e explicar o que ele não informa
- [ ] calcular com `bootstrap` o IC de cada grupo e decidir pelo da diferença
- [ ] separar significância estatística de relevância prática
- [ ] conferir cada frase do LLM com os números

<br/>

<!--
# Exercício #1 — Testes no Gapminder
Américas 73,6 anos (25 países) e Ásia 70,7 (33): Welch p = 0,086; Mann-Whitney p = 0,215.
p > 0,05 não prova que as médias são iguais.

# Exercício #2 — Intervalos por bootstrap
IC 95% (BCa, semente 42): Américas 71,7 a 75,1; Ásia 67,6 a 73,0; diferença −0,2 a 6,3 anos.
O intervalo da diferença contém o zero: o resultado é inconclusivo, e a diferença pode ir de quase zero a 6 anos.
Contraste: Europa × Américas, diferença de 2,2 a 6,2 anos (p = 0,0004).
Com a Oceania (2 países), o bootstrap só gera três médias possíveis: ótimo para discutir o tamanho do grupo.

# Exercício #3 — Interpretação do LLM
Erro típico: "não há diferença entre Américas e Ásia". O certo: os dados não permitem afirmar a diferença.

# Exercício #4 — Base própria e gráfico
Pergunta com dois subgrupos, teste, IC da diferença e um gráfico com o eixo desde o zero, com IC ou com a distribuição.

## os exercícios preparam o TP3 (Exercícios 5 a 8)
-->
