echo 'Running Migrations'
alembic upgrade head

echo 'Running Server'
fastapi dev src/main.py