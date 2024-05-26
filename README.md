# autokorekta-libreoffice
 ### **Dokłada zgubione ogonki podczas pisania**

Próbuje dokładać ogonki do ostatniego wpisanego słowa, za każdym naciśnięciem spacji.
Używa słownika który trzeba wpierw wygenerować.

0%  BASICa, wszystko w Pythonie!
## Instrukcja instalacji
1. `python przygotuj_słownik.py` -> genreuje właściwą postać słownika
2. `python deploy.py` -> instaluje skrypty w katalogu właściwym dla makr użytkownika w Libre Office 4
3. Przypiąć funkcję autokoor.AUTOKOR_USTAW_SPACJOLAPA do jakiejś kombinacji klawiszy lub do zdarzenia ładowania dokumentu
4. Logi gromadzą się w log.txt: 
    * pod Windowsem w powershellu można: `Get-Content -Path log.txt -Wait -Tail 10 -Encoding utf8`
*  `test_autokorekta.py` woła mechanizm autokorekty bez libreoffice'a - z terminala

Mateusz Strzałkowski, 2024
z tym, że:

Zawartość katalogu słownik_podzielony pierwotnie była jednym plikiem, sciągniętym z http://morfeusz.sgjp.pl/download/ i opatrzoną notką zachowaną w sgjp.license, stwierdzającą, że ów słownik jest dziełem panów: Wolińskiego, Bronka, Gruszczyńskiego, Kierasia, Saloniego, Wołosza i pani Skowrońskiej.
