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

lint_tm:
	poetry run flake8 task_manager

lint_labels:
	poetry run flake8 labels

lint_statuses:
	poetry run flake8 statuses

lint_tasks:
	poetry run flake8 tasks

lint_users:
	poetry run flake8 users
