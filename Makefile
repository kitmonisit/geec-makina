dev:
	gunicorn main:app -w 4 -b 0.0.0.0:5000 --reload

