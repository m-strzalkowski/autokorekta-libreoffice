windows_path = "%APPDATA%\\LibreOffice\\4\\user\\Scripts\\python"
unix_path = "$HOME/.config/libreoffice/4/user/Scripts/python"
import os
import platform
import shutil
import re
def expand_path(p):
    return os.path.expandvars(p)

katalog_skryptow = None
if platform.system() == "Windows":
    print("WINDOWS")
    katalog_skryptow = expand_path(windows_path)
else:
    print("UNIX?")
    katalog_skryptow = expand_path(unix_path)
print("USTALONO KATALOG SKRYPTOW UŻYTKOWNIKA DLA PYTHONA NA:", katalog_skryptow)
print("ENTER - zostaw / wpisz ścieżkę")
linia = input()
if len(linia)>1:
    katalog_skryptow = linia
katalog_oryginalny = os.path.dirname(__file__)
print("KOPIOWANIE Z ",katalog_oryginalny,"DO ", katalog_skryptow)
do_skopiowania = [
    'autokor.py',# główne makro
    'makra_wspolne.py', #różne przydatne funkcje
    'autokor_wspolne.py', #logi
    'autokorekta.py', #właściwa logika autokorekty
]
# for nazwa in do_skopiowania:
#     print("KOpiuję ", nazwa)
#     shutil.copyfile(os.path.join(katalog_oryginalny, nazwa), os.path.join(katalog_skryptow, nazwa))
podwoj_odwr_ukośniki = lambda s: s.replace("\\", "\\\\")

def zamień(tekst, nazwa_symbolu, nowa_wartość):
    return re.sub(r"("+nazwa_symbolu+r"=).*", "\\1"+nowa_wartość+"",tekst)
def zamień_ścieżkę(tekst, nazwa_stałej, ścieżka_do_podmiany):
    return re.sub(r"("+nazwa_stałej+r"=).*", "\\1\""+podwoj_odwr_ukośniki( podwoj_odwr_ukośniki(ścieżka_do_podmiany))+"\"",tekst)

def zmień_kod_by_działał_gdzie_indziej(kod):
    kod = zamień(kod, "PRZERZUCONE", "True")
    kod = zamień_ścieżkę(kod, "KATALOG_ORYGINALNY", katalog_oryginalny)
    kod = zamień_ścieżkę(kod, "KATALOG_SKRYPTOW", katalog_skryptow)
    return kod

def kopiuj_ustawiając_ścieżki(plik, z, do):
    t = open(os.path.join(katalog_oryginalny, plik), "r", encoding="utf-8").read()
    do = open(os.path.join(katalog_skryptow, plik), "w", encoding="utf-8")
    do.write(zmień_kod_by_działał_gdzie_indziej(t))
    do.close()
    print(f"kopiuj_ustawiając_ścieżki({plik}) z {z} do {do}")
for nazwa in do_skopiowania:
    kopiuj_ustawiając_ścieżki(nazwa, os.path.join(katalog_oryginalny, nazwa), os.path.join(katalog_skryptow, nazwa))

# def kopiuj_i_dołóż(plik):
#     tekst_dokładany = f"\nKATALOG_SKRYPTOW=\"{podwoj_odwr_ukośniki(katalog_skryptow)}\"\nKATALOG_ORYGINALNY=\"{podwoj_odwr_ukośniki(katalog_oryginalny)}\""
#     z = open(os.path.join(katalog_oryginalny, plik), "r", encoding="utf-8").read()
#     do = open(os.path.join(katalog_skryptow, plik), "w", encoding="utf-8")
#     do.write(z)
#     do.write(tekst_dokładany)
#     do.close()
#     print(f"kopiuj_i_dołóż({plik})")
#kopiuj_i_dołóż('autokor_katalogi.py')
shutil.rmtree(os.path.join(katalog_skryptow, "__pycache__"))
print("koniec")
