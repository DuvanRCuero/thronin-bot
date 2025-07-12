import tkinter as tk
from tkinter import ttk
from thronin.gui.widget_helpers import (
    create_entry,
    create_checkbox,
    create_textbox,
    create_scrollable_frame,
)
from thronin.gui.gui_config import SEPARATOR_FONT, HEADER_FONT


class SafeZone:
    def __init__(self, parent, options, widgets):
        self.tab_name = "Safe Zone"
        self.parent = parent
        self.options = options
        self.widgets = widgets
        self.build_ui()

    def build_ui(self):
        # Create a canvas and vertical scrollbar to allow scrolling of tab content
        self.frame, canvas = create_scrollable_frame(self.parent)
        row = 0

        # Separator: "Safe Zone" section
        sep_label = ttk.Label(self.frame, text="Safe Zone", font=SEPARATOR_FONT)
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Perform Amitoi Collection
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Amitoi Collection",
            option_key="perform_amitoi",
            row=row,
        )

        # Perform Battle Pass
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Battle Pass",
            option_key="perform_battle_pass",
            row=row,
        )

        # Perform Battle Pass Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Battle Pass Every (seconds)",
            option_key="perform_battle_pass_every",
            row=row,
        )

        # Perform Guild Collection
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Guild Collection",
            option_key="perform_guild_collection",
            row=row,
        )

        # Perform Guild Collection Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Guild Collection Every (seconds)",
            option_key="perform_guild_collection_every",
            row=row,
        )

        # Donate on Guild Collection
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Donate on Guild Collection",
            option_key="donate_on_guild_collection",
            row=row,
        )

        # Perform Kastleton
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Kastleton",
            option_key="perform_kastleton",
            row=row,
        )

        # Perform Kastleton Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Kastleton Every (seconds)",
            option_key="perform_kastleton_every",
            row=row,
        )

        # Separator: "Guild Recruitment" section
        sep_label = ttk.Label(self.frame, text="Guild Recruitment", font=SEPARATOR_FONT)
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Perform Guild Recruitment
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Guild Recruitment",
            option_key="perform_guild_recruitment",
            row=row,
        )

        # Perform Guild Recruitment Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Guild Recruitment Every (seconds)",
            option_key="perform_guild_recruitment_every",
            row=row,
        )

        # Guild Recruitment Message (using textbox helper)
        row = create_textbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Guild Recruitment Message",
            option_key="guild_recruitment_message",
            row=row,
        )

        # Separator: "Stonegard Castle (Shopping)" section
        sep_label = ttk.Label(
            self.frame,
            text="Stonegard Castle (Shopping)",
            font=SEPARATOR_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Perform Stonegard Castle
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Stonegard Castle",
            option_key="perform_stonegard",
            row=row,
        )

        # Perform Stonegard Castle Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Perform Stonegard Castle Every (seconds)",
            option_key="perform_stonegard_every",
            row=row,
        )

        # Separator: "Contract Coin Merchant" section
        sep_label = ttk.Label(
            self.frame,
            text="Contract Coin Merchant",
            font=HEADER_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Contract Coin Merchant
        config = [
            ("Purchase Fishing Bait", "purchase_fishing-bait"),
            ("Purchase Mystic Key", "purchase_mystic-key"),
            ("Purchase Trait Extraction Stone", "purchase_trait-extraction-stone"),
        ]
        for label_text, key in config:
            row = create_checkbox(
                self.frame,
                self.options,
                self.widgets,
                label_text=label_text,
                option_key=key,
                row=row,
            )

        # Separator: "Sundries Merchant" section
        sep_label = ttk.Label(
            self.frame,
            text="Sundries Merchant",
            font=HEADER_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Sundries Merchant
        config = [
            ("Purchase Egg", "purchase_egg"),
            ("Purchase Golden Rye", "purchase_golden-rye"),
            ("Purchase Honey", "purchase_honey"),
        ]
        for label_text, key in config:
            row = create_checkbox(
                self.frame,
                self.options,
                self.widgets,
                label_text=label_text,
                option_key=key,
                row=row,
            )

        # Separator: "Guild Merchant" section
        sep_label = ttk.Label(
            self.frame,
            text="Guild Merchant",
            font=HEADER_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Guild Merchant
        config = [
            ("Purchase Trait Conversion Stone", "purchase_trait-conversion-stone"),
            (
                "Purchase Precious Polished Crystal",
                "purchase_precious-polished-crystal",
            ),
            ("Purchase Rare Polished Crystal", "purchase_rare-polished-crystal"),
            (
                "Purchase Precious Base Material Selection Chest",
                "purchase_precious-base-material-selection-chest",
            ),
            (
                "Purchase Rare Base Material Selection Chest",
                "purchase_rare-base-material-selection-chest",
            ),
            ("Purchase Rare Recovery Crystal", "purchase_rare-recovery-crystal"),
            ("Purchase Quality Recovery Crystal", "purchase_quality-recovery-crystal"),
            ("Purchase Mana Regen Potion", "purchase_mana-regen-potion"),
        ]
        for label_text, key in config:
            row = create_checkbox(
                self.frame,
                self.options,
                self.widgets,
                label_text=label_text,
                option_key=key,
                row=row,
            )

        # Ensure that the second column expands properly
        self.frame.columnconfigure(1, weight=1)
