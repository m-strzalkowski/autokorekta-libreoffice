import os
import uno
from datetime import datetime
from time import sleep

def log_on_save_as(arg):
    """Log a message to a file when a document is saved as a new file."""
    # Define the path to the log file
    log_file_path = "C:\\Users\\ms\\Documents\\pythonlibreout\\log.txt"

    # Get the document context
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Title"):
        return None

    # Get the document title
    doc_title = model.Title if model.Title else "Untitled"

    # Log the message with timestamp
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()}: Document '{doc_title}' was saved as a new file.\n")
        #sleep(5)
        log_file.write("dwa")
        #log_file.write(str(arg))
    return None
