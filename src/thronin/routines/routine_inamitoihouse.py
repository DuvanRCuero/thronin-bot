import time
from thronin.routines._base import Routine
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.global_variables.temp import temp


class InAmitoiHouseRoutine(Routine):
    def __init__(self):
        super().__init__("in_amitoi_house")
        self._required_trackers = []
        self.pretty_name = "Amitoi House"

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()

        # Start routine
        self._exit_amitoi_house()
        self._complete_routine(next_routine=None)


in_amitoi_house = InAmitoiHouseRoutine()
