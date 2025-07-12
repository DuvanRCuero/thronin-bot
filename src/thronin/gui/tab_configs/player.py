import tkinter as tk
from tkinter import ttk
from thronin.gui.widget_helpers import create_entry, create_scrollable_frame
from thronin.gui.tab_configs.quickslot_builds.bow_staff import BowStaff
from thronin.gui.gui_config import (
    LABEL_FONT,
    COMBOBOX_FONT,
    ENTRY_FONT,
    SEPARATOR_FONT,
    HEADER_FONT,
)


class Player:
    def __init__(self, parent, options, widgets):
        self.tab_name = "Player"
        self.parent = parent
        self.options = options
        self.widgets = widgets
        self.build_ui()

    def build_ui(self):
        # Create a canvas and vertical scrollbar to allow scrolling of tab content
        self.frame, canvas = create_scrollable_frame(self.parent)
        row = 0

        # Create player percentage entries
        entry_specs = [
            ("Percent to use Companion:", "player_percent_to_use_companion"),
            (
                "Percent to use Health Recovery Skills:",
                "player_percent_to_use_health_recovery_skills",
            ),
            ("Percent to use Health Potion:", "player_percent_to_use_health_potion"),
            (
                "Percent to use Mana Recovery Skills:",
                "player_percent_to_use_mana_recovery_skills",
            ),
            ("Percent to use Mana Potion:", "player_percent_to_use_mana_potion"),
        ]
        for label_text, key in entry_specs:
            row = create_entry(
                self.frame, self.options, self.widgets, label_text, key, row
            )

        # Separator: "Quick Slots" section
        sep_label = ttk.Label(self.frame, text="Quick Slots", font=SEPARATOR_FONT)
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Build selection frame (above the table)
        build_frame = ttk.Frame(self.frame)
        build_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        row += 1

        ttk.Label(build_frame, text="Select Build:", font=LABEL_FONT).pack(
            side="left", padx=5
        )
        # Dictionary mapping build names to their classes; add additional builds as needed.
        self.build_options = {
            "Bow/Staff": BowStaff,
            # "Other Build": OtherBuildClass,
        }
        build_names = list(self.build_options.keys())
        self.build_combobox = ttk.Combobox(
            build_frame, values=build_names, state="readonly", font=COMBOBOX_FONT
        )
        self.build_combobox.pack(side="left", padx=5)
        self.build_combobox.set(build_names[0])
        load_button = ttk.Button(
            build_frame, text="Load Build", command=self.load_build
        )
        load_button.pack(side="left", padx=5)

        # Create a table for quick slot settings with the new column order
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        row += 1

        # Define headers: Monitored, Type, Repetitions, Casting
        headers = ["Monitored", "Type", "Repetitions", "Casting"]
        for col, header in enumerate(headers):
            hdr_label = ttk.Label(table_frame, text=header, font=HEADER_FONT)
            hdr_label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

        # Ensure each column expands horizontally
        for col in range(len(headers)):
            table_frame.columnconfigure(col, weight=1)

        # Options for the "Type" combobox column
        type_options = ["Combat", "Health Recovery", "Mana Recovery"]

        # Define the quick slots as a dictionary mapping internal names to pretty names
        quick_slots = {
            "quickslot1": "Quick Slot 1",
            "quickslot2": "Quick Slot 2",
            "quickslot3": "Quick Slot 3",
            "quickslot4": "Quick Slot 4",
            "quickslot5": "Quick Slot 5",
            "quickslot6": "Quick Slot 6",
            "quickslot7": "Quick Slot 7",
            "quickslot8": "Quick Slot 8",
            "quickslot9": "Quick Slot 9",
            "quickslot10": "Quick Slot 10",
            "quickslot11": "Quick Slot 11",
            "quickslot12": "Quick Slot 12",
        }

        # Create table rows for each quick slot with new layout
        for i, (slot, pretty_name) in enumerate(quick_slots.items(), start=1):
            # Column 0: Frame containing Monitored checkbox and quick slot pretty name.
            ms_frame = ttk.Frame(table_frame)
            ms_frame.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            var_monitored = tk.BooleanVar(
                value=self.options.get(f"{slot}_monitored_by_bot", False)
            )
            chk_monitored = ttk.Checkbutton(ms_frame, variable=var_monitored)
            chk_monitored.pack(side="left")
            name_label = ttk.Label(ms_frame, text=pretty_name, font=LABEL_FONT)
            name_label.pack(side="left", padx=(5, 0))
            self.widgets[f"{slot}_monitored_by_bot"] = var_monitored

            # Column 1: "Type" combobox
            cmb_type = ttk.Combobox(
                table_frame, values=type_options, state="readonly", font=COMBOBOX_FONT
            )
            default_type = self.options.get(f"{slot}_type", type_options[0])
            cmb_type.set(default_type)
            cmb_type.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.widgets[f"{slot}_type"] = cmb_type

            # Column 2: "Repetitions" entry field
            entry_rep = ttk.Entry(table_frame, width=10, font=ENTRY_FONT)
            default_rep = self.options.get(f"{slot}_repetitions", "0")
            entry_rep.insert(0, str(default_rep))
            entry_rep.grid(row=i, column=2, padx=5, pady=5, sticky="ew")
            self.widgets[f"{slot}_repetitions"] = entry_rep

            # Column 3: "Casting" checkbox
            var_casting = tk.BooleanVar(
                value=self.options.get(f"{slot}_casting_skill", False)
            )
            chk_casting = ttk.Checkbutton(table_frame, variable=var_casting)
            chk_casting.grid(row=i, column=3, padx=5, pady=5, sticky="w")
            self.widgets[f"{slot}_casting_skill"] = var_casting

        self.frame.columnconfigure(1, weight=1)

    def load_build(self):
        """
        Load the selected build from the dropdown and update the quick slot table accordingly.
        """
        selected_build_name = self.build_combobox.get()
        build_class = self.build_options.get(selected_build_name)
        if build_class:
            build_instance = build_class()  # instantiate the build
            config = build_instance.config
            # Iterate over each configuration key and update the corresponding widget.
            for key, value in config.items():
                widget = self.widgets.get(key)
                if widget is None:
                    continue
                # For BooleanVar (checkboxes)
                if isinstance(widget, tk.BooleanVar):
                    widget.set(bool(value))
                # For comboboxes (for 'type')
                elif isinstance(widget, ttk.Combobox):
                    widget.set(str(value))
                # For entries (for 'repetitions')
                elif isinstance(widget, ttk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
