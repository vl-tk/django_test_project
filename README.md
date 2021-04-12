#### INSTALLATION:

1. git clone https://github.com/vl-tk/django_test_project.git
2. cd django_test_project
3. python -m venv env
4. source env/bin/activate
5. pip install -r requirements.txt

#### USAGE:

python manage.py generate_codes --amount=5 --group='avtostop'

python manage.py check_code MY_CODE

Result will be in the __django_test_project/codes_generator/results/codes.json__

```
Optional --filename argument is supported for both commands. Default value is 'codes.json'
```

#### RUNNING TESTS:

python manage.py test
