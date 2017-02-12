test:
	python manage.py makemigrations css && python manage.py migrate && python manage.py test --no-input tests

%:
	python manage.py test --no-input tests.$@

