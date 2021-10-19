import requests

serverURL = 'https://www.twojkomputerowiec.bydgoszcz.pl'
serverMethods = {1:'/autor', 2:'/email'}
jsonPostEmail = {'kontakt':'mieciu@gmail.com', 'temat':'przykladowy temat', 'tresc':'przykladowa tresc'}

resp = requests.get(serverURL + serverMethods[1])
print([resp.status_code, resp.text])
print("#######################")

resp = requests.get(serverURL + serverMethods[2])
print([resp.status_code, resp.text])
print("#######################")

resp = requests.post(serverURL + serverMethods[2], json={})
print([resp.status_code, resp.text])
print("#######################")

resp = requests.post(serverURL + serverMethods[2], json=jsonPostEmail)
print([resp.status_code, resp.text])
print("#######################")