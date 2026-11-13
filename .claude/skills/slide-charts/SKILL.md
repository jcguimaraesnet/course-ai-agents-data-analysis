---
name: slide-charts
description: Gera ou regenera os gráficos estáticos dos slides de Estatística e EDA (os PNGs public/eda-*.png), a partir da base de viagens das aulas e no tema escuro dos slides. Use quando o usuário pedir para criar, refazer ou ajustar um gráfico que aparece como imagem num slide — "regera os gráficos", "cria um gráfico de resíduos para a etapa 7", "muda a cor do boxplot", "põe mais uma coluna no heatmap", "mudei o gerar_dados.py nas notas, atualiza os gráficos". Não use para os gráficos que a turma faz no notebook (esses ficam no código das notas do Live Coding) nem para as demos {monaco-run}.
---

# Gráficos dos slides

Os PNGs `public/eda-*.png` saem dos scripts desta skill. Cada gráfico é uma função Python, e um comando regenera um gráfico, uma etapa ou todos, sempre com a mesma base e o mesmo tema.

| Arquivo | Papel |
|---------|-------|
| `scripts/gerar.py` | Ponto de entrada. As dependências estão fixadas no cabeçalho (PEP 723), e o `uv run` monta o ambiente sozinho. |
| `scripts/dados.py` | Monta a base com o código das notas: o `gerar_dados.py` (etapa 1, mais o trecho de abril da etapa 2) e o `preparar_base.py` (etapa 3) rodam numa pasta temporária. |
| `scripts/tema.py` | Paleta validada, estilo do matplotlib, formatação pt-BR (`virgula`, `pct`) e o registro `@grafico`. |
| `scripts/etapaN.py` | Os gráficos da etapa N, uma função por PNG. |

O código da base **não é copiado** para a skill: ele vem das notas do Live Coding, o mesmo que a turma vê. Se as notas mudarem, os gráficos acompanham na próxima geração, e os números citados nos slides podem mudar junto: confira-os.

## Comandos

Na raiz do repo:

```bash
uv run .claude/skills/slide-charts/scripts/gerar.py --lista                # gráficos registrados, por etapa
uv run .claude/skills/slide-charts/scripts/gerar.py --saida tmp/graficos   # prévia de todos, comparada com public/
uv run .claude/skills/slide-charts/scripts/gerar.py boxplot heatmap        # só os que têm esses trechos no nome
uv run .claude/skills/slide-charts/scripts/gerar.py --etapa 3              # só os da etapa 3
uv run .claude/skills/slide-charts/scripts/gerar.py                        # todos, direto em public/
```

Sem `--saida`, os PNGs vão para `public/`. A primeira linha da saída resume a base (`base: 3119 viagens (2970 com duração)`); numa prévia fora do `public/`, cada PNG vem marcado como igual, diferente ou novo em relação à versão publicada.

## Criar ou ajustar um gráfico

1. **Leia a skill `dataviz`** antes de desenhar: forma, cor pelo papel que ela cumpre, marcas finas e rótulos seletivos.
2. **Escreva a função** em `scripts/etapaN.py` (crie o módulo se a etapa ainda não tiver um). Decorada com `@grafico("eda-<assunto>.png")`, ela recebe a base e devolve a figura; quem salva é o `gerar.py`. Quando o gráfico depender da duração, use `com_duracao(base)`, de `dados.py`: a duração ausente não é preenchida.
3. **Use as cores do `tema.py`**: séries em `AZUL`, `LARANJA` e `AQUA`, nessa ordem; texto em `TINTA`, `TINTA_2` ou `MUDA`, nunca na cor da série; correlação no `DIVERGENTE`, com `vmin=-1` e `vmax=1`. Uma cor nova só entra depois de passar no validador da skill `dataviz`, no modo escuro e contra a superfície do tema:

   ```bash
   node <pasta da skill dataviz>/scripts/validate_palette.js "#3987e5,#d95926,#199e70,<nova>" --mode dark --surface "#1e1f29" --pairs all
   ```

4. **Formate em pt-BR** com `virgula()` e `pct()`: vírgula decimal e sinal de menos tipográfico (−) em todo rótulo.
5. **Dimensione pelo lugar no slide**: `figsize=(6, 4)` numa coluna de `two-cols-header`; de `(10, 3.2)` a `(12, 2.9)` na largura inteira de um slide `default`. Confira a proporção do PNG final (o `bbox_inches="tight"` corta as bordas): abaixo de 3:1, uma linha de texto sob o gráfico invade o rodapé.
6. **Gere a prévia** com `--saida tmp/graficos` e abra o PNG (Read) para conferir rótulos sobrepostos, cortes e a vírgula decimal. Só então gere em `public/`.
7. **No slide**, use `<AssetImg src="eda-<assunto>.png" class="rounded-lg w-full" />` e confira o resultado com a skill `screenshot-slide`.

Dados sintéticos, como os de `eda-padroes-scatter.png`, são gerados dentro da própria função, com seed fixa. Quando o gráfico mostra a simulação de uma demo `{monaco-run}` (como `eda-permutacao-avaliacao.png` e `eda-bootstrap-avaliacao.png`), use a mesma semente, a mesma ordem dos dados e o mesmo número de repetições da demo, para que o gráfico e a saída da demo mostrem os mesmos números.

## Versões fixadas

pandas 3.1.1, numpy 2.5.4, matplotlib 3.11.2, seaborn 0.13.2, scipy 1.18.1 e openpyxl 3.1.5, no cabeçalho do `gerar.py`. Com elas, a base (seed 42) e os pixels se repetem a cada geração: um gráfico que não mudou sai idêntico byte a byte. Para atualizar, troque as versões, gere a prévia e confira o que mudou antes de sobrescrever o `public/`.
