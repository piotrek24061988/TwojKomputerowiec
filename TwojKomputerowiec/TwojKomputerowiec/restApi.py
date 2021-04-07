from flask import request
from flask_restful import Resource
from TwojKomputerowiec import api
from TwojKomputerowiec.konfiguracja import Konfiguracja
from TwojKomputerowiec.przydatne import emailKontaktowy


class Autor(Resource):
    def get(self):
        return {
            'autor': 'Piotr Gorecki',
            'email': Konfiguracja.MAIL_USERNAME
        }


class EmailDoAutora(Resource):
    def post(self):
        json = request.get_json()
        kontakt = json.get('kontakt')
        temat = json.get('temat')
        tresc = json.get('tresc')
        if kontakt and temat and tresc:
            emailKontaktowy(kontakt=kontakt, temat=temat, tresc=tresc)
            return {'wyslales kompletny json': json}
        else:
            return {'wyslales niekompletny json': json, 'kontakt': kontakt, 'temat': temat, 'tresc': tresc}


api.add_resource(Autor, '/autor')
api.add_resource(EmailDoAutora, '/email')