---
theme: dracula
title: "Modelagem Preditiva"
info: |
  Modelagem Preditiva e Construção de Agentes de IA
  Análise e Segurança de Agentes de IA
# hash: reload num slide bate em .../predictive-modeling/ (index da pasta), o GitHub Pages serve
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
layout: cover
footer: false
presenter: true
addons:
  - window-mockup
  - slidev-addon-python-runner
# python-runner: executa os blocos {monaco-run} no navegador (Pyodide, com pandas 2.x e scikit-learn 1.4)
python:
  installs: []
  loadPackagesFromImports: true
  suppressDeprecationWarnings: true
  alwaysReload: false
  # o addon lê "loadOptions"; os pacotes (scikit-learn, scipy, openblas) vêm do CDN oficial do Pyodide 0.26.4
  loadOptions:
    indexURL: https://cdn.jsdelivr.net/pyodide/v0.26.4/full/
---

# Modelagem Preditiva e Construção de Agentes de IA

Análise e Segurança de Agentes de IA

---
routeAlias: ementa
---

# Ementa do curso

- **Etapa 1** — <Link to="etapa1" title="Preparação de Dados para Classificação"/>
- **Etapa 2** — <Link to="etapa2" title="Pipeline e Seleção de Hiperparâmetros"/>
- **Etapa 3** — <Link to="etapa3" title="Avaliação de Classificadores IA"/>
- **Etapa 4** — <Link to="etapa4" title="Classificadores Avançados em IA"/>
- **Etapa 5** — <Link to="etapa5" title="Arquitetura e Configuração de Agentes"/>
- **Etapa 6** — <Link to="etapa6" title="Desenvolvimento de Agentes Assíncronos"/>
- **Etapa 7** — <Link to="etapa7" title="Integração Avançada de Ferramentas"/>
- **Etapa 8** — <Link to="etapa8" title="Integração de Ferramentas e APIs"/>
- **Etapa 9** — <Link to="etapa9" title="Memória e Persistência em Agentes"/>

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
class: flex flex-col
---

# Bibliografia do curso

<div class="grid grid-cols-3 gap-8 flex-1 items-center justify-items-center">
  <AssetImg src="book-hands-on-machine-learning.jpg" class="rounded-lg h-70" />
  <AssetImg src="book-machine-learning-foundations.jpg" class="rounded-lg h-70" />
  <AssetImg src="book-building-agents-with-openai-sdk.jpg" class="rounded-lg h-70" />
</div>

---
layout: two-cols-header
layoutClass: gap-8
class: flex items-center justify-center
---

# Bibliografia do curso

::left::

<div class="flex flex-col items-center gap-4">
  <teenyicons-doc-outline class="text-7xl text-cyan-400" />
  <a href="https://scikit-learn.org/stable/" target="_blank">scikit-learn.org/stable</a>
</div>

::right::

<div class="flex flex-col items-center gap-4">
  <teenyicons-doc-outline class="text-7xl text-cyan-400" />
  <a href="https://openai.github.io/openai-agents-python/" target="_blank">openai.github.io/openai-agents-python</a>
</div>

---
src: ./pages/predictive-modeling/slide-etapa1.md
---

---
src: ./pages/predictive-modeling/slide-etapa2.md
---

---
src: ./pages/predictive-modeling/slide-etapa3.md
---

---
src: ./pages/predictive-modeling/slide-etapa4.md
---

---
src: ./pages/predictive-modeling/slide-etapa5.md
---

---
src: ./pages/predictive-modeling/slide-etapa6.md
---

---
src: ./pages/predictive-modeling/slide-etapa7.md
---

---
src: ./pages/predictive-modeling/slide-etapa8.md
---

---
src: ./pages/predictive-modeling/slide-etapa9.md
---
