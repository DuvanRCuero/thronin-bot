from thronin.global_variables.assets import assets
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.utils.screenshot import screenshot_utils
import os
import time
from pynput.keyboard import Key, KeyCode


class Routine:
    def __init__(self, routine_name):
        self.routine_name = routine_name
        self._required_trackers = []
        self._cached_images = {}
        self._last_run = 0
        self._need_to_run_every = 0
        self._export_last_run_time = False
        self.output = ""
        self._import_last_run_time()

    def _sleep_safely(self, time_to_sleep):
        start_time = time.time()
        while True:
            temp.raise_if_killswitch_engaged()
            time_elapsed = time.time() - start_time
            logger.debug(f"Sleeping. Time Remaining: {time_to_sleep - time_elapsed}")
            if time_elapsed >= time_to_sleep:
                return
            time.sleep(0.1)

    def _import_last_run_time(self):
        if os.path.exists(f"cache/last_run_{self.routine_name}"):
            with open(f"cache/last_run_{self.routine_name}", "r") as f:
                timestamp = float(f.read().strip())  # Read and convert to float
                logger.debug(f"Imported Last Run Time: {time.ctime(timestamp)}")
        else:
            timestamp = 0
        self._last_run = timestamp

    def update_last_run_time(self):
        self._last_run = time.time()
        if self._export_last_run_time:
            if not os.path.exists("cache"):
                os.makedirs("cache")
            with open(f"cache/last_run_{self.routine_name}", "w") as f:
                f.write(str(self._last_run))

    def need_to_run(self):
        need_to_run = time.time() >= self._last_run + self._need_to_run_every
        return need_to_run

    def get_required_trackers(self):
        return self._required_trackers

    def _complete_routine(self, next_routine=None):
        kbm.reset_mouse()
        self.update_last_run_time()
        temp.set("current_routine", next_routine)

    def _find_and_click_target(
        self,
        what_to_look_for,
        tolerance=0.65,
        max_attempts=3,
        num_clicks=1,
        shift_click=False,
    ):
        attempt = 0
        while attempt < max_attempts:
            attempt += 1
            search_region = temp.get("screenshot")
            results = screenshot_utils.perform_template_matching(
                what_to_look_for, search_region, tolerance
            )
            logger.debug(f"find_and_click_target:{results}")
            if results["found"]:
                centerX = results["found_xywh"][0] + results["found_xywh"][2] / 2
                centerY = results["found_xywh"][1] + results["found_xywh"][3] / 2
                kbm.move_mouse(
                    centerX,
                    centerY,
                    click=True,
                    hold_shift=shift_click,
                    num_clicks=num_clicks,
                )
                return True
            else:
                logger.info(
                    f"Attempt {attempt}: {what_to_look_for} not found, retrying..."
                )
                time.sleep(1)
        return False

    def _select_map_location(self, name):
        kbm.use_keyboard(options.get_keybind_key("keybind_map"), post_time=0.5)
        kbm.reset_mouse()
        # Click Region button based on window size
        if temp.get("window_size") == 720:
            kbm.move_mouse(112, 110, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(169, 166, click=True)
        time.sleep(0.5)
        # Click search bar based on window size
        if temp.get("window_size") == 720:
            kbm.move_mouse(222, 168, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(330, 255, click=True)
        kbm.reset_mouse()
        # Type the location name using pynput
        kbm.type_with_kb(name)
        kbm.use_keyboard(Key.enter, post_time=1)
        # Click location button based on window size
        if temp.get("window_size") == 720:
            kbm.move_mouse(171, 270, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(292, 400, click=True)
        kbm.reset_mouse()
        time.sleep(1)

    def _teleport(self, pretty_name, search_name, x, y):
        temp.set("action_log", f"Teleporting to {pretty_name}")
        self._select_map_location(search_name)
        kbm.move_mouse(x, y, click=True)  # Click TP portal
        time.sleep(1.5)
        kbm.reset_mouse()
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"), post_time=10)
        # Adjust camera position by teleporting to Amitoi and back
        temp.set("action_log", "Fixing Camera")
        self._teleport_to_amitoi()
        # Verify we are in Amitoi House
        temp.set("action_log", f"Verifying we are in Amitoi House")
        max_retries = 5  # Number of attempts
        delay = 2  # Seconds between each check
        for attempt in range(1, max_retries + 1):
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
            return False  # Exit function if verification fails
        self._exit_amitoi_house()
        kbm.reset_mouse()
        time.sleep(1)
        return True

    def _teleport_to_amitoi(self):
        time.sleep(0.25)
        if temp.get("window_size") == 720:
            kbm.move_mouse(712, 659, click=True)  # Click Amitoi TP button
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1090, 960, click=True)  # Click Amitoi TP button
        time.sleep(0.25)
        kbm.reset_mouse()
        self._sleep_safely(10)  # Wait for TP to finish
        # time.sleep(10)

    def _verify_in_amitoi_house(self):
        if temp.get("window_size") == 720:
            # xywh = [1154, 20, 46, 8] # old location
            xywh = [1110, 133, 46, 8]
        elif temp.get("window_size") == 1080:
            # xywh = [1701, 37, 76, 11] # old location
            xywh = [1623, 234, 76, 11]
        x, y, w, h = xywh
        screenshot = temp.get("screenshot")
        search_region = screenshot[y : y + h, x : x + w]
        results = screenshot_utils.perform_template_matching(
            assets.get("locations", "in_amitoi_house"),
            search_region,
            0.98,
        )
        logger.debug(results)
        if results["found"]:
            return True
        return False

    def _exit_amitoi_house(self):
        temp.set("action_log", f"Exiting Amitoi House")
        if temp.get("window_size") == 720:
            kbm.move_mouse(1256, 133, click=True)  # Click Exit button
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1880, 235, click=True)  # Click Exit button
        time.sleep(1)
        kbm.reset_mouse()
        # Confirm Exit and wait for TP to finish
        kbm.use_keyboard(options.get_keybind_key("keybind_accept"), post_time=10)
        # Jump because character gets stuck after TP sometimes.
        kbm.use_keyboard(options.get_keybind_key("keybind_jump"), post_time=0.5)

    def _travel_to_vendor(self, vendor_name=None):
        temp.set("action_log", f"Traveling to {vendor_name}")
        if not vendor_name:
            logger.error("Vendor Name is required.")
            return False

        # Get the path for the chosen merchant
        chosen_vendor_path = assets.get("vendors", vendor_name)
        if not chosen_vendor_path:
            logger.error(f"No path found for vendor: {vendor_name}")
            return False

        # Attempt to find and click the target
        found = self._find_and_click_target(chosen_vendor_path)
        if not found:
            logger.error(f"{vendor_name} was not found.")
            return False

        # Morph to move faster
        kbm.use_keyboard(Key.shift)
        # Moves character to the vendor
        kbm.use_keyboard(options.get_keybind_key("keybind_interact"))
        time.sleep(6)  # Allow time to travel to the vendor

        return True

    def _handle_vendor_not_found(self):
        logger.error("Vendor not found. Resetting Routine.")
        temp.set("current_routine", None)
        time.sleep(1)

    def _deposit_items(self):
        temp.set("action_log", f"Depositing Items")
        # Click Quick Deposit button
        if temp.get("window_size") == 720:
            kbm.move_mouse(1110, 674, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1659, 1018, click=True)
        time.sleep(1)
