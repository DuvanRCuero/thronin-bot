from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.routines._base import Routine
from thronin.utils.screenshot import screenshot_utils
import time


class KickedRoutine(Routine):

    def __init__(self):
        super().__init__("kicked")
        self._required_trackers = []

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Taking a screenshot")
        screenshot_utils.save_screenshot("kicked")
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"))
        temp.set("action_log", "Waiting for game to close")
        time.sleep(15)  # Wait for game to close.
        self._complete_routine(next_routine=None)


kicked = KickedRoutine()
