# Skrypt do kopiowania makr i procedur autokorekty do katalogu makr użytkownika libreoffice
# Libreoffice widzi makra tylko w specjalnych katalogach, w tym w podanych poniżej (zależnie od systemu)
windows_path = "%APPDATA%\\LibreOffice\\4\\user\\Scripts\\python"
unix_path = "$HOME/.config/libreoffice/4/user/Scripts/python"
# Ale trochę strach kopiować tam cokolwiek poza makrami, a zwłaszcza mnóstwo pliów słowników (poza tym by to trwało)
# Dlatego kod ląduje katalogu z makrami, słowniki zostają i każdy plik dostaje wygenerowane absolutne ścieżki do obu
# (Bo nawet jeśli makra są we wspomnianym katalogu, nie mogą importować się nawzajem, bo katalog roboczy jest jakis inny)

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
## tutaj TRZEBA dopisać pliki uzywane podczas pracy autokorekty z makra ##
do_skopiowania = [
    'autokor.py',# główne makro
    'makra_wspolne.py', #różne przydatne funkcje
    'autokor_wspolne.py', #logi
    'autokorekta.py', #właściwa logika autokorekty
    'pokawałkowane_słowniki.py' #
]

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

try:
    shutil.rmtree(os.path.join(katalog_skryptow, "__pycache__"))
except FileNotFoundError:
    print("__pycache__ nie znaleziono.")
print("koniec")
