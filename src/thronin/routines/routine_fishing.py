from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.routines._base import Routine
from thronin.trackers.bobber import bobber
from thronin.trackers.fish_on_line import fish_on_line
from thronin.trackers.fishing_pole_casted import fishing_pole_casted
from thronin.trackers.fishing_pole_equipped import fishing_pole_equipped
import time
from pynput.keyboard import Key


class FishingRoutine(Routine):
    def __init__(self):
        super().__init__("fishing")
        self._required_trackers = [
            "bobber",
            "fish_on_line",
            "fishing_pole_casted",
            "fishing_pole_equipped",
        ]
        self._last_seen_bobber_coords = None
        self._first_run = True
        self._last_reel_direction = None
        self._fish_not_on_line_count = 0

    def run(self):
        temp.raise_if_killswitch_engaged()
        if self._handle_fishing_pole_not_equipped():
            return
        temp.raise_if_killswitch_engaged()
        if self._handle_fishing_pole_not_casted():
            return
        temp.raise_if_killswitch_engaged()
        if self._handle_fish_not_on_line():
            return
        temp.raise_if_killswitch_engaged()
        logger.debug(f"Fish on Line!")
        self._perform_reeling()

    def _handle_fishing_pole_not_equipped(self):
        if not fishing_pole_equipped.get("ready"):
            temp.set("action_log", "Equipping Fishing Pole")
            kbm.use_keyboard(
                options.get_keybind_key("keybind_interact"),
                post_time=3,
                modifier=Key.ctrl,
            )
            return True
        return False

    def _handle_fishing_pole_not_casted(self):
        if not fishing_pole_casted.get("ready"):
            temp.set("action_log", "Casting Fishing Pole")
            kbm.use_keyboard(
                options.get_keybind_key("keybind_interact"), press_time=0.5, post_time=3
            )
            return True
        return False

    def _handle_fish_not_on_line(self):
        if not fish_on_line.get("ready"):
            self._fish_not_on_line_count += 1
            logger.debug(f"Fish not on Line (count: {self._fish_not_on_line_count}).")
            if self._fish_not_on_line_count <= 3:
                # Debounce: the tracker pixel can flicker when the fish energy bar is
                # nearly empty — keep reeling for a few more cycles before giving up.
                time.sleep(0.35)
                return False
            temp.set("action_log", "Waiting for Fish")
            time.sleep(0.35)
            return True
        self._fish_not_on_line_count = 0
        return False

    def _get_direction(self, bobber_x, center_x):
        if bobber_x > center_x:
            return "left"
        elif bobber_x < center_x:
            return "right"
        return self._last_reel_direction or "left"

    def _get_key(self, direction):
        if direction == "right":
            return options.get_keybind_key("keybind_move_right")
        return options.get_keybind_key("keybind_move_left")

    def _perform_reeling(self):
        center_x = int(temp.get("window_xywh")[2] / 2)
        bobber_x = bobber.get("last_bobber_x", center_x)

        difference = min(abs(center_x - bobber_x), 100)
        press_time = 0.4 + (difference / 100) * 0.6

        direction = self._get_direction(bobber_x, center_x)
        self._last_reel_direction = direction
        kb_button = self._get_key(direction)

        logger.debug(
            f"Bobber ({bobber_x}) vs center ({center_x}), Difference: {difference}, Press Time: {press_time:.2f}, Direction: {direction}"
        )
        temp.set("action_log", f"Reeling {direction.capitalize()} ({kb_button})")
        kbm.use_keyboard(kb_button, press_time=press_time, post_time=0.2)


fishing = FishingRoutine()
