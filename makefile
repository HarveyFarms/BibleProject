main:
	python manage.py runserver
mi migrate:
	python manage.py migrate ;
reset:
	mysql --user=root --password=root --table < main.sql ;
	python manage.py runserver
db:
	mysql --user=root --password=root --table < main.sql ;
rm resetmigrate:
	mysql --user=root --password=root --table < main.sql ;
	python manage.py runserver
o r:
	open http://localhost:8000
m:
	nvim makefile
