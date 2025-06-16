# Projeto Pousada

## Versão do Python

- **3.12**

---

## Passo a passo para iniciar o ambiente virtual (venv)

```bash
cd code
ls
setup  venv  venv_bkp
```
# Ative o ambiente virtual
```bash
source venv/bin/activate

cd setup
ls
apps  manage.py  requirements.txt  setup  templates
```
# Instale as dependências
```bash
pip install -r requirements.txt
```
# Inicie o projeto
```bash
python3.12 manage.py runserver
```

## PASSO A PASSO CONFIGURAR POSTGRES:

# Instale o postgres:
```bash
sudo apt install postgresql-15
```
# Logue como postgres para acessar o console:
```bash
sudo -u postgres psql
```
# Defina a senha do usuário postgres:
```bash
ALTER USER postgres WITH PASSWORD 'abc123';
obs: Use essa senha, pois está configurada em ./code/setup/setup/settings.py
```
# Crie o banco de dados 'pousada':
```bash
CREATE DATABASE pousada;
```
# Rode as migrates:
(Inicie o venv)
```bash
python3.12 manage.py migrate
```

## TailwindCSS e DaisyUI

# Tailwind e Daisy devem ser compilados para cada classe css nova que for usada. 
Quando estiverem rodando o projeto, deixem rodando tambem o seguinte comando:
```bash
cd code/setup
npx @tailwindcss/cli -i ./public/stylesheets/input.css -o ./public/stylesheets/output.css
```
# Links documentações:

# Tailwind 4.1:
https://tailwindcss.com/docs/styling-with-utility-classes

# DaisyUI 5.0.38:
https://daisyui.com/docs/use/

