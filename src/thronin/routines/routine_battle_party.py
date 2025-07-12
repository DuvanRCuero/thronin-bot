from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.lib.player import player
from thronin.routines._base import Routine
from thronin.trackers.amitoi import amitoi
from thronin.trackers.health import health
from thronin.trackers.party import party
from thronin.trackers.party_invite import party_invite
from thronin.trackers.resources_nearby import resources_nearby
from thronin.trackers.target import target
import time
from pynput.keyboard import Key


class BattleParty(Routine):
    def __init__(self):
        super().__init__("battle_party")
        self.pretty_name = "Party Mode"
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
            "party",
            "party_invite",
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

        self.cycles_not_in_party = 0
        self.cycles_in_party = 0

    def run(self):
        temp.raise_if_killswitch_engaged()
        in_party = party.get("ready")
        self._update_party_status(in_party)
        temp.raise_if_killswitch_engaged()
        if in_party:
            # Were using party-invte again to check for a contract invite since they use the same location for the accept button.
            if party_invite.get("ready"):
                logger.info("We appear to have a contract invite.")
                self._accept_invite()
                temp.raise_if_killswitch_engaged()
                self._accept_contract()
                temp.raise_if_killswitch_engaged()
                time.sleep(0.25)
                kbm.use_keyboard(
                    options.get_keybind_key("keybind_accept"), post_time=0.25
                )
                return
            temp.raise_if_killswitch_engaged()
            if self._handle_precombat():
                return
            in_combat = target.get("ready")
            temp.raise_if_killswitch_engaged()
            self._handle_in_combat() if in_combat else self._handle_not_in_combat()
        else:
            temp.set("action_log", "Waiting for Party")
            logger.warning("We are NOT in a party.")
            temp.raise_if_killswitch_engaged()
            if party_invite.get("ready"):
                self._accept_invite()
            else:
                logger.warning("No invite found.")
                if player.detected_combat(3):
                    logger.warning("Combat Detected Aborting.")
                    return

    def _update_party_status(self, in_party: bool):
        if in_party:
            self.cycles_not_in_party = 0
            self.cycles_in_party += 1
        else:
            self.cycles_in_party = 0
            self.cycles_not_in_party += 1

    def _accept_invite(self):
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Accepting Invite")
        # Click Accept Button
        if temp.get("window_size") == 720:
            kbm.move_mouse(170, 205, click=True, duration_to_move=0)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(299, 361, click=True, duration_to_move=0)

    def _accept_contract(self):
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Accepting Contract")
        # Click Accept Button
        if temp.get("window_size") == 720:
            kbm.move_mouse(908, 536, click=True, duration_to_move=0)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1267, 850, click=True, duration_to_move=0)

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
        temp.raise_if_killswitch_engaged()

        # Press tab to check for target.
        temp.set("action_log", "Checking for target")
        # kbm.use_keyboard(Key.tab, post_time=0.25)
        kbm.use_keyboard(
            options.get_keybind_key("keybind_party_leader_target"), post_time=0.25
        )
        return False

    def _handle_in_combat(self):
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
        temp.raise_if_killswitch_engaged()
        # Check Line of Sight
        if player.reset_los():
            cycles_without_los = temp.get("cycles_without_los")
            temp.set("cycles_without_los", (cycles_without_los + 1))
            return
        temp.raise_if_killswitch_engaged()
        # Perform Combat
        temp.set("cycles_without_los", 0)
        player.perform_combat()

    def _handle_not_in_combat(self):
        # Reset variables
        cycles_without_target = temp.get("cycles_without_target")
        temp.set("cycles_without_los", 0)
        temp.set("action_log", "NOT IN COMBAT!")

        # if >0: check for resources or stonegard, if yes perform another loop. if no look for trouble.
        if cycles_without_target > 0:
            # Moving to Party Leader
            self._follow_target()

        cycles_without_target += 1
        temp.set("cycles_without_target", cycles_without_target)

    def _follow_target(self):
        # Select Party Member 1
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard("1", post_time=0.35, modifier=Key.ctrl)
        # Click target menu
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(408, 24, click=True, duration_to_move=0)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(716, 43, click=True, duration_to_move=0)
        # Click Follow button
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(444, 100, click=True, duration_to_move=0)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(781, 177, click=True, duration_to_move=0)
        # Remove Friendly Target
        temp.raise_if_killswitch_engaged()
        kbm.release_friendly_target()


battle_party = BattleParty()
