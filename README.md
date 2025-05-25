VERSÃO DO PYTHON DO PROJETO: 3.12

PASSO A PASSO INICIAR VENV:

cd code
ls
== setup  venv  venv_bkp

inicie o venv
source venv/bin/activate

cd setup
ls
== apps  manage.py  requirements.txt  setup  templates

- Instale as dependencias:
pip install -r requirements.txt

-Iniciar projeto:
python3.12 manage.py runserver


PASSO A PASSO CONFIGURAR POSTGRES:

- Instale o postgres:

sudo apt install postgresql-15

- Logue como postgres para acessar o console:

sudo -u postgres psql

- Defina a senha do usuário postgres:


ALTER USER postgres WITH PASSWORD 'abc123';
obs: Use essa senha, pois está configurada em ./code/setup/setup/settings.py

- Crie o banco de dados 'pousada':
CREATE DATABASE pousada;

- Rode as migrates:
(Inicie o venv)

python3.12 manage.py migrate

