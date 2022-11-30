install:
	poetry install

start:
	poetry run python manage.py runserver

makemig:
	poetry run python manage.py makemigrations

mig:
	poetry run python manage.py migrate

kill:
	sudo lsof -t -i tcp:8000 | xargs kill -9

shell:
	poetry run python manage.py shell_plus

lint:
	poetry run flake8 task_manager
	poetry run flake8 task_manager/labels
	poetry run flake8 task_manager/statuses
	poetry run flake8 task_manager/tasks
	poetry run flake8 task_manager/users

tests:
	poetry run python manage.py test

tests-cov:
	poetry run pytest --cov=task_manager --cov-report xml
