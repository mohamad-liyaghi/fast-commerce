echo 'Running Migrations'
alembic upgrade head



echo 'Running Server'
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
  fastapi run src/main.py
else
  fastapi dev src/main.py
fi