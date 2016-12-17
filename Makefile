dev:
	gunicorn main:app -w 4 -b 0.0.0.0:5000 --reload

deploy:
	git push heroku deploy:master

test:
	python -m security.tests.client

