cd ../..
source ./venv/bin/activate
cd -
alembic revision --autogenerate -m "nomos"
alembic upgrade head
alembic current
