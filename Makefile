dev:
	gunicorn main:app -w 4 -b 0.0.0.0:5000 --reload

deploy:
	git push heroku deploy:master

db_init:
	python -m db_api.db_init

db_peek:
	python -m db_api.db_peek

db_mssql:
	python -m db_api.db_mssql_test

mssql_login:
	@ODBCSYSINI=./db_api isql **** **** ****

web_test:
	curl 'https://vast-lake-95491.herokuapp.com/nonce'

test:
	python -m security.tests.client

