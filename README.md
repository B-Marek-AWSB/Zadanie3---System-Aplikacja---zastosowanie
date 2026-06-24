# 1. Temat aplikacji 
Aplikacja ukazuje prosty system zarządzania magazynem. Magazyn przechowuje różne rodzaje produktów (spożywcze, elektroniczne i chemiczne), z których każdy ma własny identyfikator (SKU), cenę oraz aktualny stan ilościowy.  
Towar trafia do magazynu poprzez dostawy od dostawców, każda dostawa składa się z pozycji wskazujących konkretny produkt, jego ilość i cenę zakupu. Magazyn pozwala przyjmować dostawy, wydawać towar, wskazywać produkty z krótką datą ważności oraz wyceniać cały stan magazynowy różnymi metodami.  
Pilnowana jest poprawności danych: nie można wydać więcej niż jest na stanie ani ustawić ujemnej ceny.  

# 2. Lista klas
Adres - Obiekt wartości opisujący lokalizację (ulica, miasto, kod pocztowy)  
Produkt - Abstrakcyjna - Wspólny kontrakt każdego towaru (SKU, nazwa, cena, stan oraz reguły przyjęcia i wydania)  
ProduktSpozywczy - Produkt z datą ważności, przechowuje informacje o terminie ważności oraz warunki przechowywania  
ProduktElektroniczny - Produkt z okresem gwarancji oraz warunkami przechowywania  
ProduktChemiczny - Produkt z klasą ADR oraz warunkami przechowywania  
Dostwaca - Reprezentuje dostawcę  
PozycjaDostawy - Jedna wartość na fakturze dostawczej  
Dostawa - Dokument przyjęcia dostawy i jego wartości  
IMetodaWyceny - Interfejsu - Dwie różne strategie liczenia wartości magazynu  
WycenaWgKosztu - Pierwsza strategia liczenia wartości magazynu według kosztu (stan x cena)  
WycenaDetaliczna - Druga strategia liczenia według potencjalnej sprzedaży (stan x cena x marża)  
Magazyn - Główny obiekt  

# 3. Opis relacji między klasami
Magazyn - Adres -> Kompozycja  
Dostawca - Adres -> Kompozycja  
Magazyn - Produkt -> Kolekcja (1:n)  
Dostawa - PozycjaDostawy -> Kompozycja oraz kolekcja  
Dostawa - Dostawca -> Agregacja  
PozycjaDostawy - Produkt -> Referencja  
Produkt - Spozywczy/Elektroniczny/Chemiczny -> Dziedziczenie  
IMetodaWyceny - WycenaWgKosztu/WycenaDetaliczna -> Interfejs  
Magazyn - IMetodaWyceny -> Parametr metody  
Magazyn - Dostawa -> Parametr metody  

# 4. Wskazanie czterech zasad OOP
Enkapsulacja -> W klasie Produkt, pola _cena_netto lub _stan  
Zmiana stanu tylko przez Przyjmij()/Wydaj(), które pilnują reguł.  
Dla ceny, wartości ujemne są odrzucane, nie da się ustawić tego stanu z zewnątrz.  

Dziedziczenie -> Produkt do ProduktSpozywczy/Eletroniczny/Chemiczny  
Podkategorie przejmują identyfikator SKU, cenę, stan, logikę magazynową oraz dokładają własne cechy takie jak - data ważności, gwarancja, klasa ADR.  

Polimorfizm -> Metody WarunkiPrzechowywania() i Kategoria()  
Pętla po produktach woła tę samą metodę na różnych typach i każdy zwraca inny wynik.  

Abstrakcja -> Produkt lub IMetodaWyceny  
Produkt definiuje, że każdy towar będzie umiał odpowiedzieć na metody Kategoria() oraz WarunkiPrzechowywania(), ale to konkretny typ decyduje o treści.  


AI zostało wykorzystane, przy wymyśleniu założeń magazynu oraz jego klas (oraz przy podpowiedzi jak zrobić nową linię w tym pliku).
