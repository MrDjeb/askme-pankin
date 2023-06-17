# askme-pankin

----
>python3 --version

>>Python 3.10.6
----
>sudo apt install python3.10-venv

>python3 -m venv venv __#создать виртуальное окружение__

>source venv/bin/activate __#активировать работу в venv__

>deactivate __#выйти из акружения__
----
>pip3 freeze > requirements.txt __#cоздать файл с зависимостями__

>pip3 install -r requirements.txt __#скачать зависимости__
----
>pip3 install Django

>python3 -m django --version

>>4.2
----
>django-admin startproject askme_pankin __#создать Django проект (перенести в него всё)__
----
>python3 manage.py runserver __#запустить сервер__

>python3 manage.py startapp askme __#cоздать Django  приложение__

----


find . -path "*/migrations/*.py" -not -name "__init__.py" -delete &&
find . -path "*/migrations/*.pyc" -delete &&
rm db.sqlite3 &&
python3 manage.py makemigrations &&
python3 manage.py migrate &&
python3 manage.py migrate --run-syncdb &&
python3 manage.py fill_db 20 &&
python3 manage.py runserver

