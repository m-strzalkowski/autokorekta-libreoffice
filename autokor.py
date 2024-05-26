#deployment-dependent params
KATALOG_SKRYPTOW="."
KATALOG_ORYGINALNY="."
PRZERZUCONE=False
import sys
sys.path.append(KATALOG_SKRYPTOW)

import uno, unohelper
from com.sun.star.awt import XKeyHandler
from com.sun.star.awt.Key import SPACE
from com.sun.star.uno import Exception as UnoException

from makra_wspolne import *
from autokorekta import *
from autokor_wspolne import log
#XSCRIPTCONTEXT = xscriptcontext()
# Global variable to store the key handler
oKeyHandler = None
def TEST():
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Text"):
        return None

    # Get the text cursor
    cursor = model.getCurrentController().getViewCursor()
    msgbox("AA.1"+cursor.getString())
    cursor.goLeft(1, True)
    msgbox("AA2"+cursor.getString())
    cursor.goLeft(1, False)
    msgbox("B"+cursor.getString())
    cursor.goLeft(-1, True)
    msgbox("C"+cursor.getString())
    cursor.goRight(1, True)
    msgbox("D"+cursor.getString())
    cursor.goRight(-1, True)
    msgbox("E"+cursor.getString())
    cursor.collapseToEnd()
    msgbox("F"+cursor.getString())

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
def poprawka(arg=None):
    # Get the document context
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Text"):
        return None

    # Get the text cursor
    cursor = model.getCurrentController().getViewCursor()
    if not cursor.isCollapsed():
        msgbox("Not collapsed")
        return None
    # Move the cursor left by 32 characters and select the text
    cursor.goLeft(32, True)
    #msgbox("do lewej")
    podglądany_tekst = cursor.getString()
    instrukcja = korekta_ost(podglądany_tekst)
    dłtekstu = len(podglądany_tekst)
    msgbox("Instrukcja:"+str(instrukcja))
    if instrukcja is None:
        cursor.collapseToEnd()
        return None
    poprawione_słowo, kolor, zasięg_org = instrukcja
    cursor.collapseToStart()
    #msgbox("@1.1:"+str(cursor))
    cursor.goRight(zasięg_org[0], False)
    #msgbox("@2:"+str(cursor))
    cursor.collapseToEnd()
    #msgbox("@3:"+str(cursor))
    cursor.goRight(zasięg_org[1]-zasięg_org[0], True)
    #msgbox("@4:"+str(cursor))
    cursor.setString(poprawione_słowo)
    #msgbox("@5:"+str(cursor))
    cursor.CharColor = kolor
    #msgbox("@6:"+str(cursor))
    cursor.collapseToEnd()
    #msgbox("@7:"+str(cursor))
    #msgbox("@8:"+str(cursor))
    cursor.goRight(dłtekstu- zasięg_org[1], False)
    cursor.CharColor = 0x000000
    #msgbox("@9:"+str(cursor))
    cursor.collapseToEnd()
    #msgbox("@10:"+str(cursor))
    #cursor.goToRange(cursorPrevPos, false)
    
    #msgbox("koniec")
    return None
def poprawka2(arg=None):
    # Get the document context
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Text"):
        return None

    # Get the text cursor
    cursor = model.getCurrentController().getViewCursor()
    if not cursor.isCollapsed():
        msgbox("Not collapsed")
        return None
    # Move the cursor left by 32 characters and select the text
    cursor.goLeft(32, True)
    #msgbox("do lewej")
    selected_text = cursor.getString()
    instrukcja = korekta_ost(selected_text)
    #msgbox("Instrukcja:"+str(instrukcja))
    if instrukcja is None:
        return None
    cursor.collapseToStart()
    #msgbox("collapseToStart1")
    cursor.goRight(instrukcja[2][1], True)
    #msgbox("goRight(instrukcja[2][1]=", instrukcja[2][1])
    cursor.collapseToEnd()
    #msgbox("collapseToEnd1", instrukcja[2][1])
    cursor.goLeft(instrukcja[2][1]-instrukcja[2][0], True)
    #msgbox("goLeft(instrukcja[2][1]-instrukcja[2][0]")
    cursor.setString(instrukcja[0])
    cursor.CharColor = instrukcja[1]#0x00FF00
    cursor.collapseToEnd()
    cursor.CharColor = 0x000000
    cursor.goRight(instrukcja[2][1]-instrukcja[2][0], True)
    cursor.collapseToEnd()
    #cursor.goToRange(cursorPrevPos, false)
    
    #msgbox("koniec")
    return None


# Bind the functions to be called from LibreOffice UI or other events
g_exportedScripts = TEST, AUTOKOR_USTAW_SPACJOLAPA, AUTOKOR_USUN_SPACJOLAPA
