#Używa funcjonalności z autokorekta.py do poprawiania na bieżąco tekstu pisanego przez użytkownika w LibreOffice
#W tym celu podpina się do zdarzenia naciśnięca klawisza (ale załącza się tylko na spacjach)

###### Ten kawałek zmieniany jest przy kopiowaniu poprzez skrypt deploy.py #######
#Katalog roboczy makr LibreOffice jest różny od ich lokalizacji i być może róóżny
#Wolałem też nie próbować kopiować plików ze słownikiem do katalogu z makrami (zob. deploy.py)
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
PRZERZUCONE=False
##################################################################################
import sys
sys.path.append(KATALOG_SKRYPTOW)#Katalog roboczy makr uruchamianych z LibreOffice może być róóżny

import uno, unohelper
from com.sun.star.awt import XKeyHandler
from com.sun.star.awt.Key import SPACE
from com.sun.star.uno import Exception as UnoException

from makra_wspolne import *
from autokorekta import *
from autokor_wspolne import log


# Global variable to store the key handler
oKeyHandler = None

## Włącznik ##
def AUTOKOR_USTAW_SPACJOLAPA():
    global oKeyHandler
    try:
        oController = XSCRIPTCONTEXT.getDocument().getCurrentController()
        #msgbox(str(oController.__dir__()))
        # Only if not yet running
        if oKeyHandler is None:
            oKeyHandler = KeyHandler()
            oController.addKeyHandler(oKeyHandler)
            załaduj()
            msgbox("Spacjołap wystartował!")
    except UnoException as e:
        msgbox(str(e))
        print("Error: ", e)
## Wyłącznik ##
def AUTOKOR_USUN_SPACJOLAPA():
    global oKeyHandler
    try:
        oController = XSCRIPTCONTEXT.getDocument().getCurrentController()
        
        # Only if still running
        if oKeyHandler is not None:
            oController.removeKeyHandler(oKeyHandler)
            oKeyHandler = None  # To know later this handler has stopped.
            msgbox("Spacjołap zatrzymany")
    except UnoException as e:
        print("Error: ", e)

#Obiekt, który słucha naciśnięć klawiszy.
#To było odkrycie, że musi dziedziczyć po obu poniższych klasach.
class KeyHandler(unohelper.Base, XKeyHandler):
    def __init__(self):
        pass

    def keyPressed(self, oEvent):
        try:
            if oEvent.KeyCode == SPACE:
                #msgbox("Space was pressed")
                poprawka()
            return False  # Allow other handlers to process the event
        except UnoException as e:
            msgbox("Error: ", str(e))
        return False

    def keyReleased(self, oEvent):
        return True  # Event has been handled

    def disposing(self, oEvent):
        pass

from autokorekta import SŁOWNIKOWY, NIEPOPRAWIALNY, POPRAWIONY, POPRAWIONY_HEURYSTYCZNIE
kolorki = {
    SŁOWNIKOWY : 0x000000,
    NIEPOPRAWIALNY : 0x0000AA,
    POPRAWIONY : 0x009900,
    POPRAWIONY_HEURYSTYCZNIE : 0x0099AA
}

def poprawka(arg=None):
    # Get the document context
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Text"):
        return None

    # Get the text cursor
    cursor = model.getCurrentController().getViewCursor()
    kolor_na_kursorze = cursor.CharColor
    if not cursor.isCollapsed():
        msgbox("Not collapsed")
        return None
    # Zbieramy jakiś, niewielki podgląd wstecz
    cursor.goLeft(32, True)
    podglądany_tekst = cursor.getString()

    #Dekodowanie odpowiedzi z autokorekty
    instrukcja = korekta_ost(podglądany_tekst)
    dłtekstu = len(podglądany_tekst)
    #msgbox("Instrukcja:"+str(instrukcja))
    if instrukcja is None:#Nic nie znalazło do zamiany
        cursor.collapseToEnd() # Trzeba wrócić z kursorem
        return None
    poprawione_słowo, typ_akcji, zasięg_org = instrukcja
    kolor = kolorki[typ_akcji]

    # Sekwencja godna makra, która ma zamienić rozpoznane słowo.
    cursor.collapseToStart()# Zaczynamy nie 32 litery przed kursorem zostawionym przez użytkownika, tylko len(cursor.getString wcześniej)
    #msgbox("@1.1:"+str(cursor))
    cursor.goRight(zasięg_org[0], False)
    #msgbox("@2:"+str(cursor))
    cursor.collapseToEnd()# Jesteśmy na początku słowa do skorygowania
    #msgbox("@3:"+str(cursor))
    cursor.goRight(zasięg_org[1]-zasięg_org[0], True)# Rozszerzamy zaznaczenie do końca słowa
    #msgbox("@4:"+str(cursor))
    cursor.setString(poprawione_słowo)# Zamienia słowo na poprawione
    #msgbox("@5:"+str(cursor))
    cursor.CharColor = kolor# Ustawia kolor zaznaczenia
    #msgbox("@6:"+str(cursor))
    cursor.collapseToEnd()
    #msgbox("@7:"+str(cursor))
    #msgbox("@8:"+str(cursor))
    cursor.goRight(dłtekstu- zasięg_org[1], False)# Wracamy, gdzie użytkownik miał kursor wcześniej
    cursor.CharColor = kolor_na_kursorze#000000000# Przywracamy kolor
    #msgbox("@9:"+str(cursor))
    cursor.collapseToEnd()
    #msgbox("@10:"+str(cursor))
    #msgbox("koniec")
    return None

#Testowe śmieci
def TEST():
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Text"):
        return None

    cursor = model.getCurrentController().getViewCursor()
    msgbox("AA.1"+cursor.getString())
    cursor.goLeft(1, True)


# Bind the functions to be called from LibreOffice UI or other events
g_exportedScripts = TEST, AUTOKOR_USTAW_SPACJOLAPA, AUTOKOR_USUN_SPACJOLAPA
