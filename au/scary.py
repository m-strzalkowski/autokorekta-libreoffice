import unohelper
from com.sun.star.awt import XKeyHandler
from com.sun.star.awt import Key
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
from com.sun.star.awt.MessageBoxType import INFOBOX
log_file_path = "C:\\Users\\ms\\Documents\\pythonlibreout\\log.txt"

fs_fkeys={} # dictionary of keys to identify each key
for key in dir(Key):
    fs_fkeys[getattr(Key, key)] = key

#Idiosyncrasies
# Shift_L, Ctrl_L, Alt_L are not reported as separate keys but are reported as modifiers
# 1,2 and 4 respectively. Shift_R and Ctrl_R are identical to their Left twins
# Alt_R (AltGr) is not reported and not a modifier.
# Super_R (Right Windows) is not reported but is a modifier, even though it doesn't modify any keys.
# It reports as modifier 8
# Super_L (Left Windows) is not reported and not a modifier.
# Caps_Lock and Num_Lock report as unidentified keys but not as modifiers.

# track key input with option of consuming the input (return True)
def fs_Tracker(*args):
    doc = XSCRIPTCONTEXT.getDocument()
    desktop = XSCRIPTCONTEXT.getDesktop()
    global contr, oEventHandler

    contr = desktop.getCurrentComponent().getCurrentController()
    oEventHandler = KeyHandler(doc)
    contr.addKeyHandler(oEventHandler)
    mess = "Key tracker active\nTo deactivate close document or Shift+Alt+Ctrl K"
    heading = "Key Tracker"
    MessageBox(None, mess, heading, INFOBOX, BUTTONS_OK)

class KeyHandler( unohelper.Base, XKeyHandler ):
    log = None
    def __init__(self, parent):
        self.parent = parent
        self.log = open(log_file_path, "a", encoding="utf-8")
        return None

    def Terminate ( self, event ):
        mess = "Key tracker deactivated!"
        heading = "Key Tracker"
        self.log.close()
        MessageBox(None, mess, heading, INFOBOX, BUTTONS_OK)

        contr.removeKeyHandler(oEventHandler)

    def keyPressed( self,  event ):
        k = event.KeyCode
        c = event.KeyChar.value 
        mods = event.Modifiers
        #with open(log_file_path, "a", encoding="utf-8") as log_file:
        self.log.write("\nkey:", k, c, mods)
        # mods are additive
        # 0 - None
        # 1 - Shift
        # 2 - Ctrl
        # 4 - Alt
        # 8 - Super_R   
        if c == "K" and mods == 7: #Shift+Ctrl+Alt+k
            self.Terminate(None)
            return True # Returning True consumes the key
                        # Thus assigning this macro to the same keyboard shortcut means that
                        # the macro is toggled On/Off by Shift+Alt+Ctrl+k
        if k in fs_fkeys:
            name = fs_fkeys[k]
        else:
            name = "Undefined"
        print(name, k, c, mods)
        return False

    def keyReleased( self, event ):
        return False

def MessageBox(ParentWindow, MsgText, MsgTitle, MsgType, MsgButtons):
    ctx = XSCRIPTCONTEXT.getComponentContext()
    sm = ctx.ServiceManager
    si = sm.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
    mBox = si.createMessageBox(ParentWindow, MsgType, MsgButtons, MsgTitle, MsgText)
    mBox.execute()

#List components that are accessible
g_exportedScripts = fs_Tracker,   
