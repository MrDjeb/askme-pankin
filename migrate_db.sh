source venv/bin/activate &&
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete &&
find . -path "*/migrations/*.pyc" -delete &&
rm db.sqlite3 &&
python3 manage.py makemigrations &&
python3 manage.py migrate &&
python3 manage.py migrate --run-syncdb &&
python3 manage.py fill_db 20 &&
python3 manage.py runserver