from abc import ABC, abstractmethod
from datetime import date, timedelta
from decimal import Decimal


class Adres:
    def __init__(self, ulica, miasto, kod_pocztowy):
        self.ulica = ulica
        self.miasto = miasto
        self.kod_pocztowy = kod_pocztowy

    def __str__(self):
        return f"{self.ulica}, {self.kod_pocztowy} {self.miasto}"


class Produkt(ABC):
    def __init__(self, sku, nazwa, cena_netto, stan_poczatkowy=0):
        if not sku:
            raise ValueError("SKU jest wymagane.")
        if not nazwa:
            raise ValueError("Nazwa jest wymagana.")
        cena_netto = Decimal(str(cena_netto))
        if cena_netto <= 0:
            raise ValueError("Cena netto musi byc dodatnia.")
        if stan_poczatkowy < 0:
            raise ValueError("Stan poczatkowy nie moze byc ujemny.")
        self._sku = sku
        self._nazwa = nazwa
        self._cena_netto = cena_netto
        self._stan = stan_poczatkowy

    @property
    def sku(self):
        return self._sku

    @property
    def nazwa(self):
        return self._nazwa

    @property
    def stan(self):
        return self._stan

    @property
    def cena_netto(self):
        return self._cena_netto

    @cena_netto.setter
    def cena_netto(self, wartosc):
        wartosc = Decimal(str(wartosc))
        if wartosc <= 0:
            raise ValueError("Cena netto musi byc dodatnia.")
        self._cena_netto = wartosc

    def przyjmij(self, ilosc):
        if ilosc <= 0:
            raise ValueError("Ilosc przyjecia musi byc dodatnia.")
        self._stan += ilosc

    def wydaj(self, ilosc):
        if ilosc <= 0:
            raise ValueError("Ilosc wydania musi byc dodatnia.")
        if ilosc > self._stan:
            raise ValueError(
                f"Brak wystarczajacego stanu ({self._stan}) dla {self._sku}. Nie można wydać ({ilosc}) sztuk"
            )
        self._stan -= ilosc

    def wartosc_stanu(self):
        return self._cena_netto * self._stan

    @abstractmethod
    def kategoria(self):
        ...

    @abstractmethod
    def warunki_przechowywania(self):
        ...

    def etykieta(self):
        return f"[{self.kategoria()}] {self._sku} - {self._nazwa} (stan: {self._stan})"


class ProduktSpozywczy(Produkt):
    def __init__(self, sku, nazwa, cena_netto, data_waznosci, stan_poczatkowy=0):
        super().__init__(sku, nazwa, cena_netto, stan_poczatkowy)
        self._data_waznosci = data_waznosci

    @property
    def data_waznosci(self):
        return self._data_waznosci

    def czy_przeterminowany(self, dzien=None):
        dzien = dzien or date.today()
        return dzien > self._data_waznosci

    def dni_do_waznosci(self, dzien=None):
        dzien = dzien or date.today()
        return (self._data_waznosci - dzien).days

    def kategoria(self):
        return "Spozywczy"

    def warunki_przechowywania(self):
        return "Chlodnia 2-6 C, rotacja FEFO wedlug daty waznosci."


class ProduktElektroniczny(Produkt):
    def __init__(self, sku, nazwa, cena_netto, gwarancja_miesiace, stan_poczatkowy=0):
        super().__init__(sku, nazwa, cena_netto, stan_poczatkowy)
        if gwarancja_miesiace < 0:
            raise ValueError("Gwarancja nie moze byc ujemna.")
        self._gwarancja_miesiace = gwarancja_miesiace

    @property
    def gwarancja_miesiace(self):
        return self._gwarancja_miesiace

    def kategoria(self):
        return "Elektronika"

    def warunki_przechowywania(self):
        return "Magazyn suchy, ochrona ESD, wilgotnosc < 60%."


class ProduktChemiczny(Produkt):
    def __init__(self, sku, nazwa, cena_netto, klasa_adr, stan_poczatkowy=0):
        super().__init__(sku, nazwa, cena_netto, stan_poczatkowy)
        self._klasa_adr = klasa_adr

    @property
    def klasa_adr(self):
        return self._klasa_adr

    def kategoria(self):
        return "Chemia"

    def warunki_przechowywania(self):
        return f"Strefa ADR (klasa {self._klasa_adr}), wentylacja, z dala od zywnosci."


class Dostawca:
    def __init__(self, id_dostawcy, nazwa, adres):
        self._id = id_dostawcy
        self._nazwa = nazwa
        self._adres = adres

    @property
    def id(self):
        return self._id

    @property
    def nazwa(self):
        return self._nazwa

    @property
    def adres(self):
        return self._adres


class PozycjaDostawy:
    def __init__(self, produkt, ilosc, cena_jednostkowa):
        if ilosc <= 0:
            raise ValueError("Ilosc w pozycji musi byc dodatnia.")
        cena_jednostkowa = Decimal(str(cena_jednostkowa))
        if cena_jednostkowa <= 0:
            raise ValueError("Cena jednostkowa musi byc dodatnia.")
        self._produkt = produkt
        self._ilosc = ilosc
        self._cena_jednostkowa = cena_jednostkowa

    @property
    def produkt(self):
        return self._produkt

    @property
    def ilosc(self):
        return self._ilosc

    def wartosc(self):
        return self._cena_jednostkowa * self._ilosc


class Dostawa:
    def __init__(self, id_dostawy, dostawca, data_przyjecia=None):
        self._id = id_dostawy
        self._dostawca = dostawca
        self._data = data_przyjecia or date.today()
        self._pozycje = []

    @property
    def id(self):
        return self._id

    @property
    def dostawca(self):
        return self._dostawca

    @property
    def pozycje(self):
        return tuple(self._pozycje)

    def dodaj_pozycje(self, produkt, ilosc, cena_jednostkowa):
        self._pozycje.append(PozycjaDostawy(produkt, ilosc, cena_jednostkowa))

    def wartosc_calkowita(self):
        return sum((p.wartosc() for p in self._pozycje), Decimal("0"))


class MetodaWyceny(ABC):
    @abstractmethod
    def wycen(self, produkty):
        ...

    @abstractmethod
    def nazwa(self):
        ...


class WycenaWgKosztu(MetodaWyceny):
    def wycen(self, produkty):
        return sum((p.wartosc_stanu() for p in produkty), Decimal("0"))

    def nazwa(self):
        return "Wycena wg ceny zakupu"


class WycenaDetaliczna(MetodaWyceny):
    def __init__(self, marza=Decimal("1.23")):
        self._marza = Decimal(str(marza))

    def wycen(self, produkty):
        return sum((p.wartosc_stanu() * self._marza for p in produkty), Decimal("0"))

    def nazwa(self):
        return "Wycena detaliczna (z marza)"


class Magazyn:
    def __init__(self, nazwa, adres):
        self._nazwa = nazwa
        self._adres = adres
        self._produkty = {}

    @property
    def nazwa(self):
        return self._nazwa

    @property
    def adres(self):
        return self._adres

    def zarejestruj_produkt(self, produkt):
        if produkt.sku in self._produkty:
            raise ValueError(f"Produkt o SKU {produkt.sku} juz istnieje.")
        self._produkty[produkt.sku] = produkt

    def produkt(self, sku):
        if sku not in self._produkty:
            raise KeyError(f"Brak produktu o SKU {sku}.")
        return self._produkty[sku]

    def przyjmij_dostawe(self, dostawa):
        for pozycja in dostawa.pozycje:
            self.produkt(pozycja.produkt.sku).przyjmij(pozycja.ilosc)

    def wydaj_produkt(self, sku, ilosc):
        self.produkt(sku).wydaj(ilosc)

    def wszystkie_produkty(self):
        return tuple(self._produkty.values())

    def produkty_zagrozone(self, prog_dni=7, dzien=None):
        dzien = dzien or date.today()
        wynik = []
        for p in self._produkty.values():
            if isinstance(p, ProduktSpozywczy) and p.dni_do_waznosci(dzien) <= prog_dni:
                wynik.append(p)
        return wynik

    def wartosc_magazynu(self, metoda):
        return metoda.wycen(self._produkty.values())


def demo():
    magazyn = Magazyn("Magazyn Centralny", Adres("Hutnicza 12", "Piekary Slaskie", "41-940"))

    mleko = ProduktSpozywczy("SPZ-001", "Mleko 2%", "3.20", date.today() + timedelta(days=4))
    laptop = ProduktElektroniczny("ELE-100", "Laptop 14 cali", "3200.00", 24)
    rozpuszczalnik = ProduktChemiczny("CHM-050", "Rozpuszczalnik", "18.50", "3")

    for p in (mleko, laptop, rozpuszczalnik):
        magazyn.zarejestruj_produkt(p)

    dostawca = Dostawca("DST-7", "Hurtownia Slask", Adres("Magazynowa 4", "Katowice", "40-001"))
    dostawa = Dostawa("DOS-2026-001", dostawca)
    dostawa.dodaj_pozycje(mleko, 200, "2.40")
    dostawa.dodaj_pozycje(laptop, 15, "2700.00")
    dostawa.dodaj_pozycje(rozpuszczalnik, 40, "12.00")

    print(f"Magazyn: {magazyn.nazwa} ({magazyn.adres})")
    print(f"Dostawa {dostawa.id} od {dostawca.nazwa}, wartosc: {dostawa.wartosc_calkowita()} zl")

    magazyn.przyjmij_dostawe(dostawa)
    print("\nStan po przyjeciu dostawy:")
    for p in magazyn.wszystkie_produkty():
        print("  " + p.etykieta())

    magazyn.wydaj_produkt("ELE-100", 3)
    magazyn.wydaj_produkt("SPZ-001", 50)
    print("\nStan po wydaniu towaru:")
    for p in magazyn.wszystkie_produkty():
        print("  " + p.etykieta())

    print("\nWarunki przechowywania (polimorfizm):")
    for p in magazyn.wszystkie_produkty():
        print(f"  {p.sku}: {p.warunki_przechowywania()}")

    print("\nProdukty zagrozone (krotka data waznosci):")
    for p in magazyn.produkty_zagrozone(prog_dni=7):
        print(f"  {p.sku} - {p.nazwa}, dni do waznosci: {p.dni_do_waznosci()}")

    print("\nWycena magazynu (ten sam interfejs, rozne strategie):")
    for metoda in (WycenaWgKosztu(), WycenaDetaliczna()):
        print(f"  {metoda.nazwa()}: {metoda.wycen(magazyn.wszystkie_produkty()):.2f} zl")

    print("\nKontrola enkapsulacji:")
    try:
        liczba=99
        magazyn.wydaj_produkt("ELE-100", liczba)
    except ValueError as e:
        print(f"  Odrzucono niedozwolona operacje: {e}")


if __name__ == "__main__":
    demo()
