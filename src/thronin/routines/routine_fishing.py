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
            temp.set("action_log", "Waiting for Fish")
            logger.debug(f"Fish not on Line.")
            time.sleep(0.35)
            return True
        return False

    def _perform_reeling(self):
        self._center_x = int(temp.get("window_xywh")[2] / 2)
        self._bobber_x = bobber.get("last_bobber_x", self._center_x)
        need_to_reel = None

        # Calculate absolute difference
        difference = abs(self._center_x - self._bobber_x)
        # Cap the difference to max_difference
        max_difference = 100
        difference = min(difference, max_difference)

        # Calculate press_time
        min_press_time = 0.4
        max_press_time = 1
        press_time = min_press_time + (difference / max_difference) * (
            max_press_time - min_press_time
        )

        if self._bobber_x > self._center_x:
            logger.debug(
                f"Bobber ({self._bobber_x}) right of center ({self._center_x}), Difference: {difference}, Press Time: {press_time:.2f}"
            )
            need_to_reel = "left"
        elif self._bobber_x < self._center_x:
            logger.debug(
                f"Bobber ({self._bobber_x}) left of center ({self._center_x}), Difference: {difference}, Press Time: {press_time:.2f}"
            )
            need_to_reel = "right"
        else:
            logger.debug(f"Bobber ({self._bobber_x}) is center ({self._center_x})")

        # Perform keyboard actions
        if not need_to_reel:
            logger.debug("Skipping Reel")
            time.sleep(0.1)
            return
        if need_to_reel == "right":
            kb_button = options.get_keybind_key("keybind_move_right")
            temp.set("action_log", f"Reeling Right ({kb_button})")
        if need_to_reel == "left":
            kb_button = options.get_keybind_key("keybind_move_left")
            temp.set("action_log", f"Reeling Left ({kb_button})")
        kbm.use_keyboard(kb_button, press_time=press_time, post_time=0.2)


fishing = FishingRoutine()
