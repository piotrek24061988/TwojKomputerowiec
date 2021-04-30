import unittest
from TwojKomputerowiec import app


class TestyStron(unittest.TestCase):
    def setUp(self):
            self.test_app = app.test_client()

    def testStronaGlowna(self):
        # Run
        rv = self.test_app.get('/')
        # Check
        self.assertIn('200', str(rv))
        self.assertIn('serwis komputerowy', str(rv.data))


if __name__ == "__main__":
    unittest.main()