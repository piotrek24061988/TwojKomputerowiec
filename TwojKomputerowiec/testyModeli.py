import unittest, string, random
from TwojKomputerowiec import app, db, bcrypt
from TwojKomputerowiec.modele import Uzytkownik, Post


class TestyModeliUzytkownika(unittest.TestCase):
    def testLosowyUzytkownik(self):
        # Setup
        self.uzytkownik = ''.join(random.choice(string.ascii_letters) for i in range(20))
        self.hashHaslo = bcrypt.generate_password_hash(self.uzytkownik)
        # Run
        uzytkownik = Uzytkownik(email=self.uzytkownik + '@gmail.com', haslo=self.hashHaslo)
        db.session.add(uzytkownik)
        db.session.commit()
        # Check
        uzytkownikDoTestu = Uzytkownik.query.filter_by(email=self.uzytkownik + '@gmail.com').first()
        self.assertNotEqual(uzytkownikDoTestu, None)
        self.assertEqual(uzytkownikDoTestu.email, self.uzytkownik + '@gmail.com')

    def testLosowyPostBlogowy(self):
        # Setup
        self.uzytkownik = Uzytkownik.query.order_by('id').first()
        self.tytul = ''.join(random.choice(string.ascii_letters) for i in range(10))
        self.tresc = ''.join(random.choice(string.ascii_letters) for i in range(50))
        # Run
        post = Post(tytul=self.tytul, tresc=self.tresc, autor=self.uzytkownik)
        db.session.add(post)
        db.session.commit()
        # Check
        postDoTestu = Post.query.filter_by(autor=self.uzytkownik).first()
        self.assertNotEqual(postDoTestu, None)


if __name__ == "__main__":
     unittest.main()