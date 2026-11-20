---
layout: section
routeAlias: etapa9
---

## **Etapa 9:** Memória e Persistência em Agentes

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Sessions
source: https://openai.github.io/openai-agents-python/sessions/
---

# Memória de curto e de longo prazo

#### **O modelo não lembra de nada: memória é o que o seu código põe na entrada**

::left::

| | curto prazo | longo prazo |
|---|---|---|
| guarda | a conversa | fatos de cada usuário |
| dono | um vendedor | o time inteiro |
| dura | a conversa | até alguém apagar |
| no SDK | `Session` | ferramentas suas |

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Curto prazo** — o histórico: "e se ele pagasse com pix?" depende de saber quem é "ele".
- **Longo prazo** — o que vale nas próximas conversas: o U00042 prefere WhatsApp.
- **Persistência** — as duas num arquivo, para sobreviver ao fim do programa.

</div>

<!--
- o modelo não guarda estado entre chamadas: cada chamada recebe tudo de novo, como na etapa 7 (o histórico inteiro a cada volta do ciclo).
- o capítulo 5 do Building Agents with OpenAI Agents SDK trata memória e conhecimento; a recuperação de documentos (RAG) fica fora da disciplina.
- a memória de longo prazo não vem pronta no SDK: a estrutura e o critério de recuperação são decisões de projeto.
-->

---
layout: section
---

## Memória de **curto prazo**
**A conversa que continua**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: "Running agents: conversations"
source: https://openai.github.io/openai-agents-python/running_agents/
---

# Sem memória, cada execução é isolada

#### **O segundo `Runner.run` não sabe o que aconteceu no primeiro**

::left::

```python [curto_prazo.py]
r1 = await Runner.run(agente,
    "Vale ligar para o U00042?")
r2 = await Runner.run(agente,
    "E se ele pagasse com pix?")
# o modelo não sabe quem é "ele"

entrada = r1.to_input_list() + [
    {"role": "user",
     "content": "E se ele pagasse com pix?"}]
r3 = await Runner.run(agente, entrada)
# com pix, a probabilidade sobe para 0,492
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Cada run começa do zero** — o modelo só vê o que recebe na entrada.
- **`to_input_list()`** — a entrada do run e tudo o que ele gerou: pergunta, chamadas de ferramenta e resposta.
- **Na mão** — funciona, mas o código guarda e remonta o histórico a cada pergunta.

</div>

<!--
- o agente é o assistente comercial desta etapa (agente_memoria.py, nas notas do Live Coding): as ferramentas da etapa 8 e resposta em texto, sem output_type, porque agora é uma conversa.
- r2 sem histórico: o modelo pergunta de quem se trata, ou chuta um usuário.
- r1.to_input_list() tem 6 itens: a pergunta, duas chamadas de ferramenta, os dois resultados e a resposta.
- U00042 com pix: 0,492, contra 0,464 com cartão.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Sessions
source: https://openai.github.io/openai-agents-python/sessions/
---

# `Session`: o histórico automático

#### **O SDK carrega e grava a conversa a cada `Runner.run`**

::left::

```python [curto_prazo.py]
from agents import SQLiteSession

sessao = SQLiteSession("vendedor-ana")
for pergunta in ["Vale ligar para o U00042?",
                 "E se ele pagasse com pix?"]:
    r = await Runner.run(agente, pergunta,
                         session=sessao)
    print(r.final_output)
len(await sessao.get_items())    # 10
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Antes de cada run** — a sessão põe o histórico na entrada.
- **Depois** — guarda a pergunta, as chamadas de ferramenta e a resposta.
- **`session_id`** — separa as conversas: uma por vendedor.
- **Sem arquivo** — o banco fica na memória e some com o programa.

</div>

<!--
- 10 itens: 6 no primeiro turno (pergunta, duas chamadas, dois resultados, resposta) e 4 no segundo (pergunta, a prever_assinatura com pix, o resultado e a resposta). Cada ferramenta a mais que o modelo decidir chamar soma 2 itens.
- Session é o protocolo do SDK; o SQLiteSession é a implementação mais simples. Há outras, como Redis, SQLAlchemy e a própria OpenAI (OpenAIConversationsSession).
- métodos da sessão: get_items (o histórico), pop_item (desfaz o último item) e clear_session (apaga a conversa).
-->

---
layout: section
---

## Persistência **entre execuções**
**A conversa sobrevive ao fim do programa**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: SQLite sessions
source: https://openai.github.io/openai-agents-python/sessions/#sqlite-sessions
---

# `SQLiteSession` num arquivo

#### **O mesmo `session_id` no mesmo arquivo traz a conversa de volta**

::left::

```python [agente_memoria.py]
async def main():
    vendedor = sys.argv[1]
    sessao = SQLiteSession(
        f"vendedor-{vendedor}", "conversas.db")
    itens = await sessao.get_items()
    print(f"Histórico de {vendedor}:",
          len(itens), "itens")
    while (pergunta := input("Você: ")) != "sair":
        r = await Runner.run(agente, pergunta,
                             session=sessao)
        print("Assistente:", r.final_output)
```

::right::

```bash
$ uv run python agente_memoria.py ana
Histórico de ana: 0 itens
Você: Vale ligar para o U00042?
Assistente: Sim: 0,464, prioridade média.
Você: sair
$ uv run python agente_memoria.py ana
Histórico de ana: 6 itens
Você: E se ele pagasse com pix?
Assistente: Com pix, sobe para 0,492.
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **O segundo argumento** — o arquivo, com as sessões de todos os vendedores.

</div>

<!--
- o texto das respostas muda a cada execução; os números vêm das ferramentas, e a API da etapa 4 precisa estar no ar.
- o conversas.db tem duas tabelas: agent_sessions (uma linha por sessão) e agent_messages (id, session_id, message_data em JSON e created_at). Dá para abrir com o sqlite3 e conferir.
- o arquivo guarda conversas sobre pessoas: fica fora do Git (.gitignore), como o .env.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: sqlite3
source: https://docs.python.org/3/library/sqlite3.html
---

# Demo: o histórico num arquivo

#### **O que a `SQLiteSession` faz por baixo, em miniatura**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
import json, sqlite3

def abrir():  # cada execução abre o arquivo
    con = sqlite3.connect("/tmp/conversas.db")
    con.execute("CREATE TABLE IF NOT EXISTS"
                " mensagens (sessao, conteudo)")
    return con
msg = json.dumps({"role": "user", "content":
                  "U00042: vale ligar?"})
with abrir() as con:  # grava e confirma (commit)
    con.execute("INSERT INTO mensagens VALUES"
                " (?, ?)", ("vendedor-ana", msg))
con.close()  # o programa termina; o arquivo fica
for sessao, conteudo in abrir().execute(
        "SELECT * FROM mensagens"):
    print(sessao, json.loads(conteudo)["content"])
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **`abrir`** — conecta ao arquivo e cria a tabela na primeira vez.
- **Uma mensagem por linha** — o JSON da mensagem, com a sessão como chave.
- **Execute duas vezes** — o que a segunda execução encontra?

</div>

<!--
- saída esperada na primeira execução: vendedor-ana U00042: vale ligar?. Na segunda, duas linhas iguais: o arquivo guardou a primeira.
- é a ideia da tabela agent_messages: o session_id e o item da conversa em JSON (message_data).
- no navegador, o arquivo dura até a página recarregar; no computador, até alguém apagá-lo.
- o with do sqlite3 confirma a transação (commit), mas não fecha a conexão: por isso o close().
-->

---
layout: section
---

## Memória de **longo prazo**
**O que o time sabe sobre cada usuário**

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Building Agents, cap. 5
source: https://github.com/PacktPublishing/Building-Agents-with-OpenAI-Agents-SDK
---

# Uma memória estruturada

#### **Uma tabela por fato: quem, quando, sobre o quê e o quê**

::left::

```python [memoria.py]
Topico = Literal["contato", "oferta", "perfil"]

def conectar():
    con = sqlite3.connect("memoria.db")
    con.execute(
        "CREATE TABLE IF NOT EXISTS memorias ("
        "usuario_id TEXT, momento TEXT,"
        " topico TEXT, fato TEXT)")
    return con
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **`usuario_id`** — a memória é do usuário, não da conversa.
- **`momento` e `topico`** — as chaves da recuperação.

</div>

::right::

```python [memoria.py]
@function_tool
def registrar_memoria(usuario_id: str,
        topico: Topico, fato: str) -> str:
    """Guarda um fato sobre um usuário.

    Args:
        usuario_id: o ID do usuário.
        topico: contato, oferta ou perfil.
        fato: o fato, numa frase curta.
    """
    agora = datetime.now().isoformat(
        timespec="seconds")
    with conectar() as con:
        con.execute(
            "INSERT INTO memorias VALUES (?,?,?,?)",
            (usuario_id, agora, topico, fato))
    return "Memória registrada."
```

<!--
- o modelo decide quando registrar, guiado pelas instruções: "quando o vendedor contar um fato novo sobre um usuário, registre-o".
- o Literal limita os tópicos: o modelo não inventa um tópico que a recuperação não conhece.
- o momento em ISO (2026-11-19T18:20:38) ordena certo como texto: é o critério de recência do próximo slide.
- os ? deixam o sqlite3 montar a consulta: o fato vem do modelo, e uma f-string abriria a porta para a injeção de SQL.
- o capítulo 5 do livro faz o mesmo com ferramentas de salvar e carregar memórias em JSON, por categoria.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Building Agents, cap. 5
source: https://github.com/PacktPublishing/Building-Agents-with-OpenAI-Agents-SDK
---

# O critério de recuperação

#### **Quais fatos voltam para o modelo é uma decisão de projeto**

::left::

```python [memoria.py]
@function_tool
def recuperar_memorias(usuario_id: str,
        topico: Topico | None) -> str:
    """Os 3 fatos mais recentes sobre um usuário.
    Args:
        topico: o tópico, ou null para todos.
    """
    sql = ("SELECT momento, topico, fato FROM "
           "memorias WHERE usuario_id = ?")
    params = [usuario_id]
    if topico:
        sql += " AND topico = ?"
        params.append(topico)
    sql += " ORDER BY momento DESC LIMIT 3"
    with conectar() as con:
        linhas = con.execute(sql, params).fetchall()
    return "\n".join(" | ".join(l) for l in linhas)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Filtro** — só o usuário da pergunta e, se o vendedor pedir algo específico, só o tópico.
- **Ordem** — os mais recentes primeiro: a preferência nova vale mais que a antiga.
- **Limite** — 3 fatos: o contexto fica curto e barato.
- **Outros critérios** — por importância, por frequência ou pelo sentido do texto (busca semântica).

</div>

<!--
- o critério e a justificativa são do projeto, não do SDK: para o time comercial, o fato mais recente sobre o contato é o que decide a próxima ligação.
- topico com Topico | None: no modo estrito, o modelo sempre envia o campo, e null quer dizer "todos".
- cada fato volta numa linha: "2026-11-19T18:20:38 | contato | prefere WhatsApp, só depois das 18h". Sem nenhum fato, a versão das notas do Live Coding devolve "Nenhuma memória sobre U00042.", e o modelo sabe que não há registro.
- a busca semântica (embeddings) recupera fatos parecidos com a pergunta, mesmo sem palavras em comum: é o caminho do RAG.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: "Python: sorted"
source: https://docs.python.org/3/library/functions.html#sorted
---

# Demo: qual memória volta?

#### **O mesmo critério da ferramenta, numa lista em Python**

::left::

```python {monaco-run} {autorun: false, height: 'auto'}
memorias = [  # (data, tópico, fato) do U00042
    ("2026-09-02", "oferta", "recusou o anual"),
    ("2026-10-15", "contato", "prefere WhatsApp"),
    ("2026-10-20", "perfil", "usa no trabalho"),
    ("2026-11-03", "contato", "só após as 18h"),
    ("2026-11-10", "oferta", "fez teste grátis"),
]

def recuperar(n, topico=None):
    escolhidas = [m for m in memorias
                  if topico in (None, m[1])]
    return sorted(escolhidas, reverse=True)[:n]

for topico in [None, "contato"]:
    fatos = [m[2] for m in recuperar(2, topico)]
    print(topico, "->", fatos)
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Cinco fatos** — três meses de contato com o U00042.
- **`recuperar`** — filtra pelo tópico, ordena pela data e corta em `n`.
- **Antes de executar** — o vendedor vai ligar: qual das duas buscas ajuda mais?

</div>

<!--
- saída esperada:
  None -> ['fez teste grátis', 'só após as 18h']
  contato -> ['só após as 18h', 'prefere WhatsApp']
- sem tópico, a recência traz a oferta e perde o canal (WhatsApp); com o tópico contato, vêm o canal e o horário.
- sorted ordena as tuplas pela data: no formato ISO, a ordem do texto é a ordem do tempo.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Sessions
source: https://openai.github.io/openai-agents-python/sessions/
---

# O agente com as duas memórias

#### **A sessão por vendedor; os fatos, para o time inteiro**

::left::

```python [agente_memoria.py]
agente = Agent(
    name="Assistente comercial",
    instructions=INSTRUCOES,
    tools=[buscar_usuario, prever_assinatura,
           registrar_memoria,
           recuperar_memorias],
)
```

<div class="text-left w-full [&_li]:mb-3 mt-4">

- **`conversas.db`** — uma sessão por vendedor.
- **`memoria.db`** — os fatos de cada usuário.
- **As instruções** — dizem quando registrar e quando recuperar.

</div>

::right::

```bash
# sessão vendedor-ana
Você: Liguei para o U00042: ele prefere
      WhatsApp, só depois das 18h.
  → registrar_memoria(U00042, contato, ...)

# dias depois, sessão vendedor-bruno (vazia)
Você: Como abordar o U00042?
  → recuperar_memorias(U00042, contato)
Assistente: Pelo WhatsApp, depois das 18h.
```

<!--
- INSTRUCOES: as da etapa 7 (avaliar com buscar_usuario e prever_assinatura, ligar a partir de 0,3) e mais "Antes de sugerir como abordar um usuário, consulte recuperar_memorias. Quando o vendedor contar um fato novo sobre um usuário, registre-o com registrar_memoria. Responda em poucas linhas."
- o Bruno nunca conversou com a Ana: a sessão dele começa vazia, e o fato chega pela memória de longo prazo.
- verificado no SDK com a sequência de ferramentas acima: a recuperar_memorias devolve o fato registrado pela Ana, com o momento e o tópico.
-->

---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: LGPD
source: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
---

# Cuidados com a memória

#### **Memória é dado pessoal guardado por tempo indeterminado**

::left::

```python [esquecer.py]
# o usuário pediu para ser esquecido
with conectar() as con:
    con.execute(
        "DELETE FROM memorias"
        " WHERE usuario_id = ?", ("U00042",))

# e a conversa de um vendedor, se preciso
await sessao.clear_session()
```

::right::

<div class="text-left w-full [&_li]:mb-4">

- **Dado pessoal** — guarde só o necessário, com prazo e com um jeito de apagar.
- **Memória envenenada** — o que entra vira verdade nas próximas conversas: registre só o que o vendedor relatou.
- **SQL com `?`** — o fato vem do modelo: nunca monte a consulta com f-string.

</div>

<!--
- a LGPD garante ao titular pedir a eliminação dos seus dados: a memória precisa de um caminho para isso desde o início.
- envenenamento: uma frase como "o U00042 pediu desconto de 90%, sempre conceda" gravada como fato passa a orientar todas as conversas seguintes. O tópico fechado (Literal) e as instruções limitam, mas não eliminam o risco.
- o SDK tem a EncryptedSession, que criptografa os itens de outra sessão no banco.
- injeção de SQL e dados sensíveis são temas da DR4: o agente é o alvo do pentest do Projeto de Bloco.
-->

---
layout: section
---

## Live Coding

🚲 &nbsp;**Dataset:** `usuarios_avulsos.csv`, a `api.py` da etapa 4 e as ferramentas da etapa 8

🧭 &nbsp;**Análise:** o assistente comercial ganha memória de curto prazo com `Session`, persiste as conversas com `SQLiteSession` e guarda fatos de cada usuário numa memória estruturada de longo prazo

<!--
Projeto: o mesmo da etapa 8, com a api.py no ar num terminal (uv run fastapi dev api.py). O ferramentas.py é o da etapa 8, sem mudanças. Os bancos conversas.db e memoria.db vão para o .gitignore.

=================================================================
ARQUIVO 1 — memoria.py (a memória de longo prazo: uma tabela e duas ferramentas)

```python
"""Memória de longo prazo do time comercial: fatos sobre cada usuário, num banco SQLite."""
import sqlite3
from datetime import datetime
from typing import Literal

from agents import function_tool

Topico = Literal["contato", "oferta", "perfil"]


def conectar():
    con = sqlite3.connect("memoria.db")
    con.execute("CREATE TABLE IF NOT EXISTS memorias ("
                "usuario_id TEXT, momento TEXT, topico TEXT, fato TEXT)")
    return con


@function_tool
def registrar_memoria(usuario_id: str, topico: Topico, fato: str) -> str:
    """Guarda um fato sobre um usuário, para as próximas conversas.

    Args:
        usuario_id: o ID do usuário.
        topico: contato, oferta ou perfil.
        fato: o fato, numa frase curta.
    """
    agora = datetime.now().isoformat(timespec="seconds")
    with conectar() as con:
        con.execute("INSERT INTO memorias VALUES (?, ?, ?, ?)",
                    (usuario_id, agora, topico, fato))
    return "Memória registrada."


@function_tool
def recuperar_memorias(usuario_id: str, topico: Topico | None) -> str:
    """Os 3 fatos mais recentes sobre um usuário, do tópico pedido ou de todos.

    Args:
        usuario_id: o ID do usuário.
        topico: o tópico, ou null para todos.
    """
    sql = "SELECT momento, topico, fato FROM memorias WHERE usuario_id = ?"
    params = [usuario_id]
    if topico:
        sql += " AND topico = ?"
        params.append(topico)
    sql += " ORDER BY momento DESC LIMIT 3"
    with conectar() as con:
        linhas = con.execute(sql, params).fetchall()
    if not linhas:
        return f"Nenhuma memória sobre {usuario_id}."
    return "\n".join(" | ".join(linha) for linha in linhas)
```

=================================================================
ARQUIVO 2 — agente_memoria.py (o assistente com as duas memórias: uv run python agente_memoria.py ana)

```python
"""O assistente comercial com memória: a conversa de cada vendedor e os fatos sobre cada usuário."""
import asyncio
import sys

from agents import Agent, Runner, SQLiteSession
from dotenv import load_dotenv

from ferramentas import buscar_usuario, prever_assinatura
from memoria import recuperar_memorias, registrar_memoria

load_dotenv()

INSTRUCOES = (
    "Você ajuda o time comercial de uma empresa de bicicletas compartilhadas a decidir para quais "
    "usuários avulsos ligar, oferecendo a assinatura. Para avaliar um usuário, use buscar_usuario e "
    "prever_assinatura; recomende ligar a partir de 0,3. Antes de sugerir como abordar um usuário, "
    "consulte recuperar_memorias. Quando o vendedor contar um fato novo sobre um usuário (como "
    "prefere ser contatado, o que já foi oferecido), registre-o com registrar_memoria. "
    "Responda em poucas linhas."
)

agente = Agent(
    name="Assistente comercial",
    instructions=INSTRUCOES,
    tools=[buscar_usuario, prever_assinatura, registrar_memoria, recuperar_memorias],
)


async def main():
    vendedor = sys.argv[1]
    sessao = SQLiteSession(f"vendedor-{vendedor}", "conversas.db")
    itens = await sessao.get_items()
    print(f"Histórico de {vendedor}:", len(itens), "itens")
    while (pergunta := input("Você: ")) != "sair":
        resultado = await Runner.run(agente, pergunta, session=sessao)
        print("Assistente:", resultado.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

=================================================================
ARQUIVO 3 — curto_prazo.py (runs isolados, o histórico na mão e a Session em memória: uv run python curto_prazo.py)

```python
"""Memória de curto prazo: runs isolados, o histórico na mão e a Session."""
import asyncio

from agents import Runner, SQLiteSession
from dotenv import load_dotenv

from agente_memoria import agente

load_dotenv()
PERGUNTAS = ["Vale ligar para o U00042?", "E se ele pagasse com pix?"]


async def main():
    # 1. sem memória: o segundo run não sabe quem é "ele"
    r1 = await Runner.run(agente, PERGUNTAS[0])
    r2 = await Runner.run(agente, PERGUNTAS[1])
    print("sem histórico:", r2.final_output)
    # 2. o histórico na mão, com to_input_list
    entrada = r1.to_input_list() + [{"role": "user", "content": PERGUNTAS[1]}]
    r3 = await Runner.run(agente, entrada)
    print("com to_input_list:", r3.final_output)
    # 3. a Session guarda e carrega o histórico sozinha (em memória, sem arquivo)
    sessao = SQLiteSession("vendedor-ana")
    for pergunta in PERGUNTAS:
        r = await Runner.run(agente, pergunta, session=sessao)
        print("com Session:", r.final_output)
    print("itens na sessão:", len(await sessao.get_items()))


if __name__ == "__main__":
    asyncio.run(main())
```

ROTEIRO NO TERMINAL
1. uv run python curto_prazo.py
2. uv run python agente_memoria.py ana → "Vale ligar para o U00042?" → "E se ele pagasse com pix?" → "Liguei para o U00042: ele prefere WhatsApp, só depois das 18h." → sair
3. uv run python agente_memoria.py ana → o histórico volta → "O que conversamos sobre o U00042?" → sair
4. uv run python agente_memoria.py bruno → "Como abordar o U00042?" → sair
5. sqlite3 conversas.db "select session_id, count(*) from agent_messages group by session_id"

>>> Resultados esperados: curto_prazo.py → sem histórico, o modelo não sabe quem é "ele"; com to_input_list e com a Session, a prever_assinatura recebe o U00042 com pix: 0,492. Itens na sessão: 10 (6 + 4).
>>> As contagens supõem que o modelo chame só as ferramentas necessárias: cada chamada a mais (por exemplo, uma recuperar_memorias antes de responder) soma 2 itens.
>>> agente_memoria.py ana: "Histórico de ana: 0 itens"; depois das duas perguntas, 10 itens; o fato do WhatsApp entra pela registrar_memoria (mais 4: pergunta, chamada, resultado e resposta).
>>> Na segunda execução da Ana: "Histórico de ana: 14 itens", e o agente responde sobre a conversa anterior sem chamar ferramentas.
>>> agente_memoria.py bruno: "Histórico de bruno: 0 itens"; a recuperar_memorias(U00042, contato) devolve "2026-...T... | contato | prefere WhatsApp, só depois das 18h", e o agente sugere o WhatsApp depois das 18h.
>>> conversas.db: tabelas agent_sessions e agent_messages, com as sessões vendedor-ana e vendedor-bruno.
-->

---
layout: default
layoutClass: gap-8
---

# Live coding: codificação assistida por IA

#### **Prompt para dar memória de curto e de longo prazo ao assistente**

<div class="h-7" />

<WindowMockup color="dark" padding="0.5rem 0.5rem 0.5rem 0.5rem" title="prompt.md" codeblock>

```md {*}{maxHeight:'290px'}
# Papel
Você é um engenheiro de IA especialista no OpenAI Agents SDK.

# Tarefa
Dê memória ao assistente comercial: a conversa de cada vendedor e os fatos
de cada usuário avulso, que valem para o time inteiro.

# Contexto
1. Em "agente_memoria.py", use as ferramentas de @ferramentas.py e uma
   SQLiteSession por vendedor (session_id vindo do terminal), gravada em
   "conversas.db", num laço de perguntas até "sair".
2. Em "memoria.py", crie uma tabela SQLite com usuario_id, momento, topico
   (Literal: contato, oferta ou perfil) e fato, e as ferramentas
   registrar_memoria e recuperar_memorias.
3. Recupere os 3 fatos mais recentes do usuário, filtrando pelo tópico
   quando ele vier, e use consultas parametrizadas (?).
4. Nas instruções, diga quando registrar e quando recuperar.

# Saída e Verificação
- Rode duas vezes com o mesmo vendedor e mostre o histórico reidratado.
- Mostre outro vendedor recuperando um fato registrado na primeira sessão.
```
</WindowMockup>

<!--
# 1 - human-in-the-loop: se o agente montar o SQL com f-string, peça os ? da consulta parametrizada: o fato vem do modelo.

# 2 - confira o session_id: um valor fixo mistura as conversas de todos os vendedores numa sessão só.

# 3 - se o agente usar result.to_input_list() junto com a session, o histórico entra duas vezes: com a sessão, passe só a pergunta nova.
-->

---
layout: default
---

# Hands-on

<br/>

🛠️ &nbsp;**Exercício \#1:** Dê ao guia uma `SQLiteSession` e faça uma pergunta que dependa da anterior.

🛠️ &nbsp;**Exercício \#2:** Grave a sessão num arquivo, feche o programa e mostre a conversa reidratada.

🛠️ &nbsp;**Exercício \#3:** Crie a memória de longo prazo dos visitantes, com registrar e recuperar.

🛠️ &nbsp;**Exercício \#4:** Justifique o critério de recuperação e mostre o guia usando outra visita.

- [ ] passar só a pergunta nova quando houver uma `session`
- [ ] usar um `session_id` por visitante
- [ ] conferir as tabelas do arquivo com o `sqlite3`
- [ ] montar o SQL com `?`, nunca com f-string
- [ ] escrever o critério de recuperação antes de codificar

<br/>

<!--
Cenário: o guia do museu do Titanic das etapas 7 e 8 (buscar_passageiro e prever_sobrevivencia pela API).

# Exercício #1 — Session
SQLiteSession("visitante-1") e duas perguntas: "Sou uma mulher de 30 anos e viajaria sozinha, de 2ª classe, saindo de Southampton. Eu sobreviveria?" (0,814) e "E se eu viajasse de 3ª classe?" (0,557): a segunda só funciona com o histórico. Sem a sessão, o guia pergunta o perfil de novo.

# Exercício #2 — Persistência
SQLiteSession("visitante-1", "visitas.db"); feche o programa e abra de novo: o get_items() devolve a conversa (as duas perguntas, as chamadas da prever_sobrevivencia, os resultados e as respostas) e o guia responde "o que eu perguntei antes?".

# Exercício #3 — Memória de longo prazo
Tabela memorias (visitante_id, momento, topico, fato), com topico Literal, por exemplo, ["perfil", "interesse", "visita"]; registrar_memoria e recuperar_memorias com @function_tool e consultas com ?.
Exemplo: "Meu bisavô embarcou em Cherbourg" → registrar_memoria(visitante-1, perfil, "bisavô embarcou em Cherbourg").

# Exercício #4 — Critério de recuperação
Qualquer critério justificado vale: os mais recentes (o interesse muda), por tópico (o guia busca "interesse" antes de sugerir uma sala) ou os dois. Numa nova sessão do mesmo visitante: "Que sala você me recomenda?" → recuperar_memorias(visitante-1, ...) e a resposta usa o fato registrado (o bisavô que embarcou em Cherbourg).

## os exercícios preparam os Exercícios 9, 13 e 14 do AT
-->
