import uno
import unohelper
from com.sun.star.task import XJobExecutor
from threading import Timer

class CheckTextAndAppendPlus(unohelper.Base, XJobExecutor):
    def __init__(self, ctx):
        self.ctx = ctx
        self.previous_text = ""
        self.check_interval = 1  # in seconds
        self.timer = None

    def trigger(self, args):
        self.start_timer()

    def start_timer(self):
        self.timer = Timer(self.check_interval, self.check_text)
        self.timer.daemon = True  # Ensures the timer does not prevent program exit
        self.timer.start()

    def check_text(self):
        desktop = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx)
        model = desktop.getCurrentComponent()
        
        if not model or not hasattr(model, "Text"):
            return

        cursor = model.getCurrentController().getViewCursor()
        current_text = cursor.getString()
        
        if len(current_text) > len(self.previous_text) and current_text[-1] == " ":
            cursor.goLeft(1, False)
            cursor.setString("+ ")
            cursor.goRight(1, False)

        self.previous_text = cursor.getString()
        self.start_timer()  # Schedule the next check

def create_instance(ctx):
    return CheckTextAndAppendPlus(ctx)
