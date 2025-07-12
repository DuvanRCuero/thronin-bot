import time
from thronin.routines._base import Routine
from thronin.global_variables.temp import temp
from thronin.global_variables.options import options
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from pynput.keyboard import Key


class QuietissDemenseRoutine(Routine):
    def __init__(self):
        super().__init__("quietiss_demense")
        self._required_trackers = []
        self.pretty_name = "Quietis's Demense"
        self.search_name = "quietis"
        self.map_tp_coords = {
            720: [556, 313],
            1080: [814, 460],
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
            press_time=1.35,
            post_time=0.5,
        )
        temp.raise_if_killswitch_engaged()
        kbm.run_and_jump(8)


quietiss_demense = QuietissDemenseRoutine()
