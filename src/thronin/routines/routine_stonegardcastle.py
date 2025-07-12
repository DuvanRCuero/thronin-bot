from thronin.global_variables.assets import assets
from thronin.global_variables.cache import cache
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.gui_manager import gui_manager
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.routines._base import Routine
import pyautogui
import time
from pynput.keyboard import Key


class StonegardCastleRoutine(Routine):
    def __init__(self):
        super().__init__("stonegard_castle")
        self._required_trackers = []
        self.pretty_name = "Stonegard Castle"
        self.search_name = "stonegard castle"
        self.map_tp_coords = {
            720: [633, 256],
            1080: [947, 357],
        }

    def run(self):
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        x, y = self.map_tp_coords.get(temp.get("window_size"), [0, 0])
        if not self._teleport(self.pretty_name, self.search_name, x, y):
            self._complete_routine(next_routine=None)
            return
        temp.raise_if_killswitch_engaged()
        self._get_positioned()
        self._complete_routine(next_routine=None)

    def _get_positioned(self):
        temp.set("action_log", f"Moving forward to merchants")
        kbm.use_keyboard(
            options.get_keybind_key("keybind_move_forward"), press_time=6.5
        )
        time.sleep(0.3)
        kbm.use_keyboard(Key.right, press_time=0.6)
        time.sleep(0.3)

        # Search and interact with Contract Coin Merchant
        if self._travel_to_vendor("contract-coin-merchant"):
            gui_manager.hide_overlay()
            time.sleep(1)
            self._select_item("fishing-bait")
            self._select_item("mystic-key")
            pyautogui.scroll(-1000)  # Scroll down to see other buy options
            self._select_item("trait-extraction-stone")
            self._purchase_items()
            kbm.use_keyboard(Key.esc)
            gui_manager.show_overlay()
            time.sleep(1)
        else:
            self._handle_vendor_not_found()
            return  # Restart the routine

        # Turn camera slightly
        temp.set("action_log", f"Turning Camera to reveal other merchants")
        kbm.use_keyboard(options.get_keybind_key("keybind_move_backward"), press_time=1)
        kbm.use_keyboard(Key.right, press_time=0.1)

        # Search and interact with Sundries Merchant
        if self._travel_to_vendor("sundries-merchant"):
            gui_manager.hide_overlay()
            time.sleep(1)
            self._select_item("egg")
            pyautogui.scroll(-1000)  # Scroll down to see other buy options
            self._select_item("golden-rye")
            self._select_item("honey")
            self._purchase_items()
            kbm.use_keyboard(Key.esc)
            gui_manager.show_overlay()
            time.sleep(1)
        else:
            self._handle_vendor_not_found()
            return  # Restart the routine

        # Turn camera slightly
        temp.set("action_log", f"Turning Camera to reveal other merchants")
        kbm.use_keyboard(options.get_keybind_key("keybind_move_backward"), press_time=2)
        kbm.use_keyboard(Key.right, press_time=0.2)

        # Search and interact with Guild Merchant
        if self._travel_to_vendor("guild-merchant"):
            gui_manager.hide_overlay()
            time.sleep(1)
            self._select_item("trait-conversion-stone")
            self._select_item("precious-polished-crystal")
            self._select_item("rare-polished-crystal")
            self._select_item("precious-base-material-selection-chest")
            self._select_item("rare-base-material-selection-chest")
            self._select_item("rare-recovery-crystal")
            self._select_item("quality-recovery-crystal")
            self._select_item("mana-regen-potion")
            self._purchase_items()
            kbm.use_keyboard(Key.esc)
            gui_manager.show_overlay()
            time.sleep(1)
        else:
            self._handle_vendor_not_found()
            return  # Restart the routine

        # Turn camera slightly
        temp.set("action_log", f"Turning Camera to reveal other merchants")
        kbm.use_keyboard(options.get_keybind_key("keybind_move_backward"), press_time=3)
        kbm.use_keyboard(Key.left, press_time=0.2)

        # Search and interact with Storage Manager
        if self._travel_to_vendor("storage-manager"):
            self._deposit_items()
            kbm.use_keyboard(Key.esc)
            time.sleep(1)
        else:
            self._handle_vendor_not_found()
            return  # Restart the routine

        # Save Last Run Time
        cache.set("last_run_stonegard", time.time())
        time.sleep(1)

    # HELPER FUNCTIONS
    def _select_item(self, item_name=None, shift_click=True):
        temp.set("action_log", f"Selecting {item_name}")

        if not item_name:
            logger.error("Item Name is required.")
            return False

        option_key = f"purchase_{item_name}"
        if options.get(option_key) == "No":
            logger.info(f"{item_name} was not wanted.")
            return False

        # Get the path for the chosen item
        chosen_item_path = assets.get("shopping", item_name)
        if not chosen_item_path:
            logger.error(f"No path found for item: {item_name}")
            return False

        # Attempt to find and click the target
        found = self._find_and_click_target(chosen_item_path, shift_click=shift_click)
        if not found:
            logger.error(f"{item_name} was not found.")
            return False

        logger.info(f"Found and selected {item_name}.")
        time.sleep(0.5)
        return True

    def _purchase_items(self):
        temp.set("action_log", f"Purchasing Items")
        if temp.get("window_size") == 720:
            kbm.move_mouse(1164, 674, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1746, 1019, click=True)
        time.sleep(1)


stonegard_castle = StonegardCastleRoutine()
