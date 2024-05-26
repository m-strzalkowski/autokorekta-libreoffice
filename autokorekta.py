#Właściwa logika autokorekty ogonków, dostępna z:
# 1. test_autokorekta.py, jako program terminalowy
# 2. autokor.py - ze środowika makr libreoffice

###### Ten kawałek zmieniany jest przy kopiowaniu poprzez skrypt deploy.py #######
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
PRZERZUCONE=False
##################################################################################
ILECZĘŚCI = 4096 # Na ile plików będzie podzielony każdy zapisywany/czytany z dysku słownik
def ile_części():
    return ILECZĘŚCI

import sys
sys.path.append(KATALOG_SKRYPTOW)
from autokor_wspolne import log, timeit

import os, glob, re
from pokawałkowane_słowniki import PokawałkowanySłownikDoOdczytu

ogonki =     {
        'ą':'a',
        'ć':'c',
        'ę':'e',
        'ł':'l',
        'ń':'n',
        'ó':'o',
        'ś':'s',
        'ż':'z',
        'ź':'z'
    }
#from unidecode import unidecode
def unidecode(s):#zamiast importu prosta funkcja - ie chcemy bawić się w instalowanie pipa we wbudwanym pythonie libreoffice'a albo niezgodność wersji, gdyby dać mu moduły systemowe
    return "".join(map(lambda c: ogonki[c.lower()] if c.lower() in ogonki else c.lower(), s))
def normalizuj(słowo):
    return unidecode(słowo).lower()

#deklaracja dwóch głównych słowników
_słowa = None # ma zawierać wszystkie słowa ze słownika jako klucze (wartości = None)
_gołe = None # opisuje relację: słowo_bez_ogonków -> [słowa z ogonkami]
_slownik_zaladowany = False

#Ładuje słowniki
@timeit
def załaduj():
    global _słowa, _gołe, _slownik_zaladowany
    with open(os.path.join(KATALOG_ORYGINALNY, 'słownik.pickle'), 'rb') as f:
        #_słowa, _gołe = pickle.load(f)
        _słowa = PokawałkowanySłownikDoOdczytu(os.path.join(KATALOG_ORYGINALNY, "słownik_skompilowany","słowa"))
        _gołe = PokawałkowanySłownikDoOdczytu(os.path.join(KATALOG_ORYGINALNY, "słownik_skompilowany","gołe"))
        _slownik_zaladowany = True

def słownik_załadowany(f):
    def wrapper(*args, **kwargs):
        if not _slownik_zaladowany:
            log("SLOWNIK NIE ZAŁADOWANY")
            raise RuntimeError("SŁOWNIK NIE ZAŁADOWANY")
        return f(*args, **kwargs)
    return wrapper

def zachowaj_wiekość_liter(stare, nowe):
    if len(stare)!= len(nowe):
        return nowe
    return "".join([n.upper() if s.isupper() else n.lower() for s,n in zip(stare, nowe)])

SŁOWNIKOWY = 'SŁOWNIKOWY'
NIEPOPRAWIALNY ="NIEPOPRAWIALNY"
POPRAWIONY = "POPRAWIONY"
POPRAWIONY_HEURYSTYCZNIE ="POPRAWIONY_HEURYSTYCZNIE"

#Główne wywołanie, tylko musi mieć za arument słowo obrane ze spacji, przecinków itd.
@słownik_załadowany
def korekta(słowo):
    log("korekta(",słowo,")")
    if słowo in _słowa:
        return słowo, SŁOWNIKOWY
    bezogonków = normalizuj(słowo)
    log("bezogonków:", bezogonków)
    if bezogonków not in _gołe:
        return słowo, NIEPOPRAWIALNY
    możliwości = _gołe[bezogonków]
    log("możliwości:",  możliwości)
    if len(możliwości)>1:
        return zachowaj_wiekość_liter(słowo, możliwości[-1]), POPRAWIONY_HEURYSTYCZNIE
    return zachowaj_wiekość_liter(słowo, możliwości[0]), POPRAWIONY

p = re.compile(r'\b[^\W\d_]+\b')
def korekta_t(tekst):
    w = []
    for match in p.finditer(tekst):
        w.append([*korekta(match.group(0)), match.span()])
    return w
#Korekta ostatniego słowa w tekście
def korekta_ost(tekst):
    matches = [match for match in p.finditer(tekst)]
    if len(matches)<1:
        return None
    else:
        match = matches[-1]#ostatnie słowo, czyli najbliżej kursora
        return [*korekta(match.group(0)), match.span()]