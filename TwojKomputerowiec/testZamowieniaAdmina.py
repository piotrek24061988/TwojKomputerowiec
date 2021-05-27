import unittest
from TwojKomputerowiec import db
from TwojKomputerowiec.modele import *
from TwojKomputerowiec.konfiguracja import Konfiguracja


class TestyModeliUzytkownika(unittest.TestCase):
    def testZamowieniaAdmina(self):
        # Setup
        #uzytkownik = Uzytkownik(email=nazwa + '@gmail.com', haslo=hashHaslo)
        uzytkownik = Uzytkownik.query.filter_by(email=Konfiguracja.MAIL_USERNAME).first()
        if uzytkownik:
            tytul = "Testowy produkt admina 1"
            tresc = "To jest pierwszy i testowy produkt admina do sklepu"
            tytul2= "Testowy produkt admina 2"
            tresc2 = "To jest drugi i testowy produkt admina do sklepu"
            zdjecie = "placeholder.png"
            produkt = Produkt(tytul=tytul, tresc=tresc, zdjecie=zdjecie, ilosc=1, cena=11.11, cyfrowy=False)
            produkt2 = Produkt(tytul=tytul2, tresc=tresc2, zdjecie=zdjecie, ilosc=2, cena=22.22, cyfrowy=True)
            platnosc = "pay pal"
            uwagi = "Testowe zamowienie administratora"
            zamowienie = Zamowienie(autor=uzytkownik, ukonczone=False, platnosc=platnosc, uwagi=uwagi)
            ilosc = 3
            ilosc2 = 5
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


if __name__ == "__main__":
     unittest.main()