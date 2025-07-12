from thronin.global_variables.options import options
from thronin.global_variables.cache import cache
from thronin.global_variables.temp import temp
from thronin.lib.logger import logger
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
import pyautogui
import time
from pynput.keyboard import Key
from thronin.trackers.amitoi import amitoi
from thronin.trackers.bobber import bobber
from thronin.trackers.casting import casting
from thronin.trackers.death import death
from thronin.trackers.fish_on_line import fish_on_line
from thronin.trackers.fishing_pole_casted import fishing_pole_casted
from thronin.trackers.fishing_pole_equipped import fishing_pole_equipped
from thronin.trackers.health import health
from thronin.trackers.line_of_sight import line_of_sight
from thronin.trackers.mana import mana
from thronin.trackers.need_to_block import need_to_block
from thronin.trackers.party import party
from thronin.trackers.party_invite import party_invite
from thronin.trackers.pvp_z import pvp_z
from thronin.trackers.quick_slot import quickslot1
from thronin.trackers.quick_slot import quickslot2
from thronin.trackers.quick_slot import quickslot3
from thronin.trackers.quick_slot import quickslot4
from thronin.trackers.quick_slot import quickslot5
from thronin.trackers.quick_slot import quickslot6
from thronin.trackers.quick_slot import quickslot7
from thronin.trackers.quick_slot import quickslot8
from thronin.trackers.quick_slot import quickslot9
from thronin.trackers.quick_slot import quickslot10
from thronin.trackers.quick_slot import quickslot11
from thronin.trackers.quick_slot import quickslot12
from thronin.trackers.quick_slot import itemquickslot1
from thronin.trackers.quick_slot import itemquickslot2
from thronin.trackers.quick_slot import itemquickslot3
from thronin.trackers.quick_slot import itemquickslot4
from thronin.trackers.resources_nearby import resources_nearby
from thronin.trackers.target import target
from thronin.global_variables.trackers import trackers


class Player:

    def load_player(self):
        self.monitored_skillbars = []
        self.combat_skills = []
        self.health_recovery_skills = []
        self.mana_recovery_skills = []
        logger.info(f"Loading Player")
        for tracker_name, tracker in trackers.get_all().items():
            if tracker_name.startswith("quickslot"):
                if options.get(f"{tracker_name}_monitored_by_bot"):
                    self.monitored_skillbars.append(tracker)
                    if options.get(f"{tracker_name}_type") == "Combat":
                        self.combat_skills.append(tracker)
                    elif options.get(f"{tracker_name}_type") == "Health Recovery":
                        self.health_recovery_skills.append(tracker)
                    elif options.get(f"{tracker_name}_type") == "Mana Recovery":
                        self.mana_recovery_skills.append(tracker)
        logger.debug(f"monitored_skillbars: {self.monitored_skillbars}")
        logger.debug(f"combat_skills: {self.combat_skills}")
        logger.debug(f"health_recovery_skills: {self.health_recovery_skills}")
        logger.debug(f"mana_recovery_skills: {self.mana_recovery_skills}")

    ###
    # PUBLIC FUNCTIONS USED IN BATTLE
    ###
    def _is_needed(self, current_percent: 0, percent_to_use: 1, name_for_logs):
        required = float(current_percent) <= float(percent_to_use)
        logger.info(
            f"{name_for_logs} required: {required} ({current_percent} <= {percent_to_use})"
        )
        return required

    def use_itemquickslot3_if_needed(self):
        use_itemquickslot3_every = options.get("use_itemquickslot3_every")
        if use_itemquickslot3_every == 0:
            logger.info(f"Skipping Item Quick Slot 3 (Disabled)")
            return
        last_use_itemquickslot3 = cache.get("last_use_itemquickslot3")
        current_time = time.time()
        time_to_use = use_itemquickslot3_every + last_use_itemquickslot3
        required = time_to_use <= current_time
        remaining_time = int(time_to_use - current_time)
        logger.info(f"itemquickslot3 required: {required} (Use in {remaining_time})")
        if required:
            temp.set("action_log", "Using Item Quick Slot 3")
            self._execute_itemslot_if_ready("itemquickslot3")
            cache.set("last_use_itemquickslot3", current_time)

    def use_itemquickslot4_if_needed(self):
        use_itemquickslot4_every = options.get("use_itemquickslot4_every")
        if use_itemquickslot4_every == 0:
            logger.info(f"Skipping Item Quick Slot 4 (Disabled)")
            return
        last_use_itemquickslot4 = cache.get("last_use_itemquickslot4")
        current_time = time.time()
        time_to_use = use_itemquickslot4_every + last_use_itemquickslot4
        required = time_to_use <= current_time
        remaining_time = int(time_to_use - current_time)
        logger.info(f"itemquickslot4 required: {required} (Use in {remaining_time})")
        if required:
            temp.set("action_log", "Using Item Quick Slot 4")
            self._execute_itemslot_if_ready("itemquickslot4")
            cache.set("last_use_itemquickslot4", current_time)

    def use_health_recovery_skills_if_needed(self):
        is_needed = self._is_needed(
            current_percent=health.get("percentage"),
            percent_to_use=options.get("player_percent_to_use_health_recovery_skills"),
            name_for_logs="Healing Skills",
        )
        if is_needed:
            temp.set("action_log", "Using Health Recovery Skills")
            for skill in self.health_recovery_skills:
                self._execute_skill_if_ready(skill)

    def use_health_potion_if_needed(self):
        is_needed = self._is_needed(
            current_percent=health.get("percentage"),
            percent_to_use=options.get("player_percent_to_use_health_potion"),
            name_for_logs="Healing Potion",
        )
        if is_needed:
            temp.set("action_log", "Using Health Potion")
            self._execute_itemslot_if_ready("itemquickslot1")

    def use_companion_if_needed(self):
        is_needed = self._is_needed(
            current_percent=health.get("percentage"),
            percent_to_use=options.get("player_percent_to_use_companion"),
            name_for_logs="Companion",
        )
        if is_needed:
            temp.set("action_log", "Bringing in Companion")
            kbm.use_keyboard(
                options.get_keybind_key("keybind_companion"), post_time=0.25
            )

    def use_mana_recovery_skills_if_needed(self):
        is_needed = self._is_needed(
            current_percent=mana.get("percentage"),
            percent_to_use=options.get("player_percent_to_use_mana_recovery_skills"),
            name_for_logs="Mana Skills",
        )
        if is_needed:
            temp.set("action_log", "Using Mana Recovery Skills")
            for skill in self.mana_recovery_skills:
                self._execute_skill_if_ready(skill)

    def use_mana_potion_if_needed(self):
        is_needed = self._is_needed(
            current_percent=mana.get("percentage"),
            percent_to_use=options.get("player_percent_to_use_mana_potion"),
            name_for_logs="Mana Potion",
        )
        if is_needed:
            temp.set("action_log", "Using Mana Potion")
            self._execute_itemslot_if_ready("itemquickslot2")

    def select_target(self, number):
        temp.set("action_log", f"Selecting Target: {number}.")
        pyautogui.press(f"num{number}")

    def use_astral_vision_if_no_los(self):
        action_performed = False
        if not line_of_sight.get("ready"):
            self.use_astral_vision()
            action_performed = True
        return action_performed

    def use_astral_vision(self):
        temp.set("action_log", "Using Astral Vision")
        kbm.use_keyboard(
            options.get_keybind_key("keybind_astral"),
            post_time=0.35,
            modifier=Key.alt,
        )

    def reset_los(self):
        if not line_of_sight.get("ready"):
            temp.set("action_log", "Resetting LOS")
            logger.warning("No LOS - clearing target and retrying.")
            kbm.use_keyboard(
                options.get_keybind_key("keybind_clear_target"), post_time=0.25
            )
            kbm.use_keyboard(
                options.get_keybind_key("keybind_clear_target"), post_time=0.25
            )
            kbm.use_keyboard(Key.tab, post_time=0.25)
            return True
        else:
            return False

    def counterattack_if_needed(self):
        action_performed = False
        if pvp_z.get("ready"):
            self.use_counterattack()
            action_performed = True
        return action_performed

    def use_counterattack(self):
        temp.set("action_log", "Counter Attacking")
        logger.warning("Using Counter Attack.")
        kbm.use_keyboard(
            options.get_keybind_key("keybind_counterattack"),
            press_time=0.5,
            post_time=0.25,
        )
        pvp_z.set("last_update", time.time() + 10)
        pvp_z.set("ready", False)

    def block_if_needed(self):
        action_performed = False
        if need_to_block.get("ready"):
            self.use_block()
            action_performed = True
        return action_performed

    def use_block(self):
        temp.set("action_log", "Blocking")
        logger.warning("Using Block.")
        kbm.use_keyboard(
            options.get_keybind_key("keybind_defense_skill"),
            press_time=0.5,
            post_time=0.25,
        )
        need_to_block.set("ready", False)

    def detected_combat(self, wait_time):
        # Wait up to wait_time seconds to ensure we are out of combat.
        start_time = time.time()
        while True:
            kbm.use_keyboard(Key.tab, post_time=0.25)
            if target.get("ready"):
                logger.warning("Detected target before timeout.")
                return True
            time_elapsed = time.time() - start_time
            logger.debug(
                f"Watching for Combat. Time Remaining: {wait_time - time_elapsed}"
            )
            if time_elapsed >= wait_time:
                logger.info(f"No combat detected within {wait_time} seconds.")
                return False
            time.sleep(0.5)  # Check every half-second for in-combat status.

    def perform_combat(self, check_block=True, check_los=True, check_counter=True):
        # Returns True if it completes all skills else False.
        skills_to_use = []
        for tracker in self.combat_skills:
            if tracker.get("ready"):
                skills_to_use.append(tracker)

        # Log and exit if no skills are available
        if not skills_to_use:
            temp.set("action_log", "No active combat skills detected!")
            logger.warning(f"No active combat skills detected!")
            time.sleep(0.5)
            return False

        # Process each skill in the prepared list
        for skill in skills_to_use:
            # Check if were ready for combat
            if check_block and need_to_block.get("ready"):
                temp.set("action_log", "Need to Block")
                return False
            if check_counter and pvp_z.get("ready"):
                temp.set("action_log", "Need to Counter")
                return False
            if not target.get("ready"):
                temp.set("action_log", "Lost Target")
                line_of_sight.set("ready", False)
                kbm.use_keyboard(Key.tab, post_time=0.25)
                return False
            if check_los and not line_of_sight.get("ready"):
                temp.set("action_log", "Lost LOS")
                return False
            # Perform combat
            self._execute_skill(skill)
            skill.set("ready", False)

        # return True to indicate we completed all skills.
        return True

    ###
    # PRIVATE FUNCTIONS USED ONLY IN THE CLASS
    ###
    def _execute_itemslot_if_ready(self, itemslot_name):
        itemslot = trackers.get(itemslot_name)
        if itemslot.get("ready"):
            temp.set(
                "action_log",
                f"Executing {itemslot_name} ({itemslot.get("display")})",
            )
            kbm.use_keyboard(
                kb_button=itemslot.get("kb_button"),
                press_time=itemslot.get("press_time"),
                post_time=itemslot.get("post_time"),
                casting_skill=itemslot.get("casting_skill"),
            )
        else:
            logger.warning(f"{itemslot_name} is on cooldown.")

    def _execute_skill_if_ready(self, tracker):
        if tracker.get("ready"):
            kbm.use_keyboard(
                kb_button=tracker.get("kb_button"),
                casting_skill=tracker.get("casting_skill"),
            )
        else:
            logger.warning(f"{tracker.tracker_name} is on cooldown.")

    def _execute_skill(self, tracker):
        repetitions = tracker.get("repetitions")
        temp.set(
            "action_log",
            f"Executing {tracker.tracker_name} ({tracker.get("display")}) {repetitions} times",
        )
        for _ in range(repetitions):
            kbm.use_keyboard(
                kb_button=tracker.get("kb_button"),
                casting_skill=tracker.get("casting_skill"),
            )


player = Player()
