web: cd TwojKomputerowiec && export FLASK_APP=twojKomputerowiec.py && rm TwojKomputerowiec/strona.db && flask db init && flask db migrate && flask db upgrade && python3 testyModeli.py && python3 testyRestApi.py && gunicorn TwojKomputerowiec:app