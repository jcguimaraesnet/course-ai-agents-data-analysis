# AGENTS.md — Slides do bloco Análise e Segurança de Agentes de IA

Instruções para agentes que trabalham neste repositório: os decks [Slidev](https://sli.dev) das disciplinas do bloco **Análise e Segurança de Agentes de IA**.

> **Padrão de instruções: `AGENTS.md`, não `CLAUDE.md`.** Não crie `CLAUDE.md` neste repositório. O Claude Code carrega o `AGENTS.md` automaticamente quando não há `CLAUDE.md`, e criar um faria o `AGENTS.md` deixar de ser lido. Ao mudar a estrutura do repo (novo deck, layout, componente, skill), atualize este arquivo.

## Escopo: este repo é PÚBLICO

Aqui vivem só os slides, publicados no GitHub Pages:

- **Repo:** <https://github.com/jcguimaraesnet/course-ai-agents-data-analysis>
- **Slides publicados:** <https://jcguimaraesnet.github.io/course-ai-agents-data-analysis/>

A **base de conhecimento** (planos de ensino, enunciados de TPs e AT, competências, entregas de alunos) vive no repo **privado** irmão `../course-ai-agents-data-analysis-llm-wiki/`. Consulte o `AGENTS.md` de lá para planejar o conteúdo das etapas.

> Nunca copie para cá material privado da wiki: orientações ao professor, gabaritos, rubricas ou qualquer dado de aluno.

## Decks

| Deck | Nome curto | Entry | Páginas | Porta (dev) | URL publicada |
|------|------------|-------|---------|-------------|---------------|
| Estatística Aplicada e Análise Exploratória de Dados (DR1) | `statistics-eda` | `slides-statistics-eda.md` | `pages/statistics-eda/` | 3333 | `/statistics-eda/` |
| Modelagem Preditiva e Construção de Agentes de IA (DR3) | `predictive-modeling` | `slides-predictive-modeling.md` | `pages/predictive-modeling/` | 3434 | `/predictive-modeling/` |

Estrutura de cada deck:

- O **entry** (`slides-<nome>.md`) tem o headmatter (tema `dracula`, `routerMode: hash`, fonte DM Sans), a capa, o slide de **Ementa** (`routeAlias: ementa`) com links para as etapas, e um include `src:` por etapa.
- Cada **etapa** é um arquivo `pages/<nome>/slide-etapaN.md` (N = 1 a 9). O primeiro slide é sempre a abertura da etapa, com `layout: section` e `routeAlias: etapaN`.
- O conteúdo dos slides é escrito em **português**.

### Adicionar um deck

1. Crie `slides-<nome>.md` copiando o headmatter de um deck existente e `pages/<nome>/slide-etapaN.md`.
2. Em `package.json`, crie `dev:<nome>` (porta nova) e `build:<nome>` (`--base /course-ai-agents-data-analysis/<nome>/ --out dist/<nome>`), e encadeie o `build:<nome>` no script `build`.
3. Atualize as tabelas do `README.md`, deste arquivo e da skill `screenshot-slide`.

## Comandos

```bash
pnpm install                    # dependências (o parser do Slidev, usado pela skill locate-slide, vem daqui)
pnpm dev:statistics-eda         # dev server em :3333
pnpm dev:predictive-modeling    # dev server em :3434
pnpm build                      # build dos dois decks em dist/<nome>/
```

## Deploy

**Todo push na `main` publica os slides.** O workflow [.github/workflows/deploy.yml](.github/workflows/deploy.yml) roda `pnpm build` e publica `dist/` no GitHub Pages. Antes de dar push, confira se `pnpm build` passa.

## Convenções

- **Links entre slides:** use `routeAlias` (`<Link to="etapa3" .../>`, `ementa`), nunca o número do slide. Os números mudam quando um slide é inserido antes.
- **URLs de slide:** com `routerMode: hash`, a URL é `/#/N`, não `/N`.
- **Imagens:** coloque em `public/` e use `<AssetImg src="arquivo.png" />` ([components/AssetImg.vue](components/AssetImg.vue)). Um `<img src="/arquivo.png">` quebra no build ou perde o prefixo do `--base` em produção.
- **Títulos:** o CSS ([styles/index.css](styles/index.css)) já põe um `#` antes de `h1`/`h2`. Não escreva `\#` no título; para tirar o prefixo de um slide, use `class: no-hash` no frontmatter.
- **Rodapé por slide** ([slide-bottom.vue](slide-bottom.vue)): `source: <url>` e `sourceLabel: <texto>` mostram a fonte à direita; `footer: false` oculta a barra.
- **Fundo com brilho** ([global-bottom.vue](global-bottom.vue)): `glow`, `glowOpacity`, `glowHue` e `glowSeed` no frontmatter.
- **Diagramas:** Mermaid com `look: handDrawn` e tema escuro ([setup/mermaid.ts](setup/mermaid.ts)).
- **Código:** Monaco em Python, somente leitura ([setup/monaco.ts](setup/monaco.ts)).
- **Addons:** os dois decks ativam o `window-mockup`. O `statistics-eda` também ativa o `slidev-addon-python-runner` (com a configuração `python:` no headmatter), que executa os blocos `{monaco-run}` no navegador.
- **Demos `{monaco-run}`:** rodam no Pyodide 0.26, que traz o **pandas 2.x**: texto aparece como `object`, não `str`. Use **um bloco executável por slide** (com dois, o addon joga a saída de um no painel do outro) e capture erros esperados com `try/except`, para não exibir o traceback longo do Pyodide.
- **Comark:** `::code-group` (abas de código) e outros blocos `::componente` exigem `comark: true` no headmatter. Hoje só o deck `statistics-eda` ativa a opção.
- **Preparação do ambiente (WSL, Antigravity, Python e uv):** os alunos usam Windows com WSL. Esses slides ficam no início da etapa 1 de `statistics-eda`, a primeira disciplina do bloco, e vieram do deck de Agentes de IA (`course-intelligent-agents`).

### Estrutura de uma etapa

Segue o padrão do deck de referência (`course-intelligent-agents`):

1. **Abertura** — `layout: section` com `routeAlias: etapaN`.
2. **Seções** — `layout: section` com o tema e uma linha em negrito com o que será visto.
3. **Conceitos** — quase sempre `two-cols-header`: título `#`, subtítulo `#### **…**`, código de um lado e explicação do outro, `sourceLabel`/`source` apontando para a documentação, e notas do professor em `<!-- -->`.
4. **Live Coding** — `layout: section` com o dataset e a análise; o código de referência completo e os resultados esperados ficam nas notas.
5. **Live coding: codificação assistida por IA** — o prompt do agente numa `WindowMockup` (`prompt.md`), com as seções Papel, Tarefa, Contexto e Saída e Verificação.
6. **Hands-on** — 3 ou 4 exercícios `🛠️ **Exercício \#N:**` (uma linha cada), um checklist `- [ ]` e, nas notas, o detalhe de cada exercício e o que ele prepara no TP.

Antes de publicar, confira os slides novos no navegador (skill `screenshot-slide`): o rodapé ocupa os ~5% inferiores do slide, e texto, tabela ou diagrama não pode invadir essa faixa.

### Base de dados das aulas (Estatística e EDA)

O fio condutor do live coding é uma base fictícia de **viagens de bicicletas compartilhadas**, gerada pelo `gerar_dados.py` (seed 42), cujo código completo está nas notas do Live Coding da etapa 1; a etapa 2 acrescenta o trecho de abril.

- **Arquivos:** `viagens.csv` (jan–mar/2026), `viagens_abril.csv` (etapa 2), `estacoes.xlsx` (12 estações) e `clima.json` (um registro por dia, jan–abr).
- **Defeitos de export:** `duracao_min` como texto com vírgula, ~5% de `duracao_min` e ~15% de `avaliacao` ausentes, ~2% de linhas reenviadas e o export de abril repetindo o 31/03.
- **Relações plantadas para as próximas etapas:** a duração é a distância dividida por uma velocidade (assinantes ~14 km/h, avulsos ~12 km/h), boa para correlação e regressão; dias com chuva acima de 5 mm têm menos viagens (16,9 contra 29,6 por dia) e viagens mais longas; a avaliação cai em viagens longas e com chuva.
- **Hands-on:** usa o Gapminder do livro *Pandas for Everyone* e uma base de outro domínio que cada aluno gera com o agente.
- **Etapas 3 em diante:** a base limpa vem de `carregar_base()`, do módulo `preparar_base.py` (código nas notas do Live Coding da etapa 3). Ele repete o pipeline da etapa 2 sem preencher `duracao_min`, porque a mediana preenchida criaria um pico artificial nas distribuições e distorceria as correlações.
- **Gráficos estáticos (`public/eda-*.png`):** gerados dessa base com matplotlib e seaborn, no tema escuro dos slides. A superfície é `#1e1f29`; as séries usam azul `#3987e5`, laranja `#d95926` e aqua `#199e70` (paleta validada para daltonismo contra essa superfície), e o heatmap usa a divergente azul `#2a78d6`, cinza `#383835` e vermelho `#e66767`. Textos em tons de tinta (`#f0efec`, `#c3c2b7`, `#898781`) e vírgula decimal. Mantenha esse padrão ao refazer ou criar gráficos.

### Layouts e componentes próprios

| Arquivo | Uso |
|---------|-----|
| [layouts/custom-author.vue](layouts/custom-author.vue) | Apresentação de pessoa/autor em duas colunas, via slots (`::title::`, `::subtitle::`, `::image::`, `::links::`). |
| [layouts/image-x.vue](layouts/image-x.vue) | Imagem de um lado e conteúdo do outro (`image`, `imageOrder: 1 \| 2`). |
| [layouts/quote.vue](layouts/quote.vue) | Citação com aspas decorativas (sobrescreve o `quote` do tema). |
| [layouts/quote-image.vue](layouts/quote-image.vue) | Citação com imagem à direita (`image`). |
| [layouts/quote-image-without-quotation-marks.vue](layouts/quote-image-without-quotation-marks.vue) | Texto com imagem ou vídeo à direita, sem aspas (`image` ou `video`, `autoplay`, `loop`). |
| [components/AssetImg.vue](components/AssetImg.vue) | Imagem de `public/` com o `base` correto e recorte lateral opcional (`crop-left`, `crop-right`). |
| [components/GitHubIcon.vue](components/GitHubIcon.vue) | Ícone do GitHub em SVG. |
| [custom-nav-controls.vue](custom-nav-controls.vue) | Botão na barra de navegação que leva ao slide de Ementa. |

## Skills do projeto

Em `.claude/skills/`:

- **`locate-slide`** — acha o arquivo e a linha de um slide pelo número mostrado na apresentação. Use sempre que o usuário citar um slide por número: `node .claude/skills/locate-slide/scripts/locate-slide.mjs --deck <nome curto> <N>`.
- **`screenshot-slide`** — tira um print (PNG) de um slide com o dev server e o Playwright MCP.

## Arquivos temporários

Prints e exports rápidos vão para `tmp/`. A pasta existe no repo, mas o conteúdo é ignorado pelo git ([tmp/.gitignore](tmp/.gitignore)).
