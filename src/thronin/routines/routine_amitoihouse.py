from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.routines._base import Routine
from thronin.trackers.amitoi import amitoi
import time
from pynput.keyboard import Key


class AmitoiHouseRoutine(Routine):
    def __init__(self):
        super().__init__("amitoi_house")
        self._required_trackers = []
        self.pretty_name = "Amitoi House"

    def run(self):
        kbm.reset_mouse()
        time.sleep(1)

        # Start routine
        temp.raise_if_killswitch_engaged()
        self._teleport_to_amitoi()

        # Verify we are in Amitoi House
        temp.set("action_log", f"Verifying we are in Amitoi House")
        max_retries = 5  # Number of attempts
        delay = 2  # Seconds between each check
        for attempt in range(1, max_retries + 1):
            temp.raise_if_killswitch_engaged()
            if self._verify_in_amitoi_house():
                break
            logger.debug(
                f"Attempt {attempt}/{max_retries}: Verification failed. Retrying in {delay} seconds..."
            )
            time.sleep(delay)
        else:
            # If all attempts fail, log an error
            logger.error(
                "Failed to verify Amitoi House location after multiple attempts."
            )
            self._complete_routine(next_routine=None)
            return  # Exit if verification fails

        # Jump because character gets stuck after TP sometimes.
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(options.get_keybind_key("keybind_jump"))
        time.sleep(0.25)

        # Interact with the expedition map to move the character to the destination.
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(247, 438, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(375, 642, click=True)
        kbm.use_keyboard(options.get_keybind_key("keybind_interact"))
        kbm.use_keyboard(options.get_keybind_key("keybind_interact"))
        time.sleep(4)  # Pause for character movement

        # Claim the reward.
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(1076, 675, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1600, 1000, click=True)
        time.sleep(1)

        # Start expedition.
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(1076, 675, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1600, 1000, click=True)
        time.sleep(1)

        # Close the expedition map
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(Key.esc)

        # Finish the routine, setting amitoi as false to ensure it doesnt run again for a bit.
        temp.raise_if_killswitch_engaged()
        self._exit_amitoi_house()
        amitoi.set("ready", False)

        self._complete_routine(next_routine=None)


amitoi_house = AmitoiHouseRoutine()
