from pynput.keyboard import Key
from thronin.global_variables.cache import cache
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.routines._base import Routine
import time


class KastletonRoutine(Routine):
    def __init__(self):
        super().__init__("kastleton")
        self._required_trackers = []
        self.pretty_name = "Kastleton"
        self.search_name = "kastleton"
        self.map_tp_coords = {
            720: [711, 372],
            1080: [1084, 561],
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
        kbm.use_keyboard(Key.right, press_time=1)

        # Search and interact with Storage Manager
        if self._travel_to_vendor("storage-manager"):
            self._deposit_items()
            kbm.use_keyboard(Key.esc)
            time.sleep(0.5)
        else:
            self._handle_vendor_not_found()
            return

        # Save Last Run Time
        cache.set("last_run_kastleton", time.time())
        time.sleep(1)


kastleton = KastletonRoutine()
