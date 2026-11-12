---
layout: section
routeAlias: etapa1
---

## **Etapa 1:** Manipulação Básica de Dados

---
layout: section
---

## Instalação e configuração de **ambiente**

<!--

verificar como está o WSL na máquina windows - TODOS DEVEM USAR WSL

-->

---
layout: two-cols-header
layoutClass: gap-8
class: flex items-center justify-center
sourceLabel: WSL
source: https://learn.microsoft.com/windows/wsl/
---

# Windows Subsystem for Linux (WSL)

#### **Linux e mac oferecem ambientes de desenvolvimento rápidos e o WSL também**

::left::

<div class="text-left w-full [&_li]:mb-5">

- **Experência semelhante com linux/mac** — WSL usa shell bash para linha de comando.
- **Ambiente rápido e leve** — Sistema de arquivo baseado em linux rápido e leve.
- **Integração com o Windows** — arquivos, terminal e o editor (VS Code/Antigravity) acessam o WSL.

</div>

::right::

<div class="h-full flex items-center justify-center">
    <AssetImg src="wsl.jpg" class="w-full max-w-[440px] rounded-lg" />
</div>

<!--
# comandos WSL
wsl --version
wsl --update
wsl --status
wsl --install -d Ubuntu
wsl
wsl -l --running
wsl --help

# comando WSL para distro por aluno
# export
wsl --export ubuntu C:\LabWSL\ubuntu-base.tar

# import aluno1
wsl --import ubuntu-<nome-aluno> C:\LabWSL C:\LabWSL\ubuntu-base.tar
wsl -d <nome-aluno> -u root -e bash -c "useradd -m -G sudo -s /bin/bash <nome-aluno> && echo '<nome-aluno>:senha123' | chpasswd && echo -e '[user]\ndefault=<nome-aluno>' > /etc/wsl.conf"

# import aluno2
wsl --import ubuntu-<nome-aluno> C:\LabWSL C:\LabWSL\ubuntu-base.tar
wsl -d <nome-aluno> -u root -e bash -c "useradd -m -G sudo -s /bin/bash <nome-aluno> && echo '<nome-aluno>:123456' | chpasswd && echo -e '[user]\ndefault=<nome-aluno>' > /etc/wsl.conf"
-->

---
layout: two-cols-header
layoutClass: gap-8
class: flex items-center justify-center
---

# Antigravity IDE

#### **IDE da Google para desenvolvimento de software com agente de codificação**

::left::

<div class="text-left w-full">

Download e documentação em:
- [antigravity.google/download](https://antigravity.google/download#antigravity-ide)
- [antigravity.google/docs/ide/overview](https://antigravity.google/docs/ide/overview)

<br/>

<v-click at="+1">

> [!TIP]
> A Google decidiu dividir o produto Antigravity em dois: Antigravity 2.0 e Antigravity IDE. 

</v-click>

</div>

::right::

<Transform :scale="0.9" origin="center">
    <AssetImg
    src="ide-google-antigravity.png"
    class="rounded-lg"
    />
</Transform>

<!-- 

# criar pasta pelo antigravity e usar o terminal para instalar uv, init, python, etc

# verifique se o aluno tem acesso ao plano Pro gratuito para estudantes

- checar se todos tem o Antigravity instalado
- mostrar rapidamente o chatbot agentico
 -->

---
sourceLabel: Downloads
source: https://www.python.org/downloads/
---

# Versões do Python

#### **Use sempre versões estáveis (fase de bugfix)**



<Transform :scale="0.7" origin="center">
    <AssetImg
    src="release-cycle.svg"
    class="rounded-lg border-10 border-white"
    />
</Transform>


<!-- 
Python tem um ciclo de cinco fases com versão estável (bugfixes) a cada dois meses 

**Cinco fases**: 
- feature, 
- prerelease, 
- bugfix, 
- security, 
- end-of-life
-->

---
layout: default
sourceLabel: Install UV
source: https://docs.astral.sh/uv/getting-started/installation
---

# Instalação Python e UV

<br/>



#### **Instalação UV: uma opção rápida e simplificada para gerenciar projetos python**
<br/>


::code-group

```sh [macOS/linux]
curl -LsSf https://astral.sh/uv/install.sh | sh
```

::

<br/><br/>

#### **Instalação do Python em múltiplas plataformas**

<br/>

::code-group

```sh [cross plataform]
uv python install 3.14
```

```sh [macOS]
brew install python@3.14
```

::



---
layout: default
sourceLabel: Install UV
source: https://docs.astral.sh/uv/getting-started/installation
footer: true
---

# Gerenciador de projetos UV

#### **uv é um gerenciador de projetos ultrarrápido escrito em Rust pela Astral (OpenAI)**

<br/>

| | |  |
| --- | --- | --- |
| instalação python | `instalador oficial` | ```uv python install``` |
| versão python | `python --version` | ```uv run python --version``` |
| criar ambiente/projeto | `python -m venv .venv` | `uv init <projeto>` |
| ativar ambiente virtual | `.venv/Scripts/activate` | ``-`` *(automático)* |
| instalar pacote | `pip install <pacote>` | ```uv add <pacote>``` |
| executar script | `python script.py` | ```uv run script.py``` |


<!--
instalação:
https://docs.astral.sh/uv/getting-started/installation/

wsl: curl -LsSf https://astral.sh/uv/install.sh | sh

powershell: <br/>
```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

-->


---
layout: default
sourceLabel: Install UV
source: https://docs.astral.sh/uv/getting-started/installation
footer: true
---

# Mais sobre o gerenciador UV

#### **Mais rápido e mais simples**

<br/>

| | |  |
| --- | --- | --- |
| criar projeto | `-` *não tem* | ```uv init <projeto>``` |
| congelar pacotes | `pip freeze > requirements.txt` | `automático` *arquivo uv.lock* |
| arquivo do projeto | `requirements.txt` | ```pyproject.toml``` |
| recriar ambiente | `pip install -r requirements.txt` | `uv sync` |


<!-- 
usando forma tradicional para recriar ambiente:
pip install -r requirements.txt (só instala)

Usando UV para recriar ambiente respeitando o lock:
uv sync (instala, desinstala e atualiza) 
-->


---
layout: two-cols-header
layoutClass: gap-8
sourceLabel: Install UV
source: https://docs.astral.sh/uv/getting-started/installation
---

# Configuração do projeto Python

#### **Meu primeiro projeto de análise de dados**

<br/>

::left::

::code-group

```sh [uv]
mkdir my-first-eda
cd my-first-eda

uv python install 3.14
uv init --python 3.14
uv add pandas matplotlib seaborn scipy ipykernel

# abra um notebook .ipynb e selecione o kernel da .venv
```

```sh [pip]
mkdir my-first-eda
cd my-first-eda

python -m venv .venv
source .venv/bin/activate

pip install pandas matplotlib seaborn scipy ipykernel
pip freeze > requirements.txt

# abra um notebook .ipynb e selecione o kernel da .venv
```
::

::right::

> [!NOTE]
> O pacote **`ipykernel`** permite **executar notebooks Jupyter** (`.ipynb`) no editor usando o ambiente virtual (`.venv`) do projeto.


<!-- 
o comando abaixo substitui tres linhas de comandos:
```shell
uv init my-first-eda --python 3.14
```
```shell
mkdir my-first-eda
uv python install 3.14
uv init --python 3.14
```
-->

---

<!--
slide vazio — conteúdo da etapa 1
-->
