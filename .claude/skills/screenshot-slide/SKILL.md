---
name: screenshot-slide
description: Gera um print (PNG) de um slide do deck Slidev deste repo, renderizado no navegador. Use quando o usuário pedir "tira um print do slide 37", "me mostra como ficou o slide 12", "screenshot da abertura da etapa 9", "printa os slides 30 a 32" — inclusive quando o slide é identificado de forma indireta ("o primeiro slide da etapa 9", "o último slide do deck de modelagem preditiva"). Não use para apenas ler ou editar o conteúdo do slide (aí basta abrir o markdown, com apoio da skill locate-slide).
---

# Print de um slide

Slidev não tem comando de CLI que capture um slide isolado (`slidev export` gera
PDF/PNG do deck inteiro e exige `playwright-chromium`, que **não** está instalado
aqui). O caminho que funciona é: subir o dev server e capturar pelo navegador via
Playwright MCP.

## 1. Descobrir o deck e o número global do slide

O número que aparece no rodapé da apresentação é **global no deck** — ele não
reinicia a cada etapa. Quem resolve isso é a skill
[locate-slide](../locate-slide/SKILL.md), que usa o parser do próprio Slidev.

| Deck | `--deck` | Entry | Porta |
|------|----------|-------|-------|
| Estatística e EDA | `statistics-eda` | `slides-statistics-eda.md` | 3333 |
| Modelagem Preditiva | `predictive-modeling` | `slides-predictive-modeling.md` | 3434 |

Se o usuário já deu o número, valide-o (e confirme o arquivo):

```bash
node .claude/skills/locate-slide/scripts/locate-slide.mjs --deck statistics-eda 165
```

Se o usuário identificou o slide de forma indireta — "o primeiro slide da etapa
9" —, tire o número do índice completo:

```bash
node .claude/skills/locate-slide/scripts/locate-slide.mjs --deck statistics-eda --list --json
```

Cada item traz `slide` (número global), `file`, `title` e `total`. Filtre por
`file` para achar o intervalo da etapa: o primeiro slide da etapa 9 é o menor
`slide` cujo `file` é `pages/statistics-eda/slide-etapa9.md`.

## 2. Subir o dev server (se ainda não estiver de pé)

```bash
pnpm dev:statistics-eda       # statistics-eda       :3333
pnpm dev:predictive-modeling  # predictive-modeling  :3434
```

Rode em background e espere a porta responder antes de navegar:

```bash
until curl -s -o /dev/null http://localhost:3333/; do sleep 1; done
```

Reaproveite um servidor já rodando — subir de novo na mesma porta faz o Vite cair
para a porta seguinte (o `--strictPort` foi removido no Slidev 52, então não há
erro: ele só troca a porta silenciosamente). Na dúvida, confira a URL real na
saída do processo.

## 3. Capturar com o Playwright MCP

```
browser_navigate       http://localhost:3333/#/165
browser_resize         1280 x 720
browser_take_screenshot  filename: tmp/slide-165-etapa9.png
```

Três detalhes que custam uma tentativa perdida cada:

- **`routerMode: hash`** nos três decks — a URL do slide é `/#/165`, não `/165`.
- **A primeira captura sai em branco.** O dev server compila o deck sob demanda;
  navegar retorna antes de a página pintar. Depois do `browser_navigate`, espere
  ~15s (ou até o `.yml` do snapshot deixar de ter 0 byte) e só então capture. Se
  o PNG vier com poucos KB e todo branco, foi isso: repita a captura.
- **O Playwright MCP só escreve dentro do repo.** Caminho absoluto para fora
  (inclusive o scratchpad) é recusado — passe `filename` relativo.

Viewport 1280×720 dá o 16:9 do slide sem sobra. Use `scale: "device"` para um PNG
mais nítido.

## 4. Onde salvar

Prints vão para **`tmp/`**, que é versionada mas tem o conteúdo ignorado
([tmp/.gitignore](../../../tmp/.gitignore)). Nomeie pelo número e pelo assunto —
`tmp/slide-165-etapa9.png`.

Depois de capturar, entregue a imagem ao usuário com `SendUserFile` (e cite o
`slide N/total` junto do arquivo de origem, para o print ficar rastreável).
