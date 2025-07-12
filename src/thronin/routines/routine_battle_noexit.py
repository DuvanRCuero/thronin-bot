from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.lib.player import player
from thronin.routines._base import Routine
from thronin.trackers.amitoi import amitoi
from thronin.trackers.health import health
from thronin.trackers.resources_nearby import resources_nearby
from thronin.trackers.target import target
import time
from pynput.keyboard import Key


class BattleNoExit(Routine):
    def __init__(self):
        super().__init__("battle_noexit")
        self.pretty_name = "Battle (No Exit)"
        # self._required_trackers = ["*"]
        self._required_trackers = [  # THIS IS THE UPDATED LIST
            # "amitoi",
            # "bobber",
            "casting",
            # "death",
            # "fish_on_line",
            # "fishing_pole_casted",
            # "fishing_pole_equipped",
            "health",
            "line_of_sight",
            "mana",
            "need_to_block",
            # "party",
            # "party_invite",
            "pvp_z",
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
            "resources_nearby",
            "target",
        ]

    def run(self):
        temp.raise_if_killswitch_engaged()
        if self._handle_precombat():
            return
        in_combat = target.get("ready")
        temp.raise_if_killswitch_engaged()
        if in_combat:
            self._handle_in_combat()
        else:
            self._handle_not_in_combat()

    def _handle_precombat(self):
        temp.raise_if_killswitch_engaged()
        # Returns True if needs to exit early. Else False.
        # Check immediate actions.
        player.counterattack_if_needed()
        temp.raise_if_killswitch_engaged()
        if player.block_if_needed():
            temp.set("cycles_without_target", 0)
            return True

        temp.raise_if_killswitch_engaged()
        player.use_health_recovery_skills_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_itemquickslot3_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_itemquickslot4_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_astral_vision_if_no_los()
        return False

    def _handle_in_combat(self):
        temp.raise_if_killswitch_engaged()
        # Reset variables
        temp.set("cycles_without_target", 0)
        temp.set("action_log", "IN COMBAT!")
        player.use_health_potion_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_companion_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_mana_recovery_skills_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_mana_potion_if_needed()
        # Check Line of Sight
        temp.raise_if_killswitch_engaged()
        if player.reset_los():
            cycles_without_los = temp.get("cycles_without_los")
            temp.set("cycles_without_los", (cycles_without_los + 1))
            return
        # Perform Combat
        temp.raise_if_killswitch_engaged()
        temp.set("cycles_without_los", 0)
        player.perform_combat()

    def _handle_not_in_combat(self):
        # Reset variables
        cycles_without_target = temp.get("cycles_without_target")
        temp.set("cycles_without_los", 0)
        temp.set("action_log", "NOT IN COMBAT!")

        # Press tab to check for target.
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Pressing tab to check for target")
        kbm.use_keyboard(Key.tab, post_time=0.25)

        # if >0: check for resources or stonegard, if yes perform another loop. if no look for trouble.
        temp.raise_if_killswitch_engaged()
        if cycles_without_target > 0:
            # Perform resource gathering if applicable.
            if resources_nearby.get("ready"):
                self._handle_resource_gathering(resources_nearby)
                return

            # Look for trouble.
            if health.get("percentage") <= 0.5:
                temp.set("action_log", "Combat Paused. Low on Health.")
                logger.warning(f"Combat Paused. Low on Health.")
                return
            temp.set("action_log", "Looking for Combat!")
            player.use_astral_vision()
            player.select_target(1)
            kbm.use_keyboard(
                options.get_keybind_key("keybind_basic_attack"), post_time=0
            )

        cycles_without_target += 1
        temp.set("cycles_without_target", cycles_without_target)

    def _handle_resource_gathering(self, tracker):
        temp.set("action_log", "Gathering Resources")
        if not tracker:
            logger.error("Tracker is not available. Skipping.")
            return
        found_coords = tracker.get("found_coords")
        if not found_coords:
            logger.warning("Can't find resource coords. Skipping.")
            return
        resource_x = found_coords[0]
        resource_y = found_coords[1]
        temp.raise_if_killswitch_engaged()
        kbm.move_mouse(resource_x, resource_y, click=False)
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(options.get_keybind_key("keybind_interact"))
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        temp.raise_if_killswitch_engaged()
        if player.detected_combat(7):
            logger.warning("Combat detected. Skipping.")
            return
        tracker.set("ready", False)
        # Add 5 seconds so we dont check again immediately.
        tracker.set("last_update", (time.time() + 5))
        tracker.set("found_coords", None)


battle_noexit = BattleNoExit()
