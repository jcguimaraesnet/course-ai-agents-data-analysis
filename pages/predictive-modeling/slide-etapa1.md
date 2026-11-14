---
layout: section
routeAlias: etapa1
---

## **Etapa 1:** Preparação de Dados para Classificação

---
layout: section
---

## Aprendizado de **máquina**
**O que é, tipos de aprendizado e modos de treinamento**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Hands-On ML, cap. 1
source: https://github.com/ageron/handson-mlp/blob/main/01_the_machine_learning_landscape.ipynb
---

# Regras ou dados?

#### **Em vez de escrever as regras, o modelo aprende o padrão com exemplos**

::left::

```python [regras.py]
def vai_assinar(usuario):
    if usuario["viagens_30d"] > 8:
        return 1
    if usuario["canal"] == "convenio_empresa":
        return 1
    return 0
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Regras à mão** — funcionam enquanto o padrão é simples, conhecido e estável.
- **Aprendizado de máquina** — o modelo extrai o padrão de exemplos com a resposta conhecida.
- **Quando vale a pena** — o padrão é complexo, muda com o tempo ou ninguém sabe descrevê-lo.

</div>

<!--
- definição de Tom Mitchell (Hands-On ML, cap. 1): um programa aprende com a experiência E numa tarefa T, medida por P, se o desempenho em T, medido por P, melhora com E.
- na base das aulas, essa regra acerta 73,1%: quase o mesmo que dizer sempre "não vira" (71,5%). É o gancho para a referência do slide "Treino, teste e uma referência".
- a regra é ilustrativa: ninguém escreveria os limites certos à mão para sete colunas ao mesmo tempo.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Supervised learning
source: https://scikit-learn.org/stable/supervised_learning.html
---

# Da regressão à classificação

#### **O mesmo fit e predict da DR1; muda o tipo do alvo**

::left::

```python [etapa1.ipynb]
import pandas as pd

df = pd.read_csv("usuarios_avulsos.csv")
df.shape                         # (3000, 9)
df["virou_assinante"].mean()     # 0.285

X = df[["idade", "viagens_30d",
        "distancia_media_km"]]
y = df["virou_assinante"]        # 0 ou 1
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Regressão (DR1)** — o alvo é um número: a duração da viagem em minutos.
- **Classificação** — o alvo é uma classe: o usuário avulso virou assinante (1) ou não (0).
- **Vocabulário** — cada linha é uma instância, as colunas de `X` são as features e `y` é o alvo, ou rótulo.

</div>

<!--
- a base das aulas: 3.000 usuários avulsos da empresa de bicicletas da DR1, com o primeiro mês de uso; 28,5% viraram assinantes em 30 dias.
- nesta etapa, só as três colunas numéricas sem valores ausentes: as categóricas e a avaliação_media (8% ausentes) entram na etapa 2, com o ColumnTransformer.
- o score de um classificador é a acurácia: a proporção de acertos.
-->

---
layout: default
sourceLabel: Hands-On ML, cap. 1
source: https://github.com/ageron/handson-mlp/blob/main/01_the_machine_learning_landscape.ipynb
---

# Tipos de aprendizado

#### **O que o modelo tem para aprender define o tipo**

<div class="h-4" />

| Tipo | O modelo aprende com | Exemplo na empresa de bicicletas |
|------|----------------------|----------------------------------|
| **Supervisionado** | exemplos com a resposta (rótulo) | prever quem vira assinante; prever a duração da viagem |
| **Não supervisionado** | dados sem rótulo | agrupar estações por padrão de uso; achar viagens anômalas |
| **Semissupervisionado** | poucos rótulos e muitos dados sem rótulo | classificar comentários quando só 200 foram rotulados à mão |
| **Por reforço** | recompensas pelas próprias ações | um agente que ajusta o preço por região e aprende com a receita |

<!--
- classificação e regressão são as duas tarefas do supervisionado: a diferença está no tipo do alvo.
- autossupervisionado: os rótulos saem dos próprios dados (esconder uma palavra e prevê-la); é assim que os LLMs são pré-treinados. Gancho para a parte de agentes da disciplina.
- por reforço: um agente percebe o ambiente, age e recebe recompensa; a segunda metade da disciplina volta a essa ideia de agente.
- pergunta para a turma: em qual linha entra o modelo de regressão da duração da DR1? (supervisionado, regressão)
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: SGDClassifier.partial_fit
source: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html
---

# Batch ou online

#### **O modo de treinamento diz como o modelo incorpora dados novos**

::left::

<div class="text-left w-full [&_li]:mb-3">

- **Batch** — treina com todos os dados de uma vez; para incorporar dados novos, retreina do zero (toda semana, por exemplo).
- **Online** — aprende aos poucos, a cada dado ou lote novo, e se adapta rápido quando o padrão muda.
- **Taxa de aprendizado** — no online, quanto cada dado novo pesa: alta adapta rápido e esquece rápido.

</div>

::right::

```python [online.py]
from sklearn.linear_model import SGDClassifier

modelo = SGDClassifier(random_state=42)
for lote_X, lote_y in lotes_que_chegam:
    modelo.partial_fit(lote_X, lote_y,
                       classes=[0, 1])
```

> [!CAUTION]
> Responder em tempo real não exige treinar online: um modelo treinado em batch também responde na hora.

<!--
- batch = offline learning no livro: o sistema não aprende em produção, só aplica o que aprendeu.
- online também serve para bases que não cabem na memória (out-of-core): o modelo aprende lote a lote.
- partial_fit é o método dos estimadores que aprendem aos poucos; no primeiro lote, é preciso informar todas as classes.
- o erro mais comum na classificação de problemas: chamar de online qualquer sistema que responde na hora.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Incremental learning
source: https://scikit-learn.org/stable/computing/scaling_strategies.html
---

# Demo: quando o padrão muda

#### **O modelo batch fica parado; o online acompanha a mudança**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np
from sklearn.linear_model import SGDClassifier
X = np.random.default_rng(0).normal(size=(3000, 2))
y = (X[:, 0] > 0).astype(int)
y[2000:] = 1 - y[2000:]   # o padrão inverte
b = SGDClassifier(random_state=0)
b.fit(X[:1000], y[:1000])
o = SGDClassifier(random_state=0)
o.partial_fit(X[:1000], y[:1000], classes=[0, 1])
for ini in [1000, 2000]:
    acc = np.zeros(2)
    for j in range(ini, ini + 1000, 50):
        L = slice(j, j + 50)
        acc += [m.score(X[L], y[L]) for m in (b, o)]
        o.partial_fit(X[L], y[L])   # aprende depois
    print(ini, (acc / 20).round(2))
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Os dados** — 3.000 eventos em sequência; a partir do 2.000, a regra se inverte.
- **Batch** — treinado com os 1.000 primeiros e nunca mais atualizado.
- **Online** — usa cada lote de 50 para prever e, depois, aprende com ele.
- **Antes de executar** — cada linha mostra [batch, online]: o que acontece com cada um depois do evento 2.000?

</div>

<!--
- saída esperada (acurácia média em cada bloco de 1.000 eventos, [batch online]): 1000 [0,99 0,98]; 2000 [0,01 0,92].
- b é o modelo batch e o, o online; L é o lote de 50 eventos.
- o batch não erra por ser ruim: ele aprendeu um padrão que deixou de valer. Retreinar resolveria, mas só no próximo ciclo.
- a mudança de padrão no tempo chama-se concept drift; o online também tem risco: um lote de dados ruins estraga o modelo.
-->

---
layout: default
sourceLabel: Hands-On ML, cap. 1
source: https://github.com/ageron/handson-mlp/blob/main/01_the_machine_learning_landscape.ipynb
---

# Classificando problemas de ML

#### **Tipo de aprendizado e modo de treinamento, com a justificativa**

<div class="h-4" />

| Problema | Tipo | Modo | Por quê |
|----------|------|------|---------|
| Prever, todo mês, quem vira assinante | supervisionado | batch | histórico rotulado; o padrão muda devagar |
| Agrupar estações por padrão de uso | não supervisionado | batch | não há rótulo; análise periódica |
| Detectar bicicleta com defeito pelos sensores | não supervisionado | online | anomalias num fluxo contínuo de leituras |
| Ajustar o preço por região ao longo do dia | por reforço | online | aprende com a receita de cada preço testado |

<!--
- justifique pelo que o problema oferece para aprender (rótulos, dados sem rótulo ou recompensas) e pela rapidez com que o modelo precisa se adaptar.
- a detecção de defeito poderia ser supervisionada se houvesse um histórico de defeitos rotulados: o tipo depende dos dados disponíveis, não só do objetivo.
- recomendação de bicicleta ou de estação também rende boa discussão: com histórico de cliques, é supervisionado.
- é o raciocínio que o Exercício 1 do TP1 pede.
-->

---
layout: section
---

## Generalização: **bias** e **variância**
**Underfitting, overfitting e regularização**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: DummyClassifier
source: https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html
---

# Treino, teste e uma referência

#### **Um modelo útil precisa acertar mais do que um palpite fixo, nos dados que não viu**

::left::

```python [etapa1.ipynb]
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42)

ref = DummyClassifier().fit(X_tr, y_tr)
ref.score(X_te, y_te)    # 0.732
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Treino e teste** — a mesma divisão da DR1: o erro que importa é o dos dados novos.
- **Referência** — o `DummyClassifier` responde sempre a classe mais comum: "não vira".
- **A régua** — com 72% de "não vira", qualquer modelo abaixo disso é pior que não fazer nada.

</div>

<!--
- na DR1, a referência da regressão era prever sempre a média (R² = 0); aqui é prever sempre a classe mais comum.
- sem estratificar, o teste ficou com 26,8% de positivos e o treino com 28,9%: por isso a referência dá 0,711 no treino e 0,732 no teste. A estratificação, na etapa 2, corrige isso.
- a acurácia engana com classes desbalanceadas; as métricas próprias de classificação (matriz de confusão, precisão, recall) são da etapa 3.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: DecisionTreeClassifier
source: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
---

# Underfitting e overfitting

#### **A profundidade da árvore controla quanto o modelo se ajusta ao treino**

::left::

```python [etapa1.ipynb]
from sklearn.tree import DecisionTreeClassifier

for d in [1, 6, None]:
    arv = DecisionTreeClassifier(max_depth=d,
        random_state=42).fit(X_tr, y_tr)
    print(d, arv.score(X_tr, y_tr), arv.score(X_te, y_te))
# 1 0.740 0.748 | 6 0.810 0.782 | None 0.969 0.718
```

<div class="text-left w-full [&_li]:mb-2">

- **Underfitting** — erra no treino e no teste: simples demais.
- **Overfitting** — acerta o treino e erra o teste: decorou o ruído.

</div>

::right::

<AssetImg src="pm-complexidade-arvore.png" class="rounded-lg w-full" />

<!--
- a árvore de decisão entra aqui só como ferramenta: uma sequência de perguntas sim/não sobre as features; quanto mais profunda, mais perguntas e mais detalhe.
- sem limite de profundidade, ela acerta 96,9% do treino e 71,8% do teste: pior que a referência (73,2%).
- o melhor teste fica entre 3 e 6 níveis; escolher pelo teste, porém, é trapaça: a etapa 2 escolhe pela validação cruzada.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Bias-variance
source: https://scikit-learn.org/stable/auto_examples/ensemble/plot_bias_variance.html
---

# O tradeoff bias-variância

#### **O erro em dados novos tem três partes, e duas delas puxam em sentidos opostos**

::left::

$$
\mathbb{E}\big[(y - \hat{f}(x))^2\big] = \text{bias}^2 + \text{variância} + \sigma^2
$$

<div class="text-left w-full [&_li]:mb-3">

- **Bias** — erro de suposições simples demais: erra do mesmo jeito em qualquer amostra.
- **Variância** — sensibilidade à amostra: outro treino daria outro modelo.
- **Ruído (σ²)** — o erro que nenhum modelo elimina.

</div>

::right::

| Sintoma | Diagnóstico | O que fazer |
|---------|-------------|-------------|
| treino e teste perto da referência | bias alto | mais complexidade, menos regularização |
| treino alto, teste bem menor | variância alta | mais regularização, mais dados |
| os dois altos e próximos | equilíbrio | manter |

<!--
- a decomposição é a do erro quadrático (Machine Learning Foundations, cap. 2); em classificação, a intuição é a mesma.
- mais complexidade: o bias cai e a variância sobe. O ponto ótimo está no meio, como no gráfico do slide anterior.
- atenção: treino e teste iguais não querem dizer modelo bom. Se os dois estão na altura da referência, o modelo não aprendeu nada (bias alto).
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: numpy.polyfit
source: https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
---

# Demo: bias e variância na prática

#### **Treine o mesmo modelo em 300 amostras diferentes e veja como as previsões variam**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import numpy as np

rng = np.random.default_rng(1)
padrao = lambda x: np.sin(2 * x)   # o verdadeiro
x0 = 1.0                           # ponto medido
for grau in [1, 3, 9]:
    prev = []
    for _ in range(300):           # 300 amostras
        x = rng.uniform(0, 3, 20)
        y = padrao(x) + rng.normal(0, 0.3, 20)
        coef = np.polyfit(x, y, grau)
        prev.append(np.polyval(coef, x0))
    prev = np.array(prev)
    bias2 = (prev.mean() - padrao(x0)) ** 2
    print(f"grau {grau}: bias² {bias2:.3f} | "
          f"variância {prev.var():.3f}")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **O experimento** — 300 amostras de 20 pontos de uma curva com ruído; em cada uma, um polinômio prevê o valor em x = 1.
- **Bias²** — o quanto a média das previsões erra o valor verdadeiro.
- **Variância** — o quanto as previsões mudam de uma amostra para outra.
- **Antes de executar** — qual grau tem o bias maior? E a variância?

</div>

<!--
- saída esperada: grau 1 bias² 0,296 e variância 0,026; grau 3 bias² 0,004 e variância 0,016; grau 9 bias² 0,002 e variância 0,744.
- a reta (grau 1) erra sempre do mesmo jeito: bias alto. O grau 9 acerta na média, mas cada amostra dá uma curva diferente: variância alta.
- o grau 3 é o equilíbrio: o mesmo papel da árvore de 6 níveis no gráfico do slide de underfitting.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: LogisticRegression
source: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
---

# Regularização: o botão da complexidade

#### **Restringir o modelo para ele não decorar o ruído**

::left::

```python [etapa1.ipynb]
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

for C in [0.001, 1]:
    m = make_pipeline(StandardScaler(),
                      LogisticRegression(C=C))
    m.fit(X_tr, y_tr)
    print(C, m.score(X_tr, y_tr),
          m.score(X_te, y_te))
# 0.001  0.725  0.742
# 1      0.785  0.805
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Hiperparâmetro** — o botão que você escolhe antes do `fit`: `max_depth` na árvore, `C` na regressão logística.
- **Parâmetro** — o que o modelo aprende no `fit`: os coeficientes, as perguntas da árvore.
- **`C`** — o inverso da força da regularização: `C` pequeno regulariza muito.
- **Diagnóstico** — com `C = 0.001`, treino e teste ficam perto da referência: bias alto.

</div>

<!--
- a regressão logística entra aqui como um classificador pronto; como ela transforma as features numa probabilidade é assunto da etapa 3.
- o make_pipeline com StandardScaler é o mesmo da DR1 (etapa 8): a regularização pune coeficientes grandes, e por isso as features precisam estar na mesma escala.
- na árvore, regularizar é limitar max_depth (ou exigir mais exemplos por folha).
- escolher o hiperparâmetro olhando o teste contamina a avaliação: a etapa 2 resolve com validação cruzada e GridSearchCV.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** `usuarios_avulsos.csv`, o primeiro mês dos usuários avulsos da empresa de bicicletas, gerado pelo `gerar_dados.py`

🎯 &nbsp;**Análise:** quem vira assinante? A referência, a árvore com profundidades diferentes e a regressão logística com `C` diferentes, com o diagnóstico de bias e variância

<!--
Projeto: o mesmo projeto uv da DR1 (WSL + uv). Dependências: uv add pandas numpy scikit-learn matplotlib ipykernel

=================================================================
ARQUIVO 1 — gerar_dados.py (rode uma vez: gera usuarios_avulsos.csv; a etapa 2 usa o mesmo arquivo)

```python
"""Gera usuarios_avulsos.csv: o primeiro mês dos usuários avulsos e se viraram assinantes."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 3000

regiao = rng.choice(["centro", "zona_sul", "zona_norte", "zona_oeste"], size=n, p=[0.3, 0.3, 0.2, 0.2])
canal = rng.choice(["loja_de_apps", "indicacao", "convenio_empresa"], size=n, p=[0.6, 0.25, 0.15])
pagamento = rng.choice(["cartao", "pix"], size=n, p=[0.65, 0.35])
idade = np.clip(rng.normal(31, 9, n), 16, 70).round().astype(int)
viagens_30d = rng.poisson(5, n)
distancia_media_km = np.round(np.clip(rng.gamma(2.0, 1.2, n), 0.3, 10), 1)
avaliacao_media = np.round(np.clip(rng.normal(4.2, 0.5, n), 1, 5), 1)

# virar assinante: mais viagens, convênio ou indicação, centro e boa avaliação aumentam a chance
logit = (-5.5 + 0.7 * viagens_30d + 1.5 * (canal == "convenio_empresa") + 0.8 * (canal == "indicacao")
         + 0.6 * (regiao == "centro") - 0.04 * (idade - 31) + 1.2 * (avaliacao_media - 4.2)
         + rng.normal(0, 0.5, n))
virou_assinante = (rng.uniform(0, 1, n) < 1 / (1 + np.exp(-logit))).astype(int)

# quem não avaliou nenhuma viagem fica sem avaliação média
avaliacao_media = np.where(rng.random(n) < 0.08, np.nan, avaliacao_media)

df = pd.DataFrame({
    "usuario_id": [f"U{i:05d}" for i in range(1, n + 1)],
    "regiao": regiao, "canal": canal, "pagamento": pagamento, "idade": idade,
    "viagens_30d": viagens_30d, "distancia_media_km": distancia_media_km,
    "avaliacao_media": avaliacao_media, "virou_assinante": virou_assinante,
})
df.to_csv("usuarios_avulsos.csv", index=False)
```

=================================================================
ARQUIVO 2 — etapa1.ipynb (uma célula de markdown antes de cada célula de código)

```python
# 1. Carga e o problema: alvo, proporção e features numéricas sem ausentes
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("usuarios_avulsos.csv")
df.shape, df["virou_assinante"].mean(), df.isna().sum()
X = df[["idade", "viagens_30d", "distancia_media_km"]]
y = df["virou_assinante"]

# 2. Treino, teste e a referência
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
ref = DummyClassifier().fit(X_tr, y_tr)
ref.score(X_tr, y_tr), ref.score(X_te, y_te)

# 3. Árvore com profundidade de 1 a 20: acurácia de treino e de teste
linhas = []
for d in range(1, 21):
    arv = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_tr, y_tr)
    linhas.append({"max_depth": d, "treino": arv.score(X_tr, y_tr), "teste": arv.score(X_te, y_te)})
curva = pd.DataFrame(linhas).set_index("max_depth")
ax = curva.plot(marker="o")
ax.axhline(ref.score(X_te, y_te), linestyle="--", color="gray")
plt.show()

# 4. Regressão logística com C muito pequeno e com o C padrão
for C in [0.001, 1]:
    m = make_pipeline(StandardScaler(), LogisticRegression(C=C)).fit(X_tr, y_tr)
    print(C, m.score(X_tr, y_tr), m.score(X_te, y_te))

# 5. Diagnóstico (markdown): para cada modelo, bias alto, variância alta ou equilíbrio, e o que fazer
```

>>> Resultados esperados: (3000, 9); 28,5% viraram assinantes; 230 avaliações médias ausentes (fora do X desta etapa).
>>> Treino 2.400 e teste 600 linhas; positivos 28,9% no treino e 26,8% no teste (sem estratificar).
>>> Referência: 0,711 no treino e 0,732 no teste.
>>> Árvore: profundidade 1 → 0,740 e 0,748 (underfitting); 6 → 0,810 e 0,782; sem limite (None) → 0,969 e 0,718; com 20 níveis, 0,967 e 0,725.
>>> Regressão logística: C = 0,001 → 0,725 e 0,742 (bias alto, perto da referência); C = 1 → 0,785 e 0,805.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para diagnosticar bias e variância na previsão de assinaturas**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um engenheiro de machine learning especialista em Python e scikit-learn.

# Tarefa
Num notebook, compare modelos simples e complexos que preveem se um
usuário avulso vira assinante e diagnostique bias e variância.

# Contexto
1. Em "etapa1.ipynb", carregue @usuarios_avulsos.csv; o alvo é
   virou_assinante, e as features são idade, viagens_30d e distancia_media_km.
2. Separe treino e teste (test_size=0.2, random_state=42).
3. Calcule a acurácia de um DummyClassifier no treino e no teste.
4. Treine DecisionTreeClassifier com max_depth de 1 a 20 (random_state=42)
   e plote a acurácia de treino e de teste, com a referência tracejada.
5. Treine LogisticRegression com C=0.001 e C=1, com StandardScaler num
   make_pipeline, e mostre as acurácias de treino e teste.
6. Antes de cada passo, crie uma célula de markdown explicando o passo.

# Saída e Verificação
- Gere etapa1.ipynb e instale as dependências com uv add.
- Execute o notebook do início ao fim, sem erros.
- No fim, escreva o diagnóstico de cada modelo: bias, variância ou equilíbrio.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: confira se o agente avaliou no teste e comparou com a referência; "acurácia de 72%" não diz nada sem ela.

# 2 - se o diagnóstico chamar de "equilibrado" o modelo com treino e teste iguais perto de 0,73, é a deixa para o slide do tradeoff: ele não aprendeu nada (bias alto).

# 3 - se o agente escolher a profundidade pelo maior acerto no teste, segure: escolher hiperparâmetro olhando o teste é assunto da etapa 2.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** Classifique quatro problemas de ML por tipo de aprendizado e modo de treinamento, com a justificativa.

🛠️ &nbsp;**Exercício \#2:** No Titanic, calcule a proporção de sobreviventes e a acurácia da referência no teste.

🛠️ &nbsp;**Exercício \#3:** Treine árvores com `max_depth` de 1 a 10 e sem limite e diagnostique bias e variância.

🛠️ &nbsp;**Exercício \#4:** Compare a regressão logística com `C=0.001` e `C=1` e explique o efeito da regularização.

- [ ] justificar o tipo pelo que o problema oferece para aprender
- [ ] não confundir responder em tempo real com treinar online
- [ ] separar treino e teste com `random_state` fixo
- [ ] comparar cada modelo com a referência do `DummyClassifier`
- [ ] escrever o diagnóstico com os números de treino e teste

<br/>

<!--
# Exercício #1 — Classificar problemas
Sugestões (de um app de delivery): prever o tempo de entrega com o histórico (supervisionado, regressão, batch); agrupar restaurantes por cardápio sem categorias (não supervisionado, batch); detectar pedidos fraudulentos num fluxo contínuo, com o modelo aprendendo com cada fraude confirmada (supervisionado, online); um sistema que escolhe a taxa de entrega por bairro e aprende com o resultado de cada escolha (por reforço, online).

# Exercício #2 — Titanic e a referência
titanic = sns.load_dataset("titanic"): 891 passageiros, 38,4% sobreviveram; age tem 177 ausentes.
Use as colunas sem ausentes: pclass, sibsp, parch e fare. Com test_size=0.2 e random_state=42 (sem estratificar):
DummyClassifier 0,624 no treino e 0,587 no teste.

# Exercício #3 — Árvores
max_depth 1 → 0,666 e 0,676; 4 → 0,742 e 0,732; 5 → 0,747 e 0,732; 10 → 0,801 e 0,732; sem limite → 0,838 e 0,693.
A árvore sem limite tem a maior diferença entre treino e teste (variância alta); a de profundidade 1 erra nos dois (bias alto).

# Exercício #4 — Regularização
make_pipeline(StandardScaler(), LogisticRegression(C=...)): C = 0,001 → 0,626 e 0,587 (igual à referência: bias alto); C = 1 → 0,680 e 0,715.

## os exercícios preparam os Exercícios 1 e 2 do TP1
-->
