import requests

serverURL = 'http://piotrek24061988.pythonanywhere.com'
serverMethods = {1:'/autor', 2:'/email'}
jsonPostMethod2 = {'kontakt':'mieciu@gmail.com', 'temat':'przykladowy temat', 'tresc':'przykladowa tresc'}

resp = requests.get(serverURL + serverMethods[1])
print([resp.status_code, resp.text])

resp = requests.get(serverURL + serverMethods[2])
print([resp.status_code, resp.text])

resp = requests.post(serverURL + serverMethods[2], json={})
print([resp.status_code, resp.text])

resp = requests.post(serverURL + serverMethods[2], json=jsonPostMethod2)
print([resp.status_code, resp.text])