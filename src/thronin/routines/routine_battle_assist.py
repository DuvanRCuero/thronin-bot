from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.lib.player import player
from thronin.routines._base import Routine
from thronin.trackers.target import target
import time


class BattleAssistRoutine(Routine):
    def __init__(self):
        super().__init__("battle_assist")
        self.pretty_name = "Assist Mode"
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
            # "line_of_sight",
            "mana",
            # "need_to_block",
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
            # "resources_nearby",
            "target",
        ]

    def run(self):
        temp.raise_if_killswitch_engaged()
        player.counterattack_if_needed()
        temp.raise_if_killswitch_engaged()
        player.use_health_recovery_skills_if_needed()
        temp.raise_if_killswitch_engaged()
        in_combat = target.get("ready")
        if in_combat:
            temp.raise_if_killswitch_engaged()
            temp.set("action_log", "IN COMBAT!")
            player.use_health_potion_if_needed()
            temp.raise_if_killswitch_engaged()
            player.use_companion_if_needed()
            temp.raise_if_killswitch_engaged()
            player.use_mana_recovery_skills_if_needed()
            temp.raise_if_killswitch_engaged()
            player.use_mana_potion_if_needed()
            temp.raise_if_killswitch_engaged()
            player.perform_combat(check_block=False, check_los=False)
        else:
            temp.raise_if_killswitch_engaged()
            temp.set("action_log", "Waiting for target")
            logger.warning("No target selected.")
            time.sleep(0.5)


battle_assist = BattleAssistRoutine()
