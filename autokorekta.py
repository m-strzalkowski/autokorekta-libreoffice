#deployment-dependent params
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
PRZERZUCONE=False
ILECZĘŚCI = 4096
def ile_części():
    return ILECZĘŚCI
POZ_PROT = 4#NAJWYŻSZY_OBSŁUGIWANY_PRZEZ_PYTHONA_LIBREOFFICOWEGO_PROTOKÓŁ_PIKLI
def poz_prot_pkl():
    return POZ_PROT

import sys, os
sys.path.append(KATALOG_SKRYPTOW)
from autokor_wspolne import log
import time
import datetime
from functools import wraps
#from autokor_wspolne import log
import os
import re
import hashlib
from hashlib import sha256
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000
        print("Function ", func.__name__, " took ",int(elapsed_time_ms)," milliseconds")
        #print(f"Function '{func.__name__}' took {elapsed_time_ms:.2f} milliseconds")
        return result
    return wrapper
# Example usage:
@timeit
def invoiceation():
    # Your function code here
    time.sleep(2)  # Simulating some work
def funkcja_haszująca(n:str):
    if not isinstance(n, str):
        raise Exception("Niestety klucz może byc tylko stringiem a nie "+ str(type(n)))
    return int.from_bytes(sha256(n.encode('utf-8')).digest(), 'big')
#Ze względu na potencjalną wielowątkowość
# def zrób_funkcję_haszującą():#->int
#     haszowacz = hashlib.sha256()
#     def funkcja_haszująca(n:str):
#         if not isinstance(n, str):
#             raise Exception("Niestety klucz może byc tylko stringiem a nie "+ str(type(n)))
#         haszowacz.update(n.encode('utf-8'))
#         return int.from_bytes(haszowacz.digest(), 'big')
#     return funkcja_haszująca

import pickle
import glob
def ścieżka_metadanych(katalog):
    return os.path.join(katalog, 'meta.pickle')
def ścieżka_części(katalog, numer_części):
    return os.path.join(katalog, str(numer_części)+".pickle")
A = 'sie'
def zapisz_pokawałkowany_słownik(słownik:dict, katalog, ileczęści:int, rób_katalog=False):
#    funkcja_haszująca = zrób_funkcję_haszującą()
    #print("słownik:", słownik)
    print("Zapis słownika w kawałkach (słownik <len=",len(słownik),">, ",katalog+", ",ileczęści,")")
    if rób_katalog:
        os.makedirs(katalog, mode=0o666, exist_ok=True)
    stare_pliki = glob.glob(os.path.join(katalog, "*"))
    for p in stare_pliki:
        print("Kasowanie starego:", p)
        os.remove(p)

    części = {}
    for i in range(ileczęści):
        części[i] = {}
    print("ilość części:", len(części))
    for k,w in słownik.items():
        cz = funkcja_haszująca(k)%ileczęści
        #print("części[",cz,"][",k,"] = ",w)
        części[cz][k] = w
    print("popisano po częściach")
    for i in range(ileczęści):
        with open(ścieżka_części(katalog, i), 'wb') as f:
            pickle.dump(części[i], f, poz_prot_pkl())
            print("zapisano część ", i)
    
    meta = {"typ":"pokawałkowany_słownik", "ilość_części":ile_części()}
    with open(ścieżka_metadanych(katalog), 'wb') as f:
        pickle.dump(meta, f, poz_prot_pkl())
    print("zapisano metadane:",meta)
    print("FH:",funkcja_haszująca(A)%ileczęści)


dbg = print
#dbg = lambda * args, **kwargs :None
class PokawałkowanySłownikDoOdczytu():
    katalog = None
    części = None
    ileczęści = 0
    def __init__(self, katalog):
        log("Inicjalizacja PokawałkowanegoSłownikaDoOdczytu z ", katalog)
#        self.funkcja_haszująca = zrób_funkcję_haszującą()
        self.katalog = katalog
        self.części = {}
        self.ileczęści = 0
        with open(ścieżka_metadanych(katalog), 'rb') as f:
            dbg("ścieżka metadanych:", ścieżka_metadanych(katalog))
            meta = pickle.load(f)
            log("Metadane:", meta)
            self.ileczęści = int(meta["ilość_części"])
            assert meta["typ"] == "pokawałkowany_słownik"
        #for i in range(ileczęści):
        #    części[i] = None# trzeba zaznaczyć, co załadowane, a co nie
        log("Koniec inicjalizacji PokawałkowanegoSłownikaDoOdczytu")
        dbg("FH:",funkcja_haszująca(A)%self.ileczęści)
    def num_załadowanej_części(self, klucz):# -> numer_części
        numer_części = funkcja_haszująca(klucz)%self.ileczęści
        if numer_części not in self.części:
            self.doładuj_część(numer_części)
        return numer_części
    def __getitem__(self, klucz):
        num_czesci = self.num_załadowanej_części(klucz)
        dbg("__getitem__", klucz,'-> cz.', num_czesci)
        return self.części[num_czesci][klucz]
    def __contains__(self, klucz):
        num_czesci = self.num_załadowanej_części(klucz)
        dbg("__contains__", klucz,'-> cz.', num_czesci)
        return klucz in self.części[num_czesci]
    @timeit
    def doładuj_część(self, numer_części):
        log("doładuj_część ", numer_części, " - start")
        with open(ścieżka_części(self.katalog, numer_części), 'rb') as f:
            część = pickle.load(f)
            self.części[numer_części] = część
            log("doładowano ", len(część), "elementów")
            log("Stan PokawałkowanegoSłownikaDoOdczytu: ", len(self.części), "/", self.ileczęści)
        log("doładuj_część ", numer_części, " - koniec")

    def wymuś_załadowanie(self):#żeby podglądnąć
        log("Wymuszone załadowanie")
        for i in range(self.ileczęści):
            self.doładuj_część(i)



#invoiceation()
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
def unidecode(s):
    return "".join(map(lambda c: ogonki[c.lower()] if c.lower() in ogonki else c.lower(), s))
def normalizuj(słowo):
    return unidecode(słowo).lower()

_słowa, _gołe = None, None
_slownik_zaladowany = False
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
            log("SLOWNIK NIE ZALADOWANY")
            raise RuntimeError("SŁOWNIK NIE ZAŁADOWANY")
        return f(*args, **kwargs)
    return wrapper

def zachowaj_wiekość_liter(stare, nowe):
    if len(stare)!= len(nowe):
        return nowe
    return "".join([n.upper() if s.isupper() else n.lower() for s,n in zip(stare, nowe)])

if PRZERZUCONE:
    SŁOWNIKOWY = 0x000000
    NIEPOPRAWIALNY = 0x0000AA
    POPRAWIONY = 0x009900
    POPRAWIONY_HEURYSTYCZNIE = 0x0099AA
else:
    SŁOWNIKOWY = 'SŁOWNIKOWY'
    NIEPOPRAWIALNY ="NIEPOPRAWIALNY"
    POPRAWIONY = "POPRAWIONY"
    POPRAWIONY_HEURYSTYCZNIE ="POPRAWIONY_HEURYSTYCZNIE"


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
def korekta_ost(tekst):
    matches = [match for match in p.finditer(tekst)]
    if len(matches)<1:
        return None
    else:
        match = matches[-1]#ostatnie słowo, czyli najbliżej kursora
        return [*korekta(match.group(0)), match.span()]