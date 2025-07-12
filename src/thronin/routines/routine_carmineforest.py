from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.routines._base import Routine
import time
from pynput.keyboard import Key


class CarmineForestRoutine(Routine):
    def __init__(self):
        super().__init__("carmine_forest")
        self._required_trackers = []
        self.pretty_name = "Carmine Forest"
        self.search_name = "carmine"
        self.map_tp_coords = {
            720: [667, 333],
            1080: [1007, 494],
        }

    def run(self):
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        x, y = self.map_tp_coords.get(temp.get("window_size"), [0, 0])
        if not self._teleport(self.pretty_name, self.search_name, x, y):
            self._complete_routine(next_routine=None)
            return
        temp.raise_if_killswitch_engaged()
        kbm.reset_camera()
        temp.raise_if_killswitch_engaged()
        self._get_positioned()
        self._complete_routine(next_routine="battle")

    def _get_positioned(self):
        temp.set("action_log", "Getting Positioned")
        kbm.use_keyboard(Key.right, press_time=0.8, post_time=0.25)
        kbm.run_and_jump(10)


carmine_forest = CarmineForestRoutine()
