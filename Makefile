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
