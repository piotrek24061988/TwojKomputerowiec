import unittest, string, random
from TwojKomputerowiec import db, bcrypt
from TwojKomputerowiec.modele import *


class TestyModeliUzytkownika(unittest.TestCase):
    def testLosowyUzytkownik(self):
        # Setup
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(10))
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
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(10))
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
        aktualnoscDoTestu = Aktualnosc.query.filter_by(tytul=tytul).first()
        self.assertEqual(aktualnoscDoTestu.tresc, tresc)
        self.assertNotEqual(aktualnoscDoTestu, None)

    def testGalerii(self):
        # Setup
        tytul = "Testowe zdjęcie do galerii"
        zdjecie = "Bydgoszcz.jpg"
        # Run
        zdjecie = Galeria(tytul=tytul, zdjecie=zdjecie)
        db.session.add(zdjecie)
        db.session.commit()
        # Check
        zdjecieDoTestu = Galeria.query.filter_by(tytul=tytul).first()
        self.assertEqual(zdjecieDoTestu.tytul, tytul)
        self.assertNotEqual(zdjecieDoTestu, None)

    def testProduktu(self):
        # Setup
        tytul = "Testowy produkt 1"
        tresc = "To jest pierwszy i testowy produkt do sklepu"
        zdjecie = "placeholder.png"
        # Run
        produkt = Produkt(tytul=tytul, tresc=tresc, zdjecie=zdjecie, ilosc=99, cena=23.45, cyfrowy=False)
        db.session.add(produkt)
        db.session.commit()
        # Check
        produktDoTestu = Produkt.query.filter_by(tytul=tytul).first()
        self.assertEqual(produktDoTestu.tytul, tytul)
        self.assertNotEqual(produktDoTestu, None)

    def testZamowienia(self):
        # Setup
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(10))
        hashHaslo = bcrypt.generate_password_hash(nazwa)
        uzytkownik = Uzytkownik(email=nazwa + '@gmail.com', haslo=hashHaslo)
        platnosc = "przelew"
        # Run
        zamowienie = Zamowienie(autor=uzytkownik, ukonczone=False, platnosc=platnosc)
        db.session.add(zamowienie)
        db.session.commit()
        # Check
        zamowienieDoTestu = Zamowienie.query.filter_by(platnosc=platnosc).first()
        self.assertEqual(zamowienieDoTestu.platnosc, platnosc)
        self.assertNotEqual(zamowienieDoTestu, None)

    def testObiektuZamowienia(self):
        # Setup
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(10))
        hashHaslo = bcrypt.generate_password_hash(nazwa)
        uzytkownik = Uzytkownik(email=nazwa + '@gmail.com', haslo=hashHaslo)
        tytul = "Testowy produkt 2"
        tresc = "To jest drugi i testowy produkt do sklepu"
        tytul2= "Testowy produkt 3"
        tresc2 = "To jest trzeci i testowy produkt do sklepu"
        zdjecie = "placeholder.png"
        produkt = Produkt(tytul=tytul, tresc=tresc, zdjecie=zdjecie, ilosc=101, cena=34.56, cyfrowy=False)
        produkt2 = Produkt(tytul=tytul2, tresc=tresc2, zdjecie=zdjecie, ilosc=102, cena=65.43, cyfrowy=True)
        platnosc = "przelew"
        uwagi = "Proszę wysyłać jedynie w pełni skompletowane zamówienie"
        zamowienie = Zamowienie(autor=uzytkownik, ukonczone=False, platnosc=platnosc, uwagi=uwagi)
        ilosc = 2
        ilosc2 = 4
        # Run
        obiektZamowienia = ObiektZamowienia(produkt=produkt, zamowienie=zamowienie, ilosc=ilosc)
        obiektZamowienia2 = ObiektZamowienia(produkt=produkt2, zamowienie=zamowienie, ilosc=ilosc2)
        db.session.add(obiektZamowienia)
        db.session.add(obiektZamowienia2)
        db.session.commit()
        # Check
        obiektZamowienieDoTestu = ObiektZamowienia.query.filter_by(ilosc=ilosc).first()
        self.assertEqual(obiektZamowienieDoTestu.ilosc, ilosc)
        self.assertNotEqual(obiektZamowienia, None)

    def testAdresu(self):
        # Setup
        nazwa = ''.join(random.choice(string.ascii_letters) for i in range(10))
        hashHaslo = bcrypt.generate_password_hash(nazwa)
        uzytkownik = Uzytkownik(email=nazwa + '@gmail.com', haslo=hashHaslo)
        platnosc = "przelew"
        uwagi = "nie mam uwag"
        zamowienie = Zamowienie(autor=uzytkownik, ukonczone=False, platnosc=platnosc, uwagi=uwagi)
        adres = "Gdanska 1/1"
        miasto = "Bydgoszcz"
        kod = "85-001"
        numer = "123-45-67-89"
        # Run
        adresDostawy = AdresDostawy(autor=uzytkownik, zamowienie=zamowienie, adres=adres, miasto=miasto, kod=kod, numer=numer)
        db.session.add(adresDostawy)
        db.session.commit()
        # Check
        adresDostawyDoTestu = AdresDostawy.query.filter_by(adres=adres).first()
        self.assertEqual(adresDostawyDoTestu.adres, adres)
        self.assertNotEqual(adresDostawyDoTestu, None)


if __name__ == "__main__":
     unittest.main()