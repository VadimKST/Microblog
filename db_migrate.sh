echo -n "Enter migration message: "
read message
alembic revision --autogenerate -m "$message"
alembic upgrade head