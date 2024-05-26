from unidecode import unidecode
import pickle
import glob
import os
import shutil
#generacja_slownika.sh
def czytaj__wszystko_w_katalogu(directory, funkcj_od_f):
    # Use glob to get a list of files in the directory
    files = glob.glob(os.path.join(directory, '*'))
    # Sort the files alphabetically
    files.sort()
    print("PLIKI:", files)
    # Iterate over the sorted list of files
    for file in files:
        if os.path.isfile(file):  # Ensure it's a file, not a directory
            with open(file, 'r', encoding='utf-8') as f:
                print('otwarto ', file)
                funkcj_od_f(f)
ss = []
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
    #if s == 'robie' or s=='robię' or g=='robie':
    #    print("rb:",g,s)
    if g in gołe and s not in gołe[g]:
    #    if s == 'robie' or s=='robię':
    #        print("@1")
        gołe[g] = gołe[g] + [s]
    else:
        #if s == 'robie' or s=='robię':
    #        print("@2")
        gołe[g] = [s]
print(gołe['robie'])
print("gołe:", len(gołe))

from autokorekta import ile_części, zapisz_pokawałkowany_słownik, poz_prot_pkl
with open('słownik.pickle', 'wb') as f:
    słownik = (słowa, gołe)
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(słownik, f, poz_prot_pkl())#pickle.HIGHEST_PROTOCOL)
shutil.rmtree(os.path.join(katalog_skryptow, "__pycache__"))
zapisz_pokawałkowany_słownik(słowa, os.path.join(".", "słownik_skompilowany", "słowa"), ile_części(), rób_katalog=True)
zapisz_pokawałkowany_słownik(gołe, os.path.join(".", "słownik_skompilowany", "gołe"), ile_części(), rób_katalog=True)
print("Wygenerowano pikla")