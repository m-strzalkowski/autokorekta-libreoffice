from autokorekta import *
załaduj()
from autokorekta import _słowa
from autokorekta import _gołe
#_słowa.wymuś_załadowanie()
if __name__=="__main__":
    while True:
        print(">",end="")
        linia = input()
        print(korekta_ost(linia))