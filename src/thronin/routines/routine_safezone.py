from thronin.global_variables.cache import cache
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.gui_manager import gui_manager
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.routines._base import Routine
from thronin.trackers.amitoi import amitoi
import time
from pynput.keyboard import Key


class SafeZoneRoutine(Routine):
    def __init__(self):
        super().__init__("safe_zone")
        self._required_trackers = ["amitoi"]
        self.last_routine = 0

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)
        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Chilling in the Safe Zone")

        # Perform Amitoi Rotation if applicable
        temp.raise_if_killswitch_engaged()
        if options.get("perform_amitoi") == True:
            if amitoi.get("ready"):
                temp.set("action_log", "Performing Amitoi Collection")
                self._complete_routine(next_routine="amitoi_house")
                return
        else:
            logger.info(f"Amitoi Collection is not wanted.")

        # Perform Battle Pass if applicable.
        temp.raise_if_killswitch_engaged()
        if self._need_to_run(
            "perform_battle_pass",
            "last_run_battle_pass",
            "perform_battle_pass_every",
            "Battle Pass",
        ):
            temp.set("action_log", "Performing Battle Pass")
            self._perform_battle_pass()

        # Perform Guild Collection if applicable.
        temp.raise_if_killswitch_engaged()
        if self._need_to_run(
            "perform_guild_collection",
            "last_run_guild_collection",
            "perform_guild_collection_every",
            "Guild Collection",
        ):
            temp.set("action_log", "Performing Guild Collection")
            self._perform_guild_collection()

        # Perform Guild Recruitment if applicable.
        temp.raise_if_killswitch_engaged()
        if self._need_to_run(
            "perform_guild_recruitment",
            "last_run_guild_recruitment",
            "perform_guild_recruitment_every",
            "Guild Recruitment",
        ):
            temp.set("action_log", "Performing Guild Recruitment")
            self._perform_guild_recruitment()

        # Perform Kastleton Routine if applicable (too drop off storage)
        temp.raise_if_killswitch_engaged()
        if self._need_to_run(
            "perform_kastleton",
            "last_run_kastleton",
            "perform_kastleton_every",
            "Kastleton",
        ):
            temp.set("action_log", "Performing Kastleton (Storage)")
            self._complete_routine(next_routine="kastleton")
            return

        # Perform Stonegard Routine if applicable
        temp.raise_if_killswitch_engaged()
        if self._need_to_run(
            "perform_stonegard",
            "last_run_stonegard",
            "perform_stonegard_every",
            "Stonegard",
        ):
            temp.set("action_log", "Performing Stonegard")
            self._complete_routine(next_routine="stonegard_castle")
            return

        # Update last run times.
        temp.raise_if_killswitch_engaged()
        cache.set("last_run_safe_zone", time.time())

        # Finished with routine - Rotate between routines
        temp.raise_if_killswitch_engaged()
        force_routine = options.get("force_routine")
        if force_routine and force_routine == "safe_zone":
            self._complete_routine(next_routine="safe_zone")
            return
        next_routine = None
        defaults = options.get_default_options()
        farming_locations = [key for key in defaults if key.startswith("farm_")]
        wanted_locations = []

        # Collect routines where the option is True
        for i in farming_locations:
            if options.get(i) == True:
                name = i.replace("farm_", "")
                wanted_locations.append(name)

        # If there are any wanted locations, rotate through them
        if wanted_locations:
            # Ensure that we are rotating through the available wanted locations
            next_routine = wanted_locations[self.last_routine]
            self.last_routine = (self.last_routine + 1) % len(wanted_locations)
        else:
            logger.info("No locations selected for farming.")
            next_routine = None  # Or handle it differently depending on your logic

        # Reset cycle count and log the next location
        temp.set("cycles_without_target", 0)
        logger.info(f"Next Routine: {next_routine}")

        self._complete_routine(next_routine=next_routine)

    def _need_to_run(self, allowed_to_run_key, last_run_key, perform_every_key, title):
        if options.get(allowed_to_run_key) == False:
            logger.info(f"{title} is not wanted.")
            return False

        last_run = cache.get(last_run_key)
        next_run = last_run + options.get(perform_every_key)
        if time.time() >= next_run:
            logger.info(f"{title} is ready now.")
            return True
        else:
            logger.debug(f"{title} is ready at {time.ctime(next_run)}.")
        return False

    def _perform_battle_pass(self):
        kbm.reset_mouse()
        time.sleep(1)

        # Open Interface
        kbm.use_keyboard(options.get_keybind_key("keybind_battle_pass"))
        time.sleep(1)

        # Click Claim All Points
        if temp.get("window_size") == 720:
            kbm.move_mouse(1143, 673, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1715, 1010, click=True)
        time.sleep(1)

        # Click Claim All Rewards
        if temp.get("window_size") == 720:
            kbm.move_mouse(833, 673, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1252, 1010, click=True)
        time.sleep(1)
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"))
        time.sleep(1)

        # Close Interface
        kbm.use_keyboard(Key.esc)

        # Save Last Run Time
        cache.set("last_run_battle_pass", time.time())
        time.sleep(1)

    def _perform_guild_collection(self):
        kbm.reset_mouse()
        time.sleep(1)

        # Press G to bring up guild screen
        kbm.use_keyboard(options.get_keybind_key("keybind_guild"))
        time.sleep(0.5)

        if options.get("donate_on_guild_collection") == True:
            # Click Info button
            if temp.get("window_size") == 720:
                kbm.move_mouse(115, 120, click=True)
            elif temp.get("window_size") == 1080:
                kbm.move_mouse(146, 180, click=True)
            time.sleep(0.5)

            # Click Donate 10 times
            if temp.get("window_size") == 720:
                kbm.move_mouse(1187, 210, click=True, num_clicks=10)
            elif temp.get("window_size") == 1080:
                kbm.move_mouse(1782, 315, click=True, num_clicks=10)
            time.sleep(0.5)

        # Click Rewards button
        if temp.get("window_size") == 720:
            kbm.move_mouse(115, 220, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(171, 329, click=True)
        time.sleep(0.5)

        # Click Claim All
        if temp.get("window_size") == 720:
            kbm.move_mouse(846, 674, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1269, 1020, click=True)
        time.sleep(1)
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"))
        time.sleep(0.5)

        # Click Open button on Chest
        if temp.get("window_size") == 720:
            kbm.move_mouse(1086, 405, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1630, 611, click=True)
        time.sleep(1)
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"))
        time.sleep(0.5)

        # Esc to exit
        kbm.use_keyboard(Key.esc)

        # Save Last Run Time
        cache.set("last_run_guild_collection", time.time())
        time.sleep(1)

    def _perform_guild_recruitment(self):
        if options.get("perform_guild_recruitment") == False:
            logger.info(f"Skipping Guild Recruitment, not wanted.")
            return
        if options.get("guild_recruitment_message") == "":
            logger.info(f"Skipping Guild Recruitment, message is empty.")
            return

        kbm.reset_mouse()
        gui_manager.hide_overlay()
        time.sleep(1)

        # Ensure we are in world chat.
        kbm.use_keyboard(Key.enter)
        kbm.type_with_kb("/a ")
        kbm.use_keyboard(Key.enter)
        time.sleep(0.1)

        # If message is bigger than 299 characters, split it into smaller messages
        message = options.get("guild_recruitment_message")

        # Split the message into chunks of 299 characters or less
        chunk_size = 299
        chunks = [
            message[i : i + chunk_size] for i in range(0, len(message), chunk_size)
        ]

        # Iterate over the chunks and send each one
        for chunk in chunks:
            kbm.set_message_to_clipboard(chunk)
            kbm.use_keyboard(Key.enter)
            kbm.paste_with_kb()
            kbm.use_keyboard(Key.enter)
            time.sleep(0.1)  # Add a slight delay between each chunk

        # Save Last Run Time
        cache.set("last_run_guild_recruitment", time.time())
        time.sleep(1)

        # Bring overlay back up
        gui_manager.show_overlay()


safe_zone = SafeZoneRoutine()
