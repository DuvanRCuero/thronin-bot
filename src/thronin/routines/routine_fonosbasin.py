import time
from thronin.routines._base import Routine
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from pynput.keyboard import Key


class FonosBasinRoutine(Routine):
    def __init__(self):
        super().__init__("fonos_basin")
        self._required_trackers = []
        self.pretty_name = "Fonos Basin"
        self.search_name = "fonos"
        self.map_tp_coords = {
            720: [697, 382],
            1080: [1061, 579],
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
        kbm.use_keyboard(Key.left, press_time=0.82, post_time=0.25)
        kbm.run_and_jump(25)
        # kbm.use_keyboard(options.get_keybind_key("keybind_move_backward"), press_time=2)


fonos_basin = FonosBasinRoutine()
