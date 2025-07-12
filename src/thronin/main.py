# Load splash screen first.
from thronin.lib.splash_screen import splash_screen
from thronin.application import Application
from thronin.lib.errors import (
    IncorrectWindowSize,
    IncorrectWindowsDPI,
    TesseractNotInstalled,
    TesseractValidationFailed,
    show_error_popup,
)


def main():
    try:
        app = Application()
        app.run()
    except IncorrectWindowSize as e:
        splash_screen.close_splash_screen()
        show_error_popup(
            "Incorrect Window Size",
            "It appears the Throne and Liberty is not setup correctly. Click OK to open the configuration guide.",
            "https://www.patreon.com/posts/how-to-set-up-119530966",
        )
    except IncorrectWindowsDPI as e:
        splash_screen.close_splash_screen()
        show_error_popup(
            "Incorrect Windows DPI Scaling",
            "Your Windows DPI Scaling is not set to 100%. Click OK to open the configuration guide.",
            "https://www.patreon.com/posts/how-to-set-up-119530966",
        )
    except TesseractNotInstalled as e:
        splash_screen.close_splash_screen()
        show_error_popup(
            "Tesseract Not Installed",
            "It appears Tesseract is not installed. Click OK to open the install guide.",
            "https://www.patreon.com/posts/how-to-install-119532580",
        )
    except TesseractValidationFailed as e:
        splash_screen.close_splash_screen()
        show_error_popup(
            "Tesseract Validation Failed",
            "Tesseract failed validation. Click OK to open the install guide.",
            "https://www.patreon.com/posts/how-to-install-119532580",
        )
    except BaseException as e:
        splash_screen.close_splash_screen()
        show_error_popup(
            "Thronin Error Encountered",
            f"An unexpected error occurred.\n\n"
            f"To help us diagnose the issue, please upload the generated 'error_package' to the support channel on Discord.\n\n"
            f"Error Details:\n{e}",
            None,
        )


if __name__ == "__main__":
    main()
