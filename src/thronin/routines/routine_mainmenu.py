from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.routines._base import Routine
import time


class MainMenuRoutine(Routine):
    def __init__(self):
        super().__init__("main_menu")
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
        # Pressing Y in case we have a return menu from crashing. Otherwise this does nothing.
        time.sleep(2)
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"))
        time.sleep(10)  # Wait for screen to progress
        self._complete_routine(next_routine=None)


main_menu = MainMenuRoutine()
