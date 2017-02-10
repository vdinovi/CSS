test:
	python manage.py test --no-input tests

%:
	python manage.py test --no-input tests.$@

