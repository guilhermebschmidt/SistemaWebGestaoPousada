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
