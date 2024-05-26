# Implementuje słownik (tylko do odczytu), który zapisany jest w kawałkach na dysku
# Kolejne kawałki doładowywane są w miarę potrzeby (ale nie zapominane - będzie puchnąć z czasem)

# Powód: wczytanie 200MB pikla ze słownikami do autokorekty naraz zajmowało ~6sek na niezłym PCcie i
# a) edytor wieszał się na 6 sekund podczas inicjalizacji autokorekty
# b) każda inicjalizacja autokorekty oznaczała spuchnięcie libreoffice o te >200MB, co powodowało, że włączanie jej za każdym razem mogło być nierozsądne
# Teraz autokorekta przy inicjalizacji nie waży i nie czyta prawie nic, przy odpowiednio małych kawałkach słownika, czas odczytu jest niezauważalny

###### Ten kawałek zmieniany jest przy kopiowaniu poprzez skrypt deploy.py #######
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
PRZERZUCONE=False
##################################################################################
import sys
sys.path.append(KATALOG_SKRYPTOW)
from autokor_wspolne import log, timeit
import time, datetime
from functools import wraps
import os, glob, re
from hashlib import sha256
import pickle

POZ_PROT = 4# nie pickle.HIGHEST_PROTOCOL, bo python3.8 w libreoffice jeszcze nie zna protokołu 5
def poz_prot_pkl():
    return POZ_PROT

#MUSI być deterministyczna, stabilna(zwracać to samo przy różnych uruchomieniach), inaczej zapisany słowik będzie bezużyteczny
def funkcja_haszująca(n:str) -> int:
    if not isinstance(n, str):
        raise Exception("Niestety klucz może byc tylko stringiem a nie "+ str(type(n)))
    return int.from_bytes(sha256(n.encode('utf-8')).digest(), 'big')

# Słownik taki musi mieć cały katalog dla siebie.
def ścieżka_metadanych(katalog):
    return os.path.join(katalog, 'meta.pickle')
def ścieżka_części(katalog, numer_części):
    return os.path.join(katalog, str(numer_części)+".pickle")

# Funkcja do zapisu słownika
def zapisz_pokawałkowany_słownik(słownik:dict, katalog, ileczęści:int, rób_katalog=False):
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
    
    meta = {"typ":"pokawałkowany_słownik", "ilość_części":ileczęści}
    with open(ścieżka_metadanych(katalog), 'wb') as f:
        pickle.dump(meta, f, poz_prot_pkl())
    print("zapisano metadane:",meta)

# Klasa zapewniająca funkcjonalności odczytu, udające pythonowski słownik, ale:
# tylko odczyt elemnu i relacja zawierania, bez długości i całej reszty
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
##################### KONIEC ZAPISYWALNYCH SŁOWNIKÓW #################