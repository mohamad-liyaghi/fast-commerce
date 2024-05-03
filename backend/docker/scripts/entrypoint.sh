echo 'Running Migrations'
alembic upgrade head

echo 'Running Server'
fastapi run src/main.py