#### INSTALLATION:

mkdir promo_gen
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pre-commit install

### USAGE:

source env/bin/activate
python manage.py generate_codes --amount=5 --group='avtostop'
(optional --filename argument is supported. Default value is 'codes.json')

python manage.py check_code MY_CODE
(optional --filename argument is supported. Default value is 'codes.json')
