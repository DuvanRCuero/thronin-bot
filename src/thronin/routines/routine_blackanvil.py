import time
from thronin.routines._base import Routine
from thronin.global_variables.temp import temp
from thronin.global_variables.options import options
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from pynput.keyboard import Key


class BlackAnvilRoutine(Routine):
    def __init__(self):
        super().__init__("black_anvil")
        self._required_trackers = []
        self.pretty_name = "Black Anvil"
        self.search_name = "black anvil"
        self.map_tp_coords = {
            720: [458, 528],
            1080: [642, 834],
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
            Key.left,
            press_time=0.25,
            post_time=0.5,
        )
        kbm.run_and_jump(14)
        kbm.use_keyboard(
            options.get_keybind_key("keybind_move_backward"),
            press_time=2,
            post_time=0.5,
        )


black_anvil = BlackAnvilRoutine()
