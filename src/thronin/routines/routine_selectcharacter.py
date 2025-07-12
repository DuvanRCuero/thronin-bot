import time
from thronin.routines._base import Routine
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm


class SelectCharacterRoutine(Routine):
    def __init__(self):
        super().__init__("select_character")
        self._required_trackers = []

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Entering Game")
        if temp.get("window_size") == 720:
            kbm.move_mouse(640, 662, click=True)  # Click Enter Button
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(922, 978, click=True)  # Click Enter Button
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        temp.raise_if_killswitch_engaged()
        time.sleep(15)  # Wait for screen to progress
        self._complete_routine(next_routine=None)


select_character = SelectCharacterRoutine()
