from thronin.lib.application_info import cache_path
from thronin.lib.logger import logger
from tkinter import Tk, messagebox
import traceback
import webbrowser


class TesseractNotInstalled(Exception):
    def __init__(self):
        message = "Tesseract-OCR is not installed."
        super().__init__(message)


class TesseractValidationFailed(Exception):
    def __init__(self):
        message = "Tesseract-OCR validation failed."
        super().__init__(message)


class IncorrectWindowSize(Exception):
    def __init__(self, window_height):
        message = f"Incorrect Window Height: {window_height}"
        super().__init__(message)


class IncorrectWindowsDPI(Exception):
    def __init__(self):
        message = f"Incorrect Windows DPI Scaling."
        super().__init__(message)


def show_error_popup(title, message, url=None):
    logger.error(traceback.format_exc())
    root = Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Make the root window always on top
    messagebox.showerror(title, message)
    root.destroy()  # Destroy the root window to clean up
    if url:
        webbrowser.open(url)  # Open the URL in the default browser
