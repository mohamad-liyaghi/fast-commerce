echo 'Running Migrations'
alembic upgrade head

echo 'Running Server'
python src/main.py