import tkinter as tk
from tkinter import ttk
from thronin.gui.widget_helpers import create_combobox, create_scrollable_frame


class General:
    def __init__(self, parent, options, widgets):
        self.tab_name = "General"
        self.parent = parent
        self.options = options
        self.widgets = widgets
        self.build_ui()

    def build_ui(self):
        # Create a canvas and vertical scrollbar to allow scrolling of tab content
        self.frame, canvas = create_scrollable_frame(self.parent)
        row = 0

        # Force Routine combobox
        row = create_combobox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Force Routine:",
            values=[
                "None",
                "fishing",
                "safe_zone",
                "battle_assist",
                "battle_party",
                "battle_noexit",
            ],
            option_key="force_routine",
            row=row,
        )

        # Ensure that the second column expands properly
        self.frame.columnconfigure(1, weight=1)
