# AGENTS.md — Slides do bloco Análise e Segurança de Agentes de IA

Instruções para agentes que trabalham neste repositório: os decks [Slidev](https://sli.dev) das disciplinas do bloco **Análise e Segurança de Agentes de IA**.

> **Padrão de instruções: `AGENTS.md`, não `CLAUDE.md`.** Não crie `CLAUDE.md` neste repositório. O Claude Code carrega o `AGENTS.md` automaticamente quando não há `CLAUDE.md`, e criar um faria o `AGENTS.md` deixar de ser lido. Ao mudar a estrutura do repo (novo deck, layout, componente, skill), atualize este arquivo.

> **Idioma das respostas: português do Brasil.** Toda resposta do agente (Claude Code ou outro) nos chats sobre este repositório deve ser escrita em pt-BR, inclusive resumos, perguntas ao usuário e mensagens de commit.

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
- **Addons:** os dois decks ativam o `window-mockup` e o `slidev-addon-python-runner` (com a configuração `python:` no headmatter), que executa os blocos `{monaco-run}` no navegador. As demos de `predictive-modeling` importam o scikit-learn, que o Pyodide carrega sozinho pelos imports (versão 1.4: a primeira execução demora alguns segundos).
- **Demos `{monaco-run}`:** rodam no Pyodide 0.26, que traz o **pandas 2.x**: texto aparece como `object`, não `str`, e o copy-on-write do pandas 3 só vale se a demo ligar `pd.options.mode.copy_on_write = True`. Use **um bloco executável por slide** (com dois, o addon joga a saída de um no painel do outro) e capture erros esperados com `try/except`, para não exibir o traceback longo do Pyodide. Avisos longos também estouram o slide: resuma-os com `warnings.catch_warnings(record=True)`.
- **Largura das demos:** numa coluna de `two-cols-header`, o editor quebra linhas com mais de ~50 caracteres. Divida a linha ou mova o comentário, e confira no navegador se a saída cabe acima do rodapé depois de executar.
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
- **Etapas 5 e 6:** a etapa 5 refaz a limpeza da etapa 2 com código gerado por IA, a partir dos exports brutos, e a confere com o pipeline manual (`limpeza_manual()`, nas notas do Live Coding); a análise descritiva volta à `carregar_base()`. A etapa 6 compara a nota média com e sem chuva (diferença grande e relevante) e de avulsos e assinantes (0,05 ponto, significativa, mas explicada pela duração). As demos recriam as notas de cada grupo a partir das contagens (`np.repeat`).
- **Etapas 7 e 8:** a regressão da duração pela distância e, na etapa 8, também pelo tipo de usuário e pela chuva, sempre com `train_test_split(test_size=0.2, random_state=42)`. O par `choveu` × `chuva_mm` (r = 0,79) mostra a multicolinearidade, e a `velocidade_kmh`, calculada com a própria duração, mostra o vazamento.
- **Etapa 9 e datasets reais:** o pipeline do live coding usa as corridas de táxi de Nova York (`taxis.csv` do repositório `mwaskom/seaborn-data`), um dataset real. Os hands-on das etapas 8 e 9 usam o `mpg`, o `penguins`, o `diamonds` e o `tips`, também do seaborn. O AT usa a base da Olist: não a use nos slides, para não antecipar a solução.
### Base de dados das aulas (Modelagem Preditiva)

- **Fio condutor:** a mesma empresa de bicicletas da DR1, agora com `usuarios_avulsos.csv`: 3.000 usuários avulsos no primeiro mês e o alvo `virou_assinante` (28,5%). O `gerar_dados.py` (seed 42) está nas notas do Live Coding da etapa 1; a `avaliacao_media` tem 8% de ausentes, tratados com `SimpleImputer` na etapa 2.
- **Divisões:** a etapa 1 usa o `train_test_split` sem estratificar (o da DR1) e só as três numéricas sem ausentes; a etapa 2 estratifica e usa as sete features. Sempre `test_size=0.2` e `random_state=42`.
- **Classificadores:** a disciplina fica só com a regressão logística e o SVM; árvores de decisão, ensembles, KNN e Naive Bayes estão fora, por decisão pedagógica (orientações do TP2). Na etapa 1, bias e variância aparecem com a regressão logística sobre termos polinomiais (`PolynomialFeatures(8)`), variando o `C`; a regressão logística só é explicada na etapa 3, e os slides dizem isso.
- **Etapa 3:** recarrega o `pipeline_assinatura.joblib` da etapa 2 (`C = 0,1`) com a mesma divisão (`dividir`) e o avalia sem retreinar: matriz de confusão, thresholds com o número de ligações do time comercial, curva ROC contra o modelo das três numéricas da etapa 1 e a sigmoid refeita à mão.
- **Etapa 4:** acrescenta ao final do `gerar_dados.py` o trecho que gera o `motivos_uso.csv` (lazer, trabalho ou estudo, sorteado por uma softmax; 10% pularam a pergunta), sem mudar o `usuarios_avulsos.csv`. O SVM começa num protótipo separável (viagens × idade, 2 vetores de suporte) e passa a todos os usuários; a comparação final mostra a regressão logística à frente do SVC com kernel RBF (AUC 0,864 contra 0,819). A etapa termina servindo o pipeline com FastAPI (`api.py`), o elo com a API da DR2.
- **Etapas 5 e 6:** ainda sem slides. As etapas 7 a 9 supõem que elas apresentem o `Agent`, o `Runner` (`Runner.run` assíncrono) e a saída estruturada `Recomendacao` (`usuario_id`, `probabilidade`, `ligar`, `prioridade` em `Literal` e `motivo`) do assistente comercial.
- **Etapas 7 a 9 (agentes):** o fio é o **assistente comercial**, que decide para quais usuários avulsos ligar. Na etapa 7, ele ganha as ferramentas `buscar_usuario` (lê o CSV sem `virou_assinante`) e `prever_assinatura` (entrada `PerfilUsuario` em Pydantic, pipeline em processo), e o ciclo é controlado com `tool_choice` e `tool_use_behavior` (U00042: 0,464, 3 chamadas ao modelo). Na etapa 8, o `ferramentas.py` é reescrito: a `prever_assinatura` chama a `api.py` da etapa 4 com `requests` (timeout e falhas tratadas), entra a `previsao_chuva` (Open-Meteo, sem chave) e uma função em `tool_use_behavior` encerra o ciclo na ferramenta. Na etapa 9, a conversa vai para uma `SQLiteSession` por vendedor (`conversas.db`) e os fatos de cada usuário, para a memória de longo prazo em `memoria.db` (`registrar_memoria` e `recuperar_memorias`: os 3 mais recentes, com filtro opcional de tópico).
- **Conferência do código dos agentes:** sem chave da OpenAI, o código das notas roda com um modelo falso que segue um roteiro de chamadas de ferramenta (uma subclasse de `agents.models.interface.Model`), contra a `api.py` de verdade, numa porta livre. As demos `{monaco-run}` dessas etapas não usam rede (o Pyodide não abre conexões): simulam as exceções do `requests` e usam respostas fixas da API.
- **Hands-on:** o Titanic do seaborn (`sns.load_dataset("titanic")`); a etapa 4 usa também o `penguins` (espécies, para a softmax e a margem máxima). Nas etapas 7 a 9, o Titanic vira o **guia do museu**, com o pipeline do hands-on da etapa 2 (`pipeline_titanic.joblib`) como ferramenta, depois atrás de uma API, e a Marine API da Open-Meteo no local do naufrágio. Os TPs usam a base sintética da NeoStream e o AT, a Telco Customer Churn: não use nenhuma das duas nos slides.

- **Gráficos estáticos (`public/eda-*.png` e `public/pm-*.png`):** saem da skill `slide-charts`, que monta essa base com o código das notas e desenha no tema escuro dos slides (paleta validada para daltonismo, vírgula decimal). Crie ou refaça gráficos sempre por ela; a paleta fica em `.claude/skills/slide-charts/scripts/tema.py`. Os do deck `predictive-modeling` (`pm-*.png`) saem da base das notas da etapa 1 desse deck.

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
- **`slide-charts`** — gera e regenera os gráficos estáticos dos slides (`public/eda-*.png`) com a base das aulas e o tema escuro: `uv run .claude/skills/slide-charts/scripts/gerar.py --lista`.

## Arquivos temporários

Prints e exports rápidos vão para `tmp/`. A pasta existe no repo, mas o conteúdo é ignorado pelo git ([tmp/.gitignore](tmp/.gitignore)).
