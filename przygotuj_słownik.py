#Przetwarza słownik z tekstowej postacji do formy czytelnej dla korekty
from unidecode import unidecode
import pickle
import glob
import os
from autokorekta import ile_części
from pokawałkowane_słowniki import zapisz_pokawałkowany_słownik, poz_prot_pkl
#from unidecode import unidecode
from autokorekta import unidecode # prosty zastępnik, by uniknąć instalowania modułów
#generacja_slownika.sh - z sgjp

def czytaj__wszystko_w_katalogu(directory, funkcj_od_f):
    #rozwinięcie gwiazdki
    files = glob.glob(os.path.join(directory, '*'))
    files.sort()
    print("PLIKI:", files)
    for file in files:
        if os.path.isfile(file):  # Ma być plik, nie katalog
            with open(file, 'r', encoding='utf-8') as f:
                print('otwarto ', file)
                funkcj_od_f(f)
ss = []#lista słów
#Wczytuje plik z kolumnami rozdzielonymi tabulatorami i wyłuskoje po prostu pierwszą kolumnę
def czytaj_kawalek_slownika(plik):
    global ss
    ss.extend(list(map(lambda li: li.split('\t')[0].strip(), plik.readlines())))
czytaj__wszystko_w_katalogu("./słownik_podzielony/", czytaj_kawalek_slownika)
#ss=list(map(lambda li: li.split('\t')[0].strip(), open('slownik.test.txt', encoding='utf-8').readlines()))
print("WSZYSTKICH_SLOW: ", len(ss))
słowa = {s:None for s in ss}

def wywal(słowo):
    if słowo in słowa:
        del słowa[słowo]
def dołóż(słowo):
    słowa[słowo] = None
for s in ['sie', 'robie', 'Robie']:
    wywal(s)
for s in ['się']:
    dołóż(s)


gołe = {}
for s in słowa.keys():
    g = unidecode(s.lower())
    if g in gołe and s not in gołe[g]:
        gołe[g] = gołe[g] + [s]
    else:
        gołe[g] = [s]
#print(gołe['robie'])
print("gołe:", len(gołe))


with open('słownik.pickle', 'wb') as f:
    słownik = (słowa, gołe)
    pickle.dump(słownik, f, poz_prot_pkl())#nie pickle.HIGHEST_PROTOCOL, bo python3.8 w libreoffice jeszcze nie zna protokołu 5)

zapisz_pokawałkowany_słownik(słowa, os.path.join(".", "słownik_skompilowany", "słowa"), ile_części(), rób_katalog=True)
zapisz_pokawałkowany_słownik(gołe, os.path.join(".", "słownik_skompilowany", "gołe"), ile_części(), rób_katalog=True)
print("Wygenerowano pikle")