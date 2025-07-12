from mttkinter import mtTkinter as tk
from thronin.global_variables.temp import temp
from thronin.gui.options_window import OptionsWindow
from thronin.lib.logger import log_queue
from tkinter import scrolledtext
import queue
from thronin.gui.gui_config import LABEL_FRAME_FONT, LABEL_FONT, LOG_FONT, ENTRY_FONT


class UI:
    def __init__(self, root):
        self.root = root
        self.options_window = None
        self.log_queue = log_queue
        self._build_frames()
        self.root.after(500, self.update)

    def _build_frames(self):
        self._build_status_frame()
        self._build_log_frame()
        self._build_button_frame()

    def _build_status_frame(self):
        status_frame = tk.LabelFrame(self.root, text="Status", font=LABEL_FRAME_FONT)
        status_frame.pack(fill="x", padx=10, pady=5)
        self.fps_var, _ = self.create_labeled_entry(
            status_frame, "FPS:", str(temp.get("fps")), row=0, disabled=True
        )
        self.bot_running_var, _ = self.create_labeled_entry(
            status_frame,
            "Bot Running:",
            str(temp.get("bot_is_running")),
            row=1,
            disabled=True,
        )
        self.current_routine_var, _ = self.create_labeled_entry(
            status_frame,
            "Current Routine:",
            str(temp.get("current_routine")),
            row=2,
            disabled=True,
        )

    def _build_log_frame(self):
        log_frame = tk.LabelFrame(self.root, text="Logs", font=LABEL_FRAME_FONT)
        log_frame.pack(fill="both", padx=10, pady=5, expand=True)
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(
            log_frame, state=tk.DISABLED, font=LOG_FONT
        )
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

    def _build_button_frame(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        self.options_button = tk.Button(
            button_frame, text="Options", command=self.open_options_window
        )
        self.options_button.pack(pady=5, anchor="e")

    def create_labeled_entry(
        self, parent, label_text, initial_value, row, disabled=False
    ):
        label = tk.Label(parent, text=label_text, width=15, anchor="w", font=LABEL_FONT)
        label.grid(row=row, column=0, padx=(10, 5), pady=2, sticky="w")
        var = tk.StringVar(value=initial_value)
        entry = tk.Entry(parent, textvariable=var, font=ENTRY_FONT)
        if disabled:
            entry.config(state="disabled")
        entry.grid(row=row, column=1, padx=(5, 10), pady=2, sticky="ew")
        parent.grid_columnconfigure(1, weight=1)
        return var, entry

    def open_options_window(self):
        if self.options_window is not None and tk.Toplevel.winfo_exists(
            self.options_window.window
        ):
            self.options_window.window.lift()
            return

        # Update the main window to ensure geometry info is current.
        self.root.update_idletasks()

        # Get the main window's geometry.
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()

        # Define the options window dimensions.
        # Here we choose a width wider than the main window (e.g., 1.5 times the main width)
        options_width = main_width
        options_height = main_height

        # Calculate the new window's position to be to the right of the main window.
        new_x = main_x
        new_y = main_y

        # Create the OptionsWindow.
        self.options_window = OptionsWindow(self.root)
        # Set the geometry of the options window.
        self.options_window.window.geometry(
            f"{options_width}x{options_height}+{new_x}+{new_y}"
        )

    def update(self):
        # Update status fields
        self.fps_var.set(str(temp.get("fps")))
        self.bot_running_var.set(str(temp.get("bot_is_running")))
        self.current_routine_var.set(str(temp.get("current_routine")))

        # Update log text widget
        while True:
            try:
                record = self.log_queue.get_nowait()
                self._update_log(record)
            except queue.Empty:
                break

        # Schedule next update
        self.root.after(500, self.update)

    def _update_log(self, record):
        msg = record.getMessage()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.yview(tk.END)
        self.log_text.config(state=tk.DISABLED)
