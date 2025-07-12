from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.routines._base import Routine
import time
from pynput.keyboard import Key


class InMenuRoutine(Routine):
    def __init__(self):
        super().__init__("in_menu")
        self._required_trackers = []

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Closing the menu")
        kbm.use_keyboard(Key.esc, post_time=5)
        self._complete_routine(next_routine=None)


in_menu = InMenuRoutine()
