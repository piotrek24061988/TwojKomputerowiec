import unittest, string, random
from TwojKomputerowiec import app, db, bcrypt
from TwojKomputerowiec.modele import Uzytkownik, Post, Aktualnosc


class TestyModeliUzytkownika(unittest.TestCase):
    def testLosowyUzytkownik(self):
        # Setup
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(20))
        hashHaslo = bcrypt.generate_password_hash(nazwa)
        # Run
        uzytkownik = Uzytkownik(email=nazwa + '@gmail.com', haslo=hashHaslo)
        db.session.add(uzytkownik)
        db.session.commit()
        # Check
        uzytkownikDoTestu = Uzytkownik.query.filter_by(email=nazwa + '@gmail.com').first()
        self.assertNotEqual(uzytkownikDoTestu, None)
        self.assertEqual(uzytkownikDoTestu.email, nazwa + '@gmail.com')

    def testLosowyPostBlogowy(self):
        # Setup
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(20))
        hashHaslo = bcrypt.generate_password_hash(nazwa)
        uzytkownik = Uzytkownik(email=nazwa + '@gmail.com', haslo=hashHaslo)
        tytul = ''.join(random.choice(string.ascii_letters) for i in range(10))
        tresc = ''.join(random.choice(string.ascii_letters) for i in range(50))
        # Run
        post = Post(tytul=tytul, tresc=tresc, autor=uzytkownik)
        db.session.add(post)
        db.session.commit()
        # Check
        postDoTestu = Post.query.filter_by(autor=uzytkownik).first()
        self.assertNotEqual(postDoTestu, None)

    def testAktualnosc(self):
        # Setup
        tytul = "Strona w budowie"
        tresc = "Rozpoczeła się budowa mojej strony internetowej."
        zdjecie = "web.jpg"
        videoUrl = "https://www.youtube.com/embed/1M0YXFW31hg"
        # Run
        aktualnosc = Aktualnosc(tytul=tytul, tresc=tresc, zdjecie=zdjecie, videoUrl=videoUrl)
        db.session.add(aktualnosc)
        db.session.commit()
        # Check
        aktualnoscDoTestu = aktualnosc.query.filter_by(tytul=tytul).first()
        self.assertEqual(aktualnoscDoTestu.tresc, tresc)
        self.assertNotEqual(aktualnoscDoTestu, None)


if __name__ == "__main__":
     unittest.main()