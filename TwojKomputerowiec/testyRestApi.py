import unittest, requests
from TwojKomputerowiec.konfiguracja import Konfiguracja

serverURL = Konfiguracja.SERVER_URL


class TestyRestApi(unittest.TestCase):
    def testGetAutor(self):
        # Setup
        metoda = '/autor'
        # Run
        resp = requests.get(serverURL + metoda)
        # Check
        self.assertEqual(resp.status_code, 200)

    def testGetEmail(self):
        # Setup
        metoda = '/email'
        # Run
        resp = requests.get(serverURL + metoda)
        # Check
        self.assertEqual(resp.status_code, 200)

    def testPostWrongEmail(self):
        # Setup
        metoda = '/email'
        # Run
        resp = requests.post(serverURL + metoda, json={})
        # Check
        self.assertEqual(resp.status_code, 401)

    def testPostValidEmail(self):
        # Setup
        metoda = '/email'
        jsonPostEmail = {'kontakt':'mieciu@gmail.com', 'temat':'przykladowy temat', 'tresc':'przykladowa tresc'}
        # Run
        resp = requests.post(serverURL + metoda, json=jsonPostEmail)
        # Check
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()