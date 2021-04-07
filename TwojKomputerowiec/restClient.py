import requests
serverURL = 'http://piotrek24061988.pythonanywhere.com'
serverMethod1 = '/autor'
serverMethod2 = '/email'
jsonPostMethod2 = {'kontakt':'mieciu@gmail.com',
                   'temat':'przykladowy temat',
                   'tresc':'przykladowa tresc'}

resp = requests.get(serverURL + serverMethod1)
print(resp.status_code)
print(resp.text)

resp = requests.get(serverURL + serverMethod2)
print(resp.status_code)
print(resp.text)

resp = requests.post(serverURL + serverMethod2, json={})
print(resp.status_code)
print(resp.text)

resp = requests.post(serverURL + serverMethod2, json=jsonPostMethod2)
print(resp.status_code)
print(resp.text)
