import tkinter as tk
from tkinter import ttk
from thronin.gui.widget_helpers import create_scrollable_frame, create_keybinding_entry
from thronin.gui.tab_configs.keyboard_layouts.qwerty import QWERTY_KEYBINDS
from thronin.gui.tab_configs.keyboard_layouts.qwertz import QWERTZ_KEYBINDS
from thronin.gui.tab_configs.keyboard_layouts.azerty import AZERTY_KEYBINDS
from thronin.lib.logger import logger
from thronin.global_variables.options import options
from thronin.gui.gui_config import LABEL_FONT, COMBOBOX_FONT, SEPARATOR_FONT


class KeyBindings:
    def __init__(self, parent, options, widgets):
        self.tab_name = "Key Bindings"
        self.parent = parent
        self.options = options
        self.widgets = widgets
        self.build_ui()

    def build_ui(self):
        # Create a canvas and vertical scrollbar for the tab content.
        self.frame, canvas = create_scrollable_frame(self.parent)
        row = 0

        label = ttk.Label(
            self.frame, text="Select Default Keyboard Layout:", font=LABEL_FONT
        )
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        # Dictionary mapping keyboard layouts to their respective Default Configuration.
        deafult_keybind_layouts = (
            "QWERTY",
            "QWERTZ",
            "AZERTY",
        )
        layouts = deafult_keybind_layouts
        layout_combobox = ttk.Combobox(
            self.frame, values=layouts, state="readonly", font=COMBOBOX_FONT
        )
        layout_combobox.set(
            options.get("kb_layout") if options.get("kb_layout") else layouts[0]
        )
        layout_combobox.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        def update_kebinds(selection):
            logger.debug(f"keybind selection: {selection}")
            options.set_default_keybinds(selection)
            # Update all disabled display entries with new default keybind display texts.
            for key, widget in self.widgets.items():
                # Only update keys that represent keybinds and are stored as a dict.
                if key.startswith("keybind_"):
                    updated_text = options.get_keybind(key)["display"]
                    logger.debug(f"Updating UI ({key}): {updated_text}")
                    widget.config(state="normal")
                    widget.delete(0, tk.END)
                    widget.insert(0, updated_text)
                    widget.config(state="disabled")

        # Create a load button
        load_button = ttk.Button(
            self.frame,
            text="Load Keybinds",
            command=lambda: update_kebinds(layout_combobox.get()),
        )
        load_button.grid(row=row, column=2, padx=5, pady=5, sticky="ew")

        # Add to widgets to be checked and move to next row.
        self.widgets["kb_layout"] = layout_combobox
        row += 1

        # Separator: "Bot" section header
        sep_label = ttk.Label(self.frame, text="Bot", font=SEPARATOR_FONT)
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Create a key binding entry for each control
        # Each tuple contains: (Descriptive Label, Option Key)
        bindings = [
            ("Start/Stop the Bot (Home)", "keybind_start_stop_bot"),
            ("Kill the Bot (Insert)", "keybind_kill_bot"),
            ("Toggle Overlay (End)", "keybind_toggle_overlay"),
        ]
        for label_text, option_key in bindings:
            row = create_keybinding_entry(
                self.frame,
                self.options,
                self.widgets,
                label_text + ":",
                option_key,
                row,
            )

        # Separator: "Shortcuts - Character" section header
        sep_label = ttk.Label(
            self.frame, text="Shortcuts - Character", font=SEPARATOR_FONT
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Create a key binding entry for each control
        # Each tuple contains: (Descriptive Label, Option Key)
        bindings = [
            ("Move Forward (w)", "keybind_move_forward"),
            ("Move Backward (s)", "keybind_move_backward"),
            ("Move Left (a)", "keybind_move_left"),
            ("Move Right (d)", "keybind_move_right"),
            ("Jump (Space)", "keybind_jump"),
            ("Basic Attack (e)", "keybind_basic_attack"),
            ("Defense Skills (q)", "keybind_defense_skill"),
            ("Clear Target (x)", "keybind_clear_target"),
            ("Interact (f)", "keybind_interact"),
            ("Return (b)", "keybind_return"),
            ("Astral (r)", "keybind_astral"),
            ("Summon Guardian (c)", "keybind_companion"),
            ("Counterattack (z)", "keybind_counterattack"),
        ]
        for label_text, option_key in bindings:
            row = create_keybinding_entry(
                self.frame,
                self.options,
                self.widgets,
                label_text + ":",
                option_key,
                row,
            )

        # Separator: "Shortcuts - UI" section header
        sep_label = ttk.Label(self.frame, text="Shortcuts - UI", font=SEPARATOR_FONT)
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Create a key binding entry for each control
        # Each tuple contains: (Descriptive Label, Option Key)
        bindings = [
            ("Guild (g)", "keybind_guild"),
            ("Battle Pass (F8)", "keybind_battle_pass"),
            ("Map (m)", "keybind_map"),
            ("Content Notifications (n)", "keybind_questlog"),
        ]
        for label_text, option_key in bindings:
            row = create_keybinding_entry(
                self.frame,
                self.options,
                self.widgets,
                label_text + ":",
                option_key,
                row,
            )

        # Separator: "Shortcuts - Shortcuts" section header
        sep_label = ttk.Label(
            self.frame, text="Shortcuts - Shortcuts", font=SEPARATOR_FONT
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Create a key binding entry for each control
        # Each tuple contains: (Descriptive Label, Option Key)
        bindings = [
            ("Party Leader Target (t)", "keybind_party_leader_target"),
            ("Quick Slot 1 (1)", "keybind_quick_slot_1"),
            ("Quick Slot 2 (2)", "keybind_quick_slot_2"),
            ("Quick Slot 3 (3)", "keybind_quick_slot_3"),
            ("Quick Slot 4 (4)", "keybind_quick_slot_4"),
            ("Quick Slot 5 (5)", "keybind_quick_slot_5"),
            ("Quick Slot 6 (6)", "keybind_quick_slot_6"),
            ("Quick Slot 7 (7)", "keybind_quick_slot_7"),
            ("Quick Slot 8 (8)", "keybind_quick_slot_8"),
            ("Quick Slot 9 (9)", "keybind_quick_slot_9"),
            ("Quick Slot 10 (0)", "keybind_quick_slot_10"),
            ("Quick Slot 11 (-)", "keybind_quick_slot_11"),
            ("Quick Slot 12 (=)", "keybind_quick_slot_12"),
            ("Item Quick Slot 1 (F1)", "keybind_item_quick_slot_1"),
            ("Item Quick Slot 2 (F2)", "keybind_item_quick_slot_2"),
            ("Item Quick Slot 3 (F3)", "keybind_item_quick_slot_3"),
            ("Item Quick Slot 4 (F4)", "keybind_item_quick_slot_4"),
        ]
        for label_text, option_key in bindings:
            row = create_keybinding_entry(
                self.frame,
                self.options,
                self.widgets,
                label_text + ":",
                option_key,
                row,
            )

        # Separator: "Other (Can't be set)" section header
        sep_label = ttk.Label(
            self.frame,
            text="Other (Not set in game)",
            font=SEPARATOR_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Define a list of key binding entries:
        # Each tuple contains: (Descriptive Label, Option Key)
        bindings = [
            ("Accept (y)", "keybind_accept"),
        ]

        # Create a key binding entry for each control
        for label_text, option_key in bindings:
            row = create_keybinding_entry(
                self.frame,
                self.options,
                self.widgets,
                label_text + ":",
                option_key,
                row,
            )

        # Ensure that the second column expands properly
        self.frame.columnconfigure(1, weight=1)
