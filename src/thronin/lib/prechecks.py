from thronin.lib.errors import (
    IncorrectWindowsDPI,
    TesseractNotInstalled,
    TesseractValidationFailed,
)
import ctypes
import subprocess
import sys


class PreChecks:

    def check_dpi_scaling(self):
        # Get the DPI for the system using GetDpiForSystem (Windows 10 and above)
        if sys.getwindowsversion().major >= 10:
            user32 = ctypes.windll.user32
            dpi = user32.GetDpiForSystem()  # Get system DPI
        else:
            # Fallback for older versions of Windows
            gdi32 = ctypes.windll.gdi32
            hdc = gdi32.GetDC(0)
            dpi = gdi32.GetDeviceCaps(hdc, 88)  # 88 is the index for DPI

        if dpi != 96:  # 96 DPI corresponds to 100% scaling
            raise IncorrectWindowsDPI()

    def validate_tesseract(self):
        try:
            subprocess.run(
                ["tesseract", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError:
            raise TesseractNotInstalled
        except subprocess.CalledProcessError as e:
            raise TesseractValidationFailed


prechecks = PreChecks()
