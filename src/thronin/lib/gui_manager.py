from mttkinter import mtTkinter as tk
from thronin.global_variables.temp import temp
from thronin.gui.overlay import Overlay
from thronin.gui.ui import UI
from thronin.gui.debug_overlay import DebugOverlay
from thronin.lib.application_info import application_title, ico_path
from thronin.lib.logger import logger
import time


class GUIManager:
    def __init__(self):
        self.running = False
        self.root = None
        self.ui = None
        self.overlay = None
        self.debug_overlay = None
        self.time_of_last_UI_update = 0
        self.exit_button_pressed = False

    def run(self):
        self.running = True
        self.root = tk.Tk()
        self.root.title(application_title)
        # set location of window to the left of game window
        game_window_coords = temp.get("window_xywh")
        if game_window_coords:
            game_x, game_y, game_width, game_height = game_window_coords
            window_width = 570
            window_height = 720
            # Place the window to the left of the game window
            new_x = game_x - (window_width + 8)  # 8 to account for window border
            new_y = game_y - 31  # 31 to account for window title
            self.root.geometry(f"{window_width}x{window_height}+{new_x}+{new_y}")
        else:
            # If game window coordinates aren't available, place UI window at a default position
            self.root.geometry(f"{window_width}x{window_height}+100+100")

        self.root.iconbitmap(ico_path)
        self.root.protocol("WM_DELETE_WINDOW", self._exit_ui)

        # Initialize UI and Overlay
        self.ui = UI(self.root)
        self.overlay = Overlay(self.root, application_title)
        self.debug_overlay = DebugOverlay(self.root)

        self.root.mainloop()
        logger.debug(f"Run loop completed. Destroying instance.")
        self.root.destroy()  # Destroy the Tk instance
        self.root = None
        self.running = False

    def stop(self):
        logger.debug("Stop Thread Initiated.")
        self.root.quit()  # Stop the mainloop
        logger.debug("Stop Thread Complete.")

    def _exit_ui(self):
        logger.debug("GUI exit button pressed.")
        self.exit_button_pressed = True

    def update(self):
        if self.overlay:
            self.overlay.update()

    def toggle_overlay(self):
        self.overlay.toggle_overlay()
        self.debug_overlay.toggle_overlay()

    def hide_overlay(self):
        if self.overlay:
            self.overlay.hide_overlay()
        else:
            logger.debug("Can't hide overlay as it's not initialized.")
        if self.debug_overlay:
            self.debug_overlay.hide_overlay()
        else:
            logger.debug("Can't hide debug_overlay as it's not initialized.")

    def show_overlay(self):
        if self.overlay:
            self.overlay.show_overlay()
        else:
            logger.debug("Can't show overlay as it's not initialized.")
        if self.debug_overlay:
            self.debug_overlay.show_overlay()
        else:
            logger.debug("Can't show debug_overlay as it's not initialized.")


gui_manager = GUIManager()
debug_overlay = gui_manager.debug_overlay
