dev:
	gunicorn main:app -w 4 -b 0.0.0.0:5000 --reload

deploy:
	git push heroku deploy:master

db_init:
	python -m db_api.db_init

test:
	python -m security.tests.client

