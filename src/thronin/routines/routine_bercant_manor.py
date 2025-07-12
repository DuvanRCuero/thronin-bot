import time
from thronin.routines._base import Routine
from thronin.global_variables.temp import temp
from thronin.global_variables.options import options
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from pynput.keyboard import Key


class BercantManorRoutine(Routine):
    def __init__(self):
        super().__init__("bercant_manor")
        self._required_trackers = []
        self.pretty_name = "Bercant Manor"
        self.search_name = "bercant manor"
        self.map_tp_coords = {
            720: [701, 445],
            1080: [1067, 692],
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
        kbm.use_keyboard(
            Key.right,
            press_time=0.1,
            post_time=0.5,
        )
        temp.raise_if_killswitch_engaged()
        kbm.run_and_jump(8)


bercant_manor = BercantManorRoutine()
