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
- **Addons:** os decks ativam só o `window-mockup` (`addons:` no headmatter). O `slidev-addon-python-runner` está instalado, mas só funciona se for incluído em `addons:` do deck.

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
