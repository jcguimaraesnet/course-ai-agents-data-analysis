---
theme: dracula
title: "Estatística e EDA"
info: |
  Estatística Aplicada e Análise Exploratória de Dados
  Análise e Segurança de Agentes de IA
# hash: reload num slide bate em .../statistics-eda/ (index da pasta), o GitHub Pages serve
# 200 e a SPA roteia pelo hash. Evita 404 em subpath sem regra de rewrite.
routerMode: hash
colorSchema: dark
fonts:
  sans: DM Sans
  weights: "200,400,600,700"
contextMenu: false
highlighter: shiki
lineNumbers: true
transition: fade-out
# comark: sintaxe de componentes no markdown (ex.: `::code-group` nos slides de instalação da etapa 1)
comark: true
layout: cover
footer: false
presenter: true
addons:
  - window-mockup
  - slidev-addon-python-runner
# python-runner: executa os blocos {monaco-run} no navegador (Pyodide, com pandas 2.x)
python:
  installs: []
  loadPackagesFromImports: true
  suppressDeprecationWarnings: true
  alwaysReload: false
  loadPyodideOptions: {}
---

# Estatística Aplicada e Análise Exploratória de Dados

Análise e Segurança de Agentes de IA

---
routeAlias: ementa
---

# Ementa do curso

- **Etapa 1** — <Link to="etapa1" title="Manipulação Básica de Dados"/>
- **Etapa 2** — <Link to="etapa2" title="Avanços em Manipulação de Dados"/>
- **Etapa 3** — <Link to="etapa3" title="Probabilidades e Análise Gráfica"/>
- **Etapa 4** — <Link to="etapa4" title="Análise de Relações Numéricas"/>
- **Etapa 5** — <Link to="etapa5" title="Análise e Limpeza com IA"/>
- **Etapa 6** — <Link to="etapa6" title="Avaliação de Hipóteses com IA"/>
- **Etapa 7** — <Link to="etapa7" title="Regressão Linear e Avaliação"/>
- **Etapa 8** — <Link to="etapa8" title="Avaliação e Modelagem de Regressão"/>
- **Etapa 9** — <Link to="etapa9" title="Pipeline de EDA com Python"/>

<!--
Ementa do curso — visão geral das 9 etapas.
-->

---
title: Sobre mim
layout: custom-author
imageSide: right
---

::title::
# Júlio César Guimarães

::image::
![image](https://github.com/jcguimaraesnet.png?size=500)

::default::
- Professor desde 2020 no Infnet
- Mestrando em EngSoft com IA (UFRJ)
- MBA em Engenharia de Software (UFRJ)
- \+ 20 anos de experiência
- \+ 10 Certificações Microsoft
- 6x MCT (Microsoft Certified Trainer)

::links::
<div><logos-linkedin-icon /> <a href="https://linkedin.com/in/jcguimaraesnet" target="_blank">linkedin.com/in/jcguimaraesnet</a></div>

<div><GitHubIcon /> <a href="https://github.com/jcguimaraesnet" target="_blank">jcguimaraesnet</a></div>

---
layout: image-x
imageOrder: 2
glowSeed: 314
image: /pessoas-apresentacao.jpg
---

::title::

# Apresentação

::default::

- Estágio?
- Transição de carreira?
- Desenvolve?
- Expectativa?

---
layout: two-cols-header
layoutClass: gap-8
class: flex items-center justify-center
---

# Bibliografia do curso

::left::

<AssetImg src="book-pandas-for-everyone.jpg" class="rounded-lg h-70" />

::right::

<AssetImg src="book-the-pandas-workshop.jpg" class="rounded-lg h-70" />

---
layout: two-cols-header
layoutClass: gap-8
class: flex items-center justify-center
---

# Bibliografia do curso

::left::

<AssetImg src="book-statistics-every-programmer-needs.jpg" class="rounded-lg h-70" />

::right::

<AssetImg src="book-starting-data-analytics-with-generative-ai.jpg" class="rounded-lg h-70" />

---
class: flex flex-col
---

# Bibliografia do curso

<div class="grid grid-cols-3 gap-8 flex-1 items-center">
  <div class="flex flex-col items-center gap-4">
    <teenyicons-doc-outline class="text-7xl text-cyan-400" />
    <a href="https://pandas.pydata.org/docs/" target="_blank">pandas.pydata.org/docs</a>
  </div>
  <div class="flex flex-col items-center gap-4">
    <teenyicons-doc-outline class="text-7xl text-cyan-400" />
    <a href="https://seaborn.pydata.org/" target="_blank">seaborn.pydata.org</a>
  </div>
  <div class="flex flex-col items-center gap-4">
    <teenyicons-doc-outline class="text-7xl text-cyan-400" />
    <a href="https://docs.scipy.org/doc/scipy/reference/stats.html" target="_blank">docs.scipy.org (scipy.stats)</a>
  </div>
</div>

---
src: ./pages/statistics-eda/slide-etapa1.md
---

---
src: ./pages/statistics-eda/slide-etapa2.md
---

---
src: ./pages/statistics-eda/slide-etapa3.md
---

---
src: ./pages/statistics-eda/slide-etapa4.md
---

---
src: ./pages/statistics-eda/slide-etapa5.md
---

---
src: ./pages/statistics-eda/slide-etapa6.md
---

---
src: ./pages/statistics-eda/slide-etapa7.md
---

---
src: ./pages/statistics-eda/slide-etapa8.md
---

---
src: ./pages/statistics-eda/slide-etapa9.md
---
