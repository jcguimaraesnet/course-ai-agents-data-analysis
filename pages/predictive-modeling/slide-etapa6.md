---
layout: section
routeAlias: etapa6
---

## **Etapa 6:** Desenvolvimento de Agentes Assíncronos

---
layout: section
---

## O primeiro **agente**
**`Agent` define, `Runner` executa**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Agents
source: https://openai.github.io/openai-agents-python/agents/
---

# `Agent`: quem é o agente

#### **Um nome, as instruções e, se quiser, o modelo**

::left::

```python [assistente.py]
from agents import Agent

INSTRUCOES = (
    "Você ajuda o time comercial de uma empresa de "
    "bicicletas compartilhadas a decidir para quais "
    "usuários avulsos ligar, oferecendo a assinatura. "
    "Use só o perfil e a probabilidade de assinatura "
    "que vierem na pergunta. Recomende ligar a partir "
    "de 0,3. Prioridade: alta a partir de 0,6, média "
    "de 0,3 a 0,6 e baixa abaixo de 0,3. Se a pergunta "
    "não trouxer a probabilidade, não invente: diga "
    "que falta o dado.")

assistente = Agent(name="Assistente comercial",
                   instructions=INSTRUCOES)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`name`** — identifica o agente nos registros e no rastreamento.
- **`instructions`** — o prompt de sistema: o papel, as regras de negócio e o que fazer quando falta um dado.
- **`model`** — opcional: sem ele, vale o `OPENAI_DEFAULT_MODEL` ou o padrão do SDK, o `gpt-5.6-luna`.

</div>

<!--
- as instruções vão para o modelo em toda chamada: as regras fixas (o threshold 0,3 da etapa 3, as faixas de prioridade) ficam nelas; os dados de cada usuário vão na pergunta.
- "não invente" importa: o agente ainda não acessa a base nem o pipeline. Sem a probabilidade na pergunta, ele deve dizer que falta o dado.
- uma boa estrutura de instruções: o papel, a tarefa, as regras e o formato da resposta. É a mesma do prompt.md dos live codings.
- o capítulo 3 do Building Agents with OpenAI Agents SDK constrói o primeiro agente com Agent e Runner.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Running agents
source: https://openai.github.io/openai-agents-python/running_agents/
---

# `Runner`: executando o agente

#### **O `Runner` conduz o ciclo e devolve um resultado**

::left::

```python [assistente.py]
from agents import Runner

resultado = Runner.run_sync(
    assistente, montar_pergunta("U00042"))
print(resultado.final_output)
# Sim, vale ligar: a probabilidade de 0,464
# está acima de 0,3. Prioridade média.
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`Runner.run_sync`** — executa o agente e espera a resposta final.
- **`final_output`** — a resposta: aqui, texto livre.
- **Só em script `.py`** — num notebook o loop de eventos já está rodando, e o `run_sync` dá `RuntimeError`.

</div>

<!--
- o texto da resposta muda a cada execução; o que não muda é a regra: 0,464 fica entre 0,3 e 0,6, prioridade média.
- o resultado traz mais que o final_output: last_agent (o agente que respondeu), new_items (o que foi gerado), raw_responses (uma resposta por chamada ao modelo: aqui, 1) e to_input_list (a conversa, na etapa 9).
- o run_sync é um atalho: por dentro, ele cria o loop de eventos, chama o Runner.run e espera. Por isso não funciona onde já existe um loop rodando, como o Jupyter.
-->

---
layout: two-cols-header
layoutClass: gap-8
---

# A pergunta leva os dados

#### **O script busca o perfil e calcula a probabilidade; o agente só lê o texto**

::left::

```python [assistente.py]
USUARIOS = (pd.read_csv("usuarios_avulsos.csv")
            .drop(columns="virou_assinante")
            .set_index("usuario_id"))
PIPE = joblib.load("pipeline_assinatura.joblib")

def montar_pergunta(usuario_id):
    perfil = USUARIOS.loc[[usuario_id]]
    p = PIPE.predict_proba(perfil)[0, 1]
    return (f"Usuário {usuario_id}. Perfil: "
            f"{perfil.iloc[0].to_json()}. "
            f"Probabilidade de virar assinante: "
            f"{p:.3f}. Vale ligar?")
```

::right::

```text
Usuário U00042. Perfil: {"regiao":"zona_oeste",
"canal":"convenio_empresa","pagamento":"cartao",
"idade":30,"viagens_30d":7,"distancia_media_km":3.0,
"avaliacao_media":3.4}. Probabilidade de virar
assinante: 0.464. Vale ligar?
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **`loc[[...]]`** — com colchetes duplos, uma linha que continua `DataFrame`, como o pipeline espera.
- **Na etapa 7** — o agente ganha ferramentas e busca os dados sozinho.

</div>

<!--
- o pipeline é o da etapa 2 (C = 0,1), carregado uma vez; o joblib.load executa código, então só arquivos gerados pelo próprio time.
- virou_assinante sai da base: é o alvo histórico, e não deve chegar ao modelo.
- outros usuários: U00010 → 0,817 (prioridade alta) e U00043 → 0,206 (não ligar).
- o perfil vai em JSON (to_json), e não como dicionário do pandas, que mostraria tipos do numpy no texto.
-->

---
layout: section
---

## Saída **estruturada**
**Um objeto Pydantic no lugar do texto livre**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Output types
source: https://openai.github.io/openai-agents-python/agents/#output-types
---

# `output_type`: a resposta vira objeto

#### **O SDK envia o esquema ao modelo e valida a resposta**

::left::

```python [agente.py]
from typing import Literal
from pydantic import BaseModel, Field

class Recomendacao(BaseModel):
    usuario_id: str
    probabilidade: float = Field(ge=0, le=1)
    ligar: bool
    prioridade: Literal["baixa", "media", "alta"]
    motivo: str

agente = Agent(
    name="Assistente comercial",
    instructions=INSTRUCOES,
    output_type=Recomendacao,
)
```

::right::

```python [agente.py]
r = resultado.final_output
type(r).__name__        # 'Recomendacao'
r.prioridade, r.ligar   # ('media', True)
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **O esquema vai junto** — `Literal` vira `enum`; `Field`, `minimum` e `maximum`.
- **A resposta é validada** — o `final_output` é um `Recomendacao`, com os campos por atributo.
- **Fora do esquema** — o SDK levanta `ModelBehaviorError`.

</div>

<!--
- no modo estrito (o padrão), todos os campos são obrigatórios e o modelo não pode acrescentar outros: o painel do time comercial lê r.prioridade sem interpretar texto.
- Field(description="...") também vai para o esquema e orienta o modelo sobre o campo.
- a mensagem do erro, quando a resposta não passa no Pydantic: "Invalid JSON when parsing model output". É raro com o modo estrito, mas acontece.
- verificado no SDK: o esquema enviado tem "enum": ["baixa", "media", "alta"] e "minimum": 0, "maximum": 1 na probabilidade.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: "Pydantic: JSON parsing"
source: https://docs.pydantic.dev/latest/concepts/json/
---

# Demo: a resposta passa pelo Pydantic

#### **O que o SDK faz com o texto que o modelo devolve**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
from typing import Literal
from pydantic import BaseModel, ValidationError

class Recomendacao(BaseModel):
    prioridade: Literal["baixa", "media", "alta"]

respostas = [  # o texto que o modelo devolveu
    '{"prioridade": "alta"}',
    '{"prioridade": "urgente"}',
    'Prioridade alta.']
for txt in respostas:
    try:
        r = Recomendacao.model_validate_json(txt)
        print("ok:", r)
    except ValidationError as e:
        print("erro:", e.errors()[0]["type"])
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Três respostas** — um JSON válido, uma prioridade fora da lista e texto livre.
- **`model_validate_json`** — lê o JSON e confere cada campo de uma vez.
- **Antes de executar** — qual erro aparece em cada caso?

</div>

<!--
- saída esperada:
  ok: prioridade='alta'
  erro: literal_error
  erro: json_invalid
- é o que o SDK faz com a resposta do modelo quando há output_type: o texto vira um objeto, ou a execução para com ModelBehaviorError.
- sem output_type, o código teria de interpretar "Prioridade alta." no texto, e qualquer variação da frase quebraria o painel.
-->

---
layout: section
---

## Execução **assíncrona**
**Enquanto uma chamada espera a rede, outra avança**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: asyncio
source: https://docs.python.org/3/library/asyncio-task.html
---

# Síncrono e assíncrono

#### **`run_sync` espera cada resposta; `Runner.run` libera o programa**

::left::

```python [síncrono]
usuarios = ["U00010", "U00042", "U00043"]
for usuario_id in usuarios:
    r = Runner.run_sync(
        agente, montar_pergunta(usuario_id))
    print(r.final_output.prioridade)
```

::right::

```python [assíncrono]
async def recomendar(usuario_id):
    r = await Runner.run(
        agente, montar_pergunta(usuario_id))
    return r.final_output

async def main():
    recs = await asyncio.gather(
        *(recomendar(u) for u in usuarios))

asyncio.run(main())
```

<!--
- uma chamada ao modelo passa quase todo o tempo esperando a rede. No síncrono, o programa fica parado nessa espera; no assíncrono, o await diz "posso esperar aqui": o loop de eventos atende outra tarefa enquanto isso.
- async def cria uma corrotina: chamar recomendar(u) não executa nada até alguém fazer await (ou entregar ao gather).
- asyncio.run(main()) cria o loop, roda o main até o fim e fecha o loop: uma vez só, no ponto de entrada do script.
- o assíncrono não deixa cada chamada mais rápida: ele permite que várias esperem ao mesmo tempo.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: asyncio.gather
source: https://docs.python.org/3/library/asyncio-task.html#asyncio.gather
---

# Demo: três chamadas, um terço do tempo

#### **As esperas se sobrepõem quando as chamadas são concorrentes**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import asyncio
from time import perf_counter as agora

async def consultar(usuario):  # simula a rede
    await asyncio.sleep(1)
    return f"{usuario}: ok"

usuarios = ["U00010", "U00042", "U00043"]
t = agora()
for u in usuarios:
    await consultar(u)
print(f"em sequência: {agora() - t:.1f} s")
t = agora()
await asyncio.gather(*map(consultar, usuarios))
print(f"concorrentes: {agora() - t:.1f} s")
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`consultar`** — o `asyncio.sleep(1)` faz o papel da espera pela resposta do modelo.
- **`gather`** — dispara as três e espera todas: as esperas acontecem juntas.
- **Antes de executar** — quanto tempo leva cada modo?

</div>

<!--
- saída esperada: em sequência: 3.0 s e concorrentes: 1.0 s.
- no navegador (e no Jupyter), o loop de eventos já está rodando: por isso o await aparece solto, fora de uma função. Num script .py, o mesmo código fica dentro de um async def main(), com asyncio.run(main()).
- pelo mesmo motivo, o asyncio.run dá RuntimeError aqui: é o mesmo erro do run_sync num notebook.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Running agents
source: https://openai.github.io/openai-agents-python/running_agents/
---

# Várias recomendações ao mesmo tempo

#### **O tempo total fica perto do da chamada mais lenta**

::left::

```python [agente.py]
async def main():
    inicio = time.perf_counter()
    for usuario_id in usuarios:
        await recomendar(usuario_id)
    print(f"em sequência: "
          f"{time.perf_counter() - inicio:.1f} s")

    inicio = time.perf_counter()
    recs = await asyncio.gather(
        *(recomendar(u) for u in usuarios))
    print(f"concorrentes: "
          f"{time.perf_counter() - inicio:.1f} s")
    for r in recs:
        print(r.usuario_id, r.probabilidade,
              r.ligar, r.prioridade)
```

::right::

```text
em sequência: 3.0 s
concorrentes: 1.0 s
U00010 0.817 True alta
U00042 0.464 True media
U00043 0.206 False baixa
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **A ordem** — o `gather` devolve as respostas na ordem dos pedidos.
- **Limite de taxa** — muitas chamadas juntas podem levar o erro 429 da API.

</div>

<!--
- os tempos acima são de uma conferência com 1 s de espera simulada por chamada. Com o modelo de verdade, cada chamada leva alguns segundos, e o ganho é parecido: o total fica perto do da chamada mais lenta.
- as probabilidades vêm do pipeline, pela pergunta; a prioridade, das regras das instruções.
- com dezenas de chamadas, use um asyncio.Semaphore para limitar quantas rodam ao mesmo tempo e não estourar o limite de taxa da conta.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Running agents
source: https://openai.github.io/openai-agents-python/running_agents/
---

# Três erros comuns

#### **Cada um deixa uma mensagem que ajuda a achar a causa**

::left::

```python
# 1. run_sync com o loop já rodando (notebook)
Runner.run_sync(agente, pergunta)
# RuntimeError: AgentRunner.run_sync() cannot
# be called when an event loop is already running.

# 2. Runner.run sem o await
r = Runner.run(agente, pergunta)
r.final_output
# AttributeError: 'coroutine' object has no
# attribute 'final_output'

# 3. a chave não foi carregada
# openai.OpenAIError: Missing credentials. ...
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **No notebook** — use `await Runner.run(...)` direto na célula.
- **Sem o `await`** — o `Runner.run` só devolve uma corrotina, que nunca roda.
- **Sem a chave** — chame o `load_dotenv()` antes da primeira execução.

</div>

<!--
- os três erros foram reproduzidos no SDK: as mensagens são as que o aluno vai ver.
- no caso 2, o Python ainda avisa "RuntimeWarning: coroutine 'Runner.run' was never awaited".
- no caso 3, confira o verificar_ambiente.py da etapa 5: o .env está na pasta de onde o script roda?
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** `usuarios_avulsos.csv` e o `pipeline_assinatura.joblib` da etapa 2

🧭 &nbsp;**Análise:** o primeiro agente do time comercial, com `Agent` e `Runner`, a recomendação estruturada em Pydantic e várias recomendações ao mesmo tempo com `asyncio`

<!--
Projeto: o mesmo da etapa 5, com o .env carregado. Os dois arquivos ficam na pasta do usuarios_avulsos.csv e do pipeline_assinatura.joblib.

=================================================================
ARQUIVO 1 — assistente.py (o primeiro agente, com resposta em texto: uv run python assistente.py)

```python
"""O primeiro agente: o assistente comercial responde com o perfil e a probabilidade na pergunta."""
import joblib
import pandas as pd
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

# o script, e não o agente, busca o perfil e calcula a probabilidade: as ferramentas vêm na etapa 7
USUARIOS = (pd.read_csv("usuarios_avulsos.csv")
            .drop(columns="virou_assinante")
            .set_index("usuario_id"))
PIPE = joblib.load("pipeline_assinatura.joblib")  # o arquivo da etapa 2, gerado pelo próprio time

INSTRUCOES = (
    "Você ajuda o time comercial de uma empresa de bicicletas compartilhadas a decidir para quais "
    "usuários avulsos ligar, oferecendo a assinatura. Use só o perfil e a probabilidade de "
    "assinatura que vierem na pergunta. Recomende ligar a partir de 0,3. Prioridade: alta a partir "
    "de 0,6, média de 0,3 a 0,6 e baixa abaixo de 0,3. Se a pergunta não trouxer a probabilidade, "
    "não invente: diga que falta o dado."
)

assistente = Agent(name="Assistente comercial", instructions=INSTRUCOES)


def montar_pergunta(usuario_id):
    perfil = USUARIOS.loc[[usuario_id]]
    p = PIPE.predict_proba(perfil)[0, 1]
    return (f"Usuário {usuario_id}. Perfil: {perfil.iloc[0].to_json()}. "
            f"Probabilidade de virar assinante: {p:.3f}. Vale ligar?")


if __name__ == "__main__":
    resultado = Runner.run_sync(assistente, montar_pergunta("U00042"))
    print(resultado.final_output)
```

=================================================================
ARQUIVO 2 — agente.py (saída estruturada e execução assíncrona: uv run python agente.py)

```python
"""O assistente comercial com saída estruturada e execução assíncrona."""
import asyncio
import time
from typing import Literal

from agents import Agent, Runner
from pydantic import BaseModel, Field

from assistente import INSTRUCOES, montar_pergunta


class Recomendacao(BaseModel):
    usuario_id: str
    probabilidade: float = Field(ge=0, le=1)
    ligar: bool
    prioridade: Literal["baixa", "media", "alta"]
    motivo: str


agente = Agent(
    name="Assistente comercial",
    instructions=INSTRUCOES,
    output_type=Recomendacao,
)


async def recomendar(usuario_id):
    resultado = await Runner.run(agente, montar_pergunta(usuario_id))
    return resultado.final_output


async def main():
    usuarios = ["U00010", "U00042", "U00043"]

    inicio = time.perf_counter()
    for usuario_id in usuarios:
        await recomendar(usuario_id)
    print(f"em sequência: {time.perf_counter() - inicio:.1f} s")

    inicio = time.perf_counter()
    recomendacoes = await asyncio.gather(*(recomendar(u) for u in usuarios))
    print(f"concorrentes: {time.perf_counter() - inicio:.1f} s")

    for r in recomendacoes:
        print(r.usuario_id, r.probabilidade, r.ligar, r.prioridade)


if __name__ == "__main__":
    asyncio.run(main())
```

>>> Resultados esperados: a pergunta do U00042 traz o perfil em JSON e "Probabilidade de virar assinante: 0.464". U00010 → 0,817 e U00043 → 0,206.
>>> assistente.py: uma resposta em texto recomendando ligar, com prioridade média (o texto muda a cada execução).
>>> agente.py: U00010 0.817 True alta; U00042 0.464 True media; U00043 0.206 False baixa. Os tempos dependem do modelo e da rede: o concorrente fica perto do tempo da chamada mais lenta, e o em sequência, perto da soma (com 1 s simulado por chamada: 3,0 s e 1,0 s).
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para construir o primeiro agente do time comercial**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um engenheiro de IA especialista no OpenAI Agents SDK.

# Tarefa
Construa o assistente comercial da empresa de bicicletas: um agente que
recomenda se vale ligar para um usuário avulso, oferecendo a assinatura.

# Contexto
1. Em "assistente.py", leia @usuarios_avulsos.csv sem a coluna
   virou_assinante, calcule a probabilidade com @pipeline_assinatura.joblib
   e monte uma pergunta com o perfil e a probabilidade do usuário.
2. Crie um Agent com as regras do time comercial nas instruções (ligar a
   partir de 0,3; prioridade alta a partir de 0,6, média de 0,3 a 0,6 e
   baixa abaixo de 0,3; sem a probabilidade, não inventar) e execute-o com
   Runner.run_sync.
3. Em "agente.py", estruture a saída num modelo Pydantic Recomendacao
   (usuario_id, probabilidade de 0 a 1, ligar, prioridade em Literal e
   motivo), com output_type.
4. Recomende U00010, U00042 e U00043 com Runner.run, em sequência e com
   asyncio.gather, medindo os dois tempos.

# Saída e Verificação
- Imprima os campos de cada Recomendacao e confira a probabilidade com a
  do pipeline.
- Mostre os tempos em sequência e concorrente.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: se o agente de código usar Runner.run_sync dentro de um async def (ou num notebook), vem o RuntimeError: dentro do loop, é await Runner.run.

# 2 - confira se a probabilidade de cada Recomendacao é a do pipeline: o modelo copia o número da pergunta. Se ele "arredondar" ou estimar outro, reforce as instruções.

# 3 - código de tutoriais antigos chama a API de chat direto e faz json.loads na resposta: com o SDK, o output_type gera o esquema e valida a resposta.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** Crie o guia do museu com `Agent` e responda duas perguntas com `run_sync`.

🛠️ &nbsp;**Exercício \#2:** Leve à pergunta o perfil e a probabilidade do pipeline do Titanic de um passageiro.

🛠️ &nbsp;**Exercício \#3:** Estruture a resposta com `output_type`, `Literal` e `Field` e imprima os campos.

🛠️ &nbsp;**Exercício \#4:** Responda três passageiros com `asyncio.gather` e compare com a sequência.

- [ ] chamar o `load_dotenv()` antes da primeira execução
- [ ] usar o `run_sync` só em script `.py`
- [ ] pôr as regras nas instruções, e os dados na pergunta
- [ ] acessar os campos do `final_output` por atributo
- [ ] medir os tempos com `time.perf_counter()`

<br/>

<!--
Cenário: o guia do museu do Titanic, com o titanic do seaborn e o pipeline salvo no Exercício 4 da etapa 2 (pipeline_titanic.joblib: age, fare, sibsp, parch, sex, pclass e embarked; C = 10).

# Exercício #1 — Agent e Runner
Agent(name="Guia do museu", instructions=papel de guia do museu do Titanic, com respostas curtas e fiéis aos fatos) e Runner.run_sync para duas perguntas, como "quantos passageiros havia a bordo?" e "por que mais mulheres sobreviveram?". As respostas são texto e mudam a cada execução.

# Exercício #2 — Os dados na pergunta
O script calcula a probabilidade com o pipeline e a coloca na pergunta, com o perfil em JSON. Passageiro 0 (homem, 22 anos, 3ª classe) → 0,083; passageiro 1 (mulher, 38 anos, 1ª classe, Cherbourg) → 0,919; passageiro 2 (mulher, 26 anos, 3ª classe) → 0,592.

# Exercício #3 — Saída estruturada
Um modelo como Veredito(passageiro: int, probabilidade: float = Field(ge=0, le=1), chance: Literal["baixa", "media", "alta"], explicacao: str), com as faixas nas instruções (por exemplo, baixa abaixo de 0,3, média até 0,6 e alta a partir de 0,6): 0,083 baixa, 0,592 média e 0,919 alta. Os campos são lidos por atributo (v.chance).

# Exercício #4 — Concorrência
asyncio.gather com os três passageiros, dentro de um async def main() com asyncio.run(main()). O tempo concorrente fica perto do da chamada mais lenta; o em sequência, perto da soma. Conferência de cada objeto: isinstance(v, Veredito), v.chance entre as três categorias e 0 <= v.probabilidade <= 1.

## os exercícios preparam os Exercícios 4 a 8 do TP3
-->
