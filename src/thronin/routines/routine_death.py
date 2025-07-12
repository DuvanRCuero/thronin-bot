from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.lib.player import player
from thronin.routines._base import Routine
from thronin.trackers.health import health
from thronin.trackers.mana import mana
from thronin.utils.screenshot import screenshot_utils
import time


class DeathRoutine(Routine):
    def __init__(self):
        super().__init__("death")
        self._required_trackers = [  # THIS IS THE UPDATED LIST
            # "amitoi",
            # "bobber",
            "casting",
            # "death",
            # "fish_on_line",
            # "fishing_pole_casted",
            # "fishing_pole_equipped",
            "health",
            # "line_of_sight",
            "mana",
            # "need_to_block",
            # "party",
            # "party_invite",
            # "pvp_z",
            "quickslot1",
            "quickslot2",
            "quickslot3",
            "quickslot4",
            "quickslot5",
            "quickslot6",
            "quickslot7",
            "quickslot8",
            "quickslot9",
            "quickslot10",
            "quickslot11",
            "quickslot12",
            "itemquickslot1",
            "itemquickslot2",
            "itemquickslot3",
            "itemquickslot4",
            # "resources_nearby",
            # "target",
        ]

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()

        # Save Screenshot
        screenshot_utils.save_screenshot("death")
        time.sleep(1)
        temp.raise_if_killswitch_engaged()

        # Perform resurrection actions
        temp.set("action_log", f"Resurrecting")
        if temp.get("window_size") == 720:
            kbm.move_mouse(588, 656, click=True)  # Click Resurrection Button
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(960, 975, click=True)  # Click Resurrection Button
        kbm.reset_mouse()
        temp.raise_if_killswitch_engaged()
        time.sleep(10)  # Wait for resurrection to finish
        temp.raise_if_killswitch_engaged()

        # Fix health and mana
        temp.set("action_log", f"Fixing Health and Mana")
        player.use_health_recovery_skills_if_needed()
        player.use_mana_recovery_skills_if_needed()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()

        # Wait for combat to wear off
        temp.set("action_log", f"Waiting for combat to wear off")
        time.sleep(15)
        temp.raise_if_killswitch_engaged()

        self._complete_routine(next_routine=None)


death = DeathRoutine()
