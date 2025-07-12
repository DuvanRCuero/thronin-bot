import os
from importlib.util import find_spec

# Close Pyinstller Splash Screen
if "_PYI_SPLASH_IPC" in os.environ and find_spec("pyi_splash"):
    import pyi_splash

    pyi_splash.close()

from thronin.lib.application_info import assets_path
from mttkinter import mtTkinter as tk
from thronin.lib.logger import logger
import threading
import time


class SplashScreen:
    def __init__(self):
        self.splash_screen = None
        self.status_label = None
        self.splash_thread = threading.Thread(target=self._create_splash)
        self.splash_thread.start()
        logger.debug(f"Initializing Splash Screen")

    def _create_splash(self):
        logger.debug(f"Creating Splash Screen")
        splash_root = tk.Tk()
        splash_root.title("Loading Thronin Bot")

        # Center the splash screen on the screen
        window_width, window_height = 400, 200
        screen_width = splash_root.winfo_screenwidth()
        screen_height = splash_root.winfo_screenheight()
        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)
        splash_root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        splash_root.overrideredirect(True)
        splash_root.attributes("-topmost", True)

        # Load and display the background image
        background_image_path = os.path.join(assets_path, "splash.png")
        canvas = tk.Canvas(splash_root, width=window_width, height=window_height)
        canvas.pack(fill="both", expand=True)
        try:
            bg_image = tk.PhotoImage(file=background_image_path)
            canvas.create_image(0, 0, anchor="nw", image=bg_image)
            canvas.image = bg_image  # Keep a reference to avoid garbage collection
        except Exception as e:
            logger.error(f"Error loading splash image: {e}")

        # Add your text labels on top of the canvas
        self.status_label = tk.Label(
            splash_root,
            text="Starting...",
            font=("TkDefaultFont", 12),
            anchor="w",
            bg="white",
        )
        self.status_label.place(relx=0.5, rely=0.5, anchor="center")

        self.splash_screen = splash_root
        self.splash_screen.mainloop()
        logger.debug(f"Run loop completed. Destroying instance.")
        self.splash_screen.destroy()  # Destroy the Tk instance
        self.splash_screen = None

    def update_status(self, message):
        """Update the status label on the splash screen."""
        logger.debug(f"Updating Status: {message}")
        if self.splash_screen:
            if self.status_label:
                self.status_label.config(text=message)
                self.splash_screen.update_idletasks()  # Ensure immediate UI update

    def close_splash_screen(self):
        """Close and destroy the splash screen."""
        if self.splash_screen:
            logger.debug(f"Closing Splash Screen")
            self.splash_screen.quit()  # Stop the mainloop


# Pre-create an instance
splash_screen = SplashScreen()
