import time
from thronin.routines._base import Routine
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm


class UrstellaFieldsRoutine(Routine):
    def __init__(self):
        super().__init__("urstella_fields")
        self._required_trackers = []
        self.pretty_name = "Urstella Fields"
        self.search_name = "urstella"
        self.map_tp_coords = {
            720: [515, 369],
            1080: [741, 556],
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
        kbm.run_and_jump(5)


urstella_fields = UrstellaFieldsRoutine()
