import tkinter as tk
from tkinter import ttk
from thronin.gui.widget_helpers import (
    create_entry,
    create_checkbox,
    create_scrollable_frame,
)
from thronin.gui.gui_config import SEPARATOR_FONT


class Farming:
    def __init__(self, parent, options, widgets):
        self.tab_name = "Farming"
        self.parent = parent
        self.options = options
        self.widgets = widgets
        self.build_ui()

    def build_ui(self):
        # Create a canvas and vertical scrollbar to allow scrolling of tab content
        self.frame, canvas = create_scrollable_frame(self.parent)
        row = 0

        # Separator: "Farming Options" section
        sep_label = ttk.Label(self.frame, text="Farming Options", font=SEPARATOR_FONT)
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Return to Safe Zone Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Return to Safe Zone Every (seconds)",
            option_key="perform_safe_zone_every",
            row=row,
        )

        # Use Item Quick Slot 3 Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Use Item Quick Slot 3 Every (seconds)",
            option_key="use_itemquickslot3_every",
            row=row,
        )

        # Use Item Quick Slot 4 Every (seconds)
        row = create_entry(
            self.frame,
            self.options,
            self.widgets,
            label_text="Use Item Quick Slot 4 Every (seconds)",
            option_key="use_itemquickslot4_every",
            row=row,
        )

        # Separator: "Contracts Locations" section
        sep_label = ttk.Label(
            self.frame,
            text="Contracts Locations",
            font=SEPARATOR_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Contracts Locations
        config = [
            ("Canina Village", "farm_canina_village"),
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

        # Drop Contract When None Available
        row = create_checkbox(
            self.frame,
            self.options,
            self.widgets,
            label_text="Drop Contract When None Available",
            option_key="drop_contract_when_none_available",
            row=row,
        )

        # Separator: "Laslan Region" section
        sep_label = ttk.Label(
            self.frame,
            text="Laslan Region",
            font=SEPARATOR_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Laslan Region
        config = [
            (
                "Farm Blackhowl Plains (8-11)",
                "farm_blackhowl_plains",
            ),
            (
                "Farm Urstella Fields (12-16)",
                "farm_urstella_fields",
            ),
            (
                "Farm Carmine Forest (17-19)",
                "farm_carmine_forest",
            ),
            (
                "Farm Nesting Grounds (20-23)",
                "farm_nesting_grounds",
            ),
            (
                "Farm Fonos Basin (50)",
                "farm_fonos_basin",
            ),
            (
                "Farm Ruins of Turayne (50)",
                "farm_ruins_of_turayne",
            ),
            (
                "Farm Purelight Hills (50)",
                "farm_purelight_hills",
            ),
            (
                "Farm Shattered Temple (50)",
                "farm_shattered_temple",
            ),
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

        # Separator: "Stonegard Region" section
        sep_label = ttk.Label(
            self.frame,
            text="Stonegard Region",
            font=SEPARATOR_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Stonegard Region
        config = [
            (
                "Farm Monolith Wastelands (24-27)",
                "farm_monolith_wastelands",
            ),
            (
                "Farm Abandoned Stonemason Town (28-31)",
                "farm_abandoned_stonemason_town",
            ),
            (
                "Farm Moonlight Desert (32-34)",
                "farm_moonlight_desert",
            ),
            (
                "Farm Daybreak Shore (38-40)",
                "farm_daybreak_shore",
            ),
            (
                "Farm Raging Wilds (41-42)",
                "farm_raging_wilds",
            ),
            (
                "Farm Manawastes (43-45)",
                "farm_manawastes",
            ),
            (
                "Farm Akidu Valley (46-49)",
                "farm_akidu_valley",
            ),
            (
                "Farm Grayclaw Forest (50)",
                "farm_grayclaw_forest",
            ),
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
        # Separator: "Talandre Region" section
        sep_label = ttk.Label(
            self.frame,
            text="Talandre Region",
            font=SEPARATOR_FONT,
        )
        sep_label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 2))
        row += 1

        # Specifications for Talandre Region
        config = [
            (
                "Farm Quietis's Demense (51)",
                "farm_quietiss_demense",
            ),
            (
                "Farm Forest of the Great Tree (52)",
                "farm_forest_of_the_great_tree",
            ),
            (
                "Farm Swamp of Silence (53)",
                "farm_swamp_of_silence",
            ),
            (
                "Farm Black Anvil (54)",
                "farm_black_anvil",
            ),
            (
                "Farm Bercant Manor (55)",
                "farm_bercant_manor",
            ),
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
