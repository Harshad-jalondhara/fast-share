python3 -m venv .venv

source venv/bin/activate

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-multipart pydantic

pip install alembic

pip freeze > requirements.txt


uvicorn app.main:app --reload
--------

my work 
database
models
main.py
schemas
uitls.py
