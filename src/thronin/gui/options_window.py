from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.global_variables.trackers import trackers
from thronin.lib.logger import logger
from thronin.lib.window_manager import window_manager
from thronin.lib.player import player
from tkinter import ttk
import tkinter as tk
from thronin.gui.tab_configs.general import General
from thronin.gui.tab_configs.player import Player
from thronin.gui.tab_configs.safe_zone import SafeZone
from thronin.gui.tab_configs.farming import Farming
from thronin.gui.tab_configs.key_bindings import KeyBindings

# from thronin.global_variables.routines import routines


class OptionsWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Options")
        self.window.resizable(True, True)

        # Create a Notebook to hold tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Shared dictionary to hold references to widgets across tabs
        self.widgets = {}

        # Create Tabs
        self.tabs = {}

        # General Tab
        tab_frame = ttk.Frame(self.notebook)
        self.tabs["General"] = General(tab_frame, options, self.widgets)
        self.notebook.add(tab_frame, text="General")

        # Player Tab
        tab_frame = ttk.Frame(self.notebook)
        self.tabs["Player"] = Player(tab_frame, options, self.widgets)
        self.notebook.add(tab_frame, text="Player")

        # Safe Zone Tab
        tab_frame = ttk.Frame(self.notebook)
        self.tabs["Safe Zone"] = SafeZone(tab_frame, options, self.widgets)
        self.notebook.add(tab_frame, text="Safe Zone")

        # Farming Tab
        tab_frame = ttk.Frame(self.notebook)
        self.tabs["Farming"] = Farming(tab_frame, options, self.widgets)
        self.notebook.add(tab_frame, text="Farming")

        # Key Bindings Tab
        tab_frame = ttk.Frame(self.notebook)
        self.tabs["Key Bindings"] = KeyBindings(tab_frame, options, self.widgets)
        self.notebook.add(tab_frame, text="Key Bindings")

        # Create a frame for the Save and Reset buttons at the bottom.
        self.buttons_frame = ttk.Frame(self.window)
        self.buttons_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.reset_button = ttk.Button(
            self.buttons_frame,
            text="Reset to Defaults",
            command=self.reset_options,
            takefocus=0,
        )
        self.reset_button.pack(side="left", padx=(0, 5))

        self.save_button = ttk.Button(
            self.buttons_frame, text="Save", command=self.save_options, takefocus=0
        )
        self.save_button.pack(side="right", padx=(0, 5))

    def save_options(self):
        default_options = options.get_default_options()
        for key, widget in self.widgets.items():
            # Determine the value based on widget type.
            if isinstance(widget, ttk.Button):
                continue
            elif isinstance(widget, ttk.Combobox):
                value = widget.get()
            elif isinstance(widget, ttk.Entry):
                if "keybind_" in key:
                    continue  # This is already set when the key is captured, just needs to be saved.
                value = widget.get()
            elif isinstance(widget, tk.BooleanVar):
                value = widget.get()
            elif isinstance(widget, tk.StringVar):
                value = widget.get().strip()
            # Handle text widgets stored as dict.
            elif isinstance(widget, dict) and "widget" in widget:
                textbox = widget["widget"]
                value = textbox.get("1.0", tk.END).strip()
                widget["var"].set(value)
            else:
                raise SystemExit(f"Unsupported widget type: {type(widget)}")

            # Convert the value to the type of the default value if possible.
            default_val = default_options.get(key)
            if default_val is not None:
                try:
                    if isinstance(default_val, bool):
                        value = bool(value)
                    elif isinstance(default_val, int):
                        value = int(value)
                    elif isinstance(default_val, float):
                        value = float(value)
                    # Strings and others remain as-is.
                except ValueError:
                    logger.error(
                        f"Could not convert {key} value '{value}' to type {type(default_val)}"
                    )
            # Update the options object.
            options.set(key, value)

        # Save the updated options to file.
        options.save_to_file()
        logger.info("Options saved.")

        # Close the options window.
        self.window.destroy()

        # Reload necessary modules.
        trackers.load()
        player.load_player()
        # routines.load()
        temp.set("current_routine", None)
        window_manager.bring_window_to_foreground()

    def reset_options(self):
        # Reset options in the Options instance.
        options.reset_to_defaults()

        # Save the reset options to file.
        options.save_to_file()
        logger.info("Options reset to defaults.")

        # Close the options window.
        self.window.destroy()
