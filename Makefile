SHELL := /bin/bash

manage_py := python app/manage.py

runserver:
	$(manage_py) runserver 0:8000

migrate:
	$(manage_py) migrate

makemigrations:
	$(manage_py) makemigrations

shell:
	$(manage_py) shell_plus --print-sql

show_urls:
	$(manage_py) show_urls

createsuperuser:
	$(manage_py) createsuperuser

worker:
	cd app && celery -A settings worker -l info --autoscale=10,0
	#cd app && celery -A settings worker -l info --concurrency 20

beat:
	cd app && celery -A settings beat -l info