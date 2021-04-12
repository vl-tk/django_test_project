#### INSTALLATION:

1. git clone https://github.com/vl-tk/django_test_project.git
2. python -m venv env
3. source env/bin/activate
4. pip install -r requirements.txt

#### USAGE:

python manage.py generate_codes --amount=5 --group='avtostop'

(optional --filename argument is supported. Default value is 'codes.json')

python manage.py check_code MY_CODE

(optional --filename argument is supported. Default value is 'codes.json')

#### RUNNING TESTS:

python manage.py test
