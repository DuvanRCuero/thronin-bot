from pynput.keyboard import Key, KeyCode
from thronin.gui.tab_configs.keyboard_layouts.azerty import AZERTY_KEYBINDS
from thronin.gui.tab_configs.keyboard_layouts.qwerty import QWERTY_KEYBINDS
from thronin.gui.tab_configs.keyboard_layouts.qwertz import QWERTZ_KEYBINDS
from thronin.lib.application_info import cache_path
from thronin.lib.logger import logger
import json
import os
import threading


class Options:
    DEFAULTS = {
        # General Tab
        "force_routine": None,
        "kb_layout": "QWERTY",
        # Player Tab
        "player_percent_to_use_companion": 0.2,
        "player_percent_to_use_health_recovery_skills": 0.85,
        "player_percent_to_use_health_potion": 0.35,
        "player_percent_to_use_mana_recovery_skills": 0.5,
        "player_percent_to_use_mana_potion": 0.1,
        "quickslot1_monitored_by_bot": True,
        "quickslot1_casting_skill": False,
        "quickslot1_type": "Combat",
        "quickslot1_repetitions": 1,
        "quickslot2_monitored_by_bot": True,
        "quickslot2_casting_skill": False,
        "quickslot2_type": "Combat",
        "quickslot2_repetitions": 1,
        "quickslot3_monitored_by_bot": True,
        "quickslot3_casting_skill": False,
        "quickslot3_type": "Combat",
        "quickslot3_repetitions": 1,
        "quickslot4_monitored_by_bot": True,
        "quickslot4_casting_skill": False,
        "quickslot4_type": "Combat",
        "quickslot4_repetitions": 1,
        "quickslot5_monitored_by_bot": True,
        "quickslot5_casting_skill": False,
        "quickslot5_type": "Combat",
        "quickslot5_repetitions": 1,
        "quickslot6_monitored_by_bot": True,
        "quickslot6_casting_skill": False,
        "quickslot6_type": "Combat",
        "quickslot6_repetitions": 1,
        "quickslot7_monitored_by_bot": True,
        "quickslot7_casting_skill": False,
        "quickslot7_type": "Combat",
        "quickslot7_repetitions": 1,
        "quickslot8_monitored_by_bot": True,
        "quickslot8_casting_skill": False,
        "quickslot8_type": "Combat",
        "quickslot8_repetitions": 1,
        "quickslot9_monitored_by_bot": True,
        "quickslot9_casting_skill": False,
        "quickslot9_type": "Combat",
        "quickslot9_repetitions": 1,
        "quickslot10_monitored_by_bot": True,
        "quickslot10_casting_skill": False,
        "quickslot10_type": "Combat",
        "quickslot10_repetitions": 1,
        "quickslot11_monitored_by_bot": True,
        "quickslot11_casting_skill": False,
        "quickslot11_type": "Combat",
        "quickslot11_repetitions": 1,
        "quickslot12_monitored_by_bot": True,
        "quickslot12_casting_skill": False,
        "quickslot12_type": "Combat",
        "quickslot12_repetitions": 1,
        # Safe Zone Tab
        "perform_amitoi": True,
        "perform_battle_pass": True,
        "perform_battle_pass_every": int(3600),  # 1 hour
        "perform_guild_collection": False,
        "perform_guild_collection_every": int(3600),  # 1 hour
        "donate_on_guild_collection": False,
        "perform_guild_recruitment": False,
        "perform_guild_recruitment_every": int(43200),  # 12 hours
        "guild_recruitment_message": str(""),
        "perform_kastleton": False,
        "perform_kastleton_every": int(7200),  # 2 hours
        "perform_stonegard": False,
        "perform_stonegard_every": int(43200),  # 12 hours
        ## contract-coin-merchant
        "purchase_fishing-bait": True,
        "purchase_mystic-key": True,
        "purchase_trait-extraction-stone": True,
        ## sundries-merchant
        "purchase_egg": True,
        "purchase_golden-rye": True,
        "purchase_honey": True,
        ## guild-merchant
        "purchase_trait-conversion-stone": True,
        "purchase_precious-polished-crystal": True,
        "purchase_rare-polished-crystal": True,
        "purchase_precious-base-material-selection-chest": True,
        "purchase_rare-base-material-selection-chest": True,
        "purchase_rare-recovery-crystal": True,
        "purchase_quality-recovery-crystal": False,
        "purchase_mana-regen-potion": False,
        # Farming Tab
        "perform_safe_zone_every": int(1800),  # 30 minutes
        "use_itemquickslot3_every": int(0),  # 0 to disable
        "use_itemquickslot4_every": int(0),  # 0 to disable
        "farm_canina_village": True,
        "drop_contract_when_none_available": True,
        "farm_blackhowl_plains": False,
        "farm_urstella_fields": False,
        "farm_carmine_forest": False,
        "farm_nesting_grounds": False,
        "farm_fonos_basin": False,
        "farm_ruins_of_turayne": False,
        "farm_purelight_hills": False,
        "farm_shattered_temple": False,
        "farm_monolith_wastelands": False,
        "farm_abandoned_stonemason_town": False,
        "farm_moonlight_desert": False,
        "farm_daybreak_shore": False,
        "farm_raging_wilds": False,
        "farm_manawastes": False,
        "farm_akidu_valley": False,
        "farm_grayclaw_forest": False,
        "farm_quietiss_demense": False,
        "farm_forest_of_the_great_tree": False,
        "farm_swamp_of_silence": False,
        "farm_black_anvil": False,
        "farm_bercant_manor": False,
    }
    # Merge layout-specific keybinds into the defaults
    DEFAULTS = {**DEFAULTS, **QWERTY_KEYBINDS}

    def __init__(self):
        self._options = {}
        self.lock = threading.Lock()
        self.file_path = os.path.join(cache_path, "options.json")
        self._load_from_file()

    def set(self, key, value):
        """Set an option."""
        with self.lock:
            if key in self._options:
                if value == "None":
                    value = None
                self._options[key] = value
                logger.debug(f"Set {key} to {type(value)}({value})")
            else:
                logger.error(f"{key} is not a valid option")
                raise KeyError(f"{key} is not a valid option")

    def get(self, key, default=None):
        """Get an option value."""
        with self.lock:
            return self._options.get(key, default)

    def reset_to_defaults(self):
        """Reset all options to default values."""
        with self.lock:
            self._options = self.DEFAULTS.copy()
            logger.debug("Options reset to default values.")

    def get_default_options(self):
        """Return default options."""
        return self.DEFAULTS

    #######################################################################################################################
    # FILE FUNCTIONS
    #######################################################################################################################
    def _load_from_file(self):
        """Load saved options from file or set defaults if missing."""
        with self.lock:
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r") as f:
                        loaded_options = json.load(f)
                        self._options.update(loaded_options)
                        logger.info("Previous options loaded successfully.")
                except (json.JSONDecodeError, IOError) as e:
                    logger.error(f"Error loading options from file: {e}")
            else:
                logger.debug(f"{self.file_path} not found. Using default options.")

            # Add any missing default options
            missing_defaults = {
                key: value
                for key, value in self.DEFAULTS.items()
                if key not in self._options
            }
            if missing_defaults:
                self._options.update(missing_defaults)
            logger.debug(f"Options Loaded: {self._options}")

    def save_to_file(self):
        """Save options to a file."""
        try:
            with open(self.file_path, "w") as f:
                json.dump(self._options, f, indent=4)
            logger.debug(f"Options saved successfully: {self.file_path}")
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error saving options: {e}")

    #######################################################################################################################
    # KEYBINDS
    #######################################################################################################################
    def get_keybind_key(self, key_name):
        key = self.get_keybind(key_name)["key"]
        logger.debug(f"Returning '{key}' for '{key_name}")
        return key

    def get_keybind(self, key_name):
        """
        Get a keybind and return an object containing a display name and the actual Key or KeyCode object.

        Args:
            key_name (str): The keybinding name to load.

        Returns:
            dict: {
                "display": str,  # Pretty name for UI
                "key": Key or KeyCode  # Actual pynput Key object
            }
        """
        with self.lock:
            key_data = self._options.get(key_name)
            # logger.debug(f"Key Data for {key_name}: {key_data}")

            if not key_data:
                raise ValueError(f"No keybind found for {key_name}")

            # Ensure data structure is correct
            if isinstance(key_data, str):
                raise ValueError(
                    f"Invalid format for {key_name}, expected dict but got string."
                )

            key_str = key_data.get("key", "")
            display_name = key_data.get("display", "Unknown Key")
            key_obj = None

            # Convert back to `Key` or `KeyCode`
            if key_str.startswith("special:"):
                special_key = key_str.split(":")[1]
                key_obj = getattr(Key, special_key, None)
            elif key_str.startswith("keycode:"):
                try:
                    vk_code = int(key_str.split(":")[1])
                    key_obj = KeyCode.from_vk(vk_code)
                except ValueError:
                    logger.error(f"Invalid keycode format: {key_str}")
            elif key_str.startswith("char:"):
                char = key_str.split(":")[1]
                key_obj = KeyCode.from_char(char)

            if not key_obj:
                raise ValueError(f"Invalid keybind format: {key_str}")

            return_obj = {"display": display_name, "key": key_obj}
            # logger.debug(f"Returning '{return_obj}' for '{key_name}")
            return return_obj

    def set_keybind(self, key_name, key, display_name=None):
        """
        Set a keybind. Saves an object containing a display name and the actual Key or KeyCode object.

        Args:
            key_name (str): The name of the keybinding.
            key (Key or KeyCode): The key to save.
            display_name (str, optional): A custom display name for UI. Defaults to None.
        """
        with self.lock:
            key_str = None

            # Determine key type and format storage
            if isinstance(key, Key):  # Special keys (e.g., Home, Insert)
                key_str = f"special:{key.name}"
                default_display = key.name.replace(
                    "_", " "
                ).title()  # e.g., 'space' → 'Space'
            elif isinstance(key, KeyCode):  # Regular keys (e.g., 'A', '1')
                if key.char:
                    key_str = f"char:{key.char}"
                    default_display = key.char.upper()
                else:
                    key_str = f"keycode:{key.vk}"
                    default_display = (
                        chr(key.vk) if 32 <= key.vk <= 126 else f"KeyCode({key.vk})"
                    )
            else:
                logger.error(f"Unsupported key type for {key_name}: {key}")
                return

            # Use the provided display name or fallback to the default generated one
            display_name = display_name if display_name else default_display

            # Save the keybind as an object
            self._options[key_name] = {
                "display": display_name,
                "key": key_str,  # Stores serialized key string
            }

            logger.debug(f"Set keybind {key_name}: {self._options[key_name]}")

    def set_default_keybinds(self, layout: str):
        deafult_keybind_layouts = {
            "QWERTY": QWERTY_KEYBINDS,
            "QWERTZ": QWERTZ_KEYBINDS,
            "AZERTY": AZERTY_KEYBINDS,
        }
        selected_layout = deafult_keybind_layouts.get(layout.upper())
        if not selected_layout:
            raise ValueError(f"Selected layout '{layout}' not found.")

        # Iterate through the keybindings and update options via set_keybind.
        for option_key, binding in selected_layout.items():
            self.set(option_key, binding)


#######################################################################################################################
# CREATE INSTANCE
#######################################################################################################################
options = Options()
