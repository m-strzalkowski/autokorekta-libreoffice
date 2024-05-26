import uno
from datetime import datetime


def color_last_word_and_log(arg=None):
    dupa
    """Colors the last word typed green, appends a + sign to it, and logs the operation to a file."""
    # Define the path to the log file
    log_file_path = "C:\\Users\\ms\\Documents\\pythonlibreout\\log.txt"

    # Get the document context
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    
    if not hasattr(model, "Text"):
        return None

    # Get the text cursor
    cursor = model.getCurrentController().getViewCursor()

    # Move the cursor left by 32 characters and select the text
    cursor.goLeft(32, True)
    selected_text = cursor.getString()

    # Find the start of the last word in the selected text
    last_space_index = selected_text.rfind(' ')
    if last_space_index == -1:
        # No space found, the entire selection is the last word
        last_word_start = 0
    else:
        last_word_start = last_space_index + 1

    # Deselect the current selection
    cursor.collapseToEnd()

    # Move the cursor to the start of the last word and select it
    cursor.goLeft(32 - last_word_start, False)
    cursor.goRight(len(selected_text) - last_word_start, True)
    
    last_word = cursor.getString()

    # Append a + sign to the last word
    cursor.setString(last_word + '+')

    # Apply green color to the last word
    cursor.CharColor = 0x00FF00  # Green color in RGB
    cursor.collapseToEnd()
    cursor.CharColor = 0x000000

    # Log the operation with timestamp
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()}: Colored word '{last_word}' green and appended +.\n")

    return None
