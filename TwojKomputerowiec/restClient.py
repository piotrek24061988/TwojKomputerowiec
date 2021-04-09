import requests
from TwojKomputerowiec.konfiguracja import Konfiguracja

serverURL = Konfiguracja.SERVER_URL
serverMethods = {1:'/autor', 2:'/email'}
jsonPostEmail = {'kontakt':'mieciu@gmail.com', 'temat':'przykladowy temat', 'tresc':'przykladowa tresc'}

resp = requests.get(serverURL + serverMethods[1])
print([resp.status_code, resp.text])

resp = requests.get(serverURL + serverMethods[2])
print([resp.status_code, resp.text])

resp = requests.post(serverURL + serverMethods[2], json={})
print([resp.status_code, resp.text])

resp = requests.post(serverURL + serverMethods[2], json=jsonPostEmail)
print([resp.status_code, resp.text])