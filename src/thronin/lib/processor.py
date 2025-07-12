from thronin.global_variables.assets import assets
from thronin.global_variables.options import options
from thronin.global_variables.routines import routines
from thronin.global_variables.temp import temp
from thronin.global_variables.trackers import trackers
from thronin.lib.logger import logger
from thronin.utils.screenshot import screenshot_utils
from typing import Optional
import os
import re
import time


class Processor:
    def analyze_screenshot(self):
        screenshot = temp.get("screenshot")
        if screenshot_utils.invalid_screenshot(screenshot):
            return

        routine = self._determine_routine_to_use(screenshot)
        temp.set("current_routine", routine)

        if routine:
            self._handle_trackers(routine, screenshot)

    def _handle_trackers(self, routine_name, screenshot):
        routine_config = routines.get(routine_name)
        required_trackers = routine_config.get_required_trackers()
        all_trackers = trackers.get_all()

        if required_trackers == ["*"]:
            for tracker in all_trackers.values():
                if not tracker.get("enabled"):
                    tracker.enable()
                tracker.analyze_screenshot(screenshot)
            return

        for tracker_name, tracker in all_trackers.items():
            enabled = tracker.get("enabled")

            if tracker_name in required_trackers:
                if not enabled:
                    tracker.enable()
            elif enabled:
                tracker.disable()

            if tracker.get("enabled"):
                tracker.analyze_screenshot(screenshot)

    def _determine_routine_to_use(self, screenshot):
        force_routine = options.get("force_routine")
        if force_routine and force_routine != "default":
            return force_routine

        current_routine = temp.get("current_routine")
        if not current_routine:
            temp.set("action_log", "Searching for Location")
            return self._match_location(screenshot)

        return current_routine

    def _match_location(self, screenshot) -> Optional[str]:
        locations = assets.get_all("locations")
        for path in locations.values():
            try:
                filename = os.path.basename(path)
                match = re.search(r"([\w_]+?)(\d*)\.png$", filename)
                if not match:
                    raise ValueError(f"Unrecognized file format: {path}")
                location_name = match.group(1)
            except Exception as e:
                logger.error(f"Regex error for {path}: {e}")
                continue

            try:
                results = screenshot_utils.perform_template_matching(
                    path, screenshot, tolerance=0.8
                )
                found = results.get("found")
                confidence = results.get("confidence", 0.0)
            except Exception as e:
                logger.error(f"Template matching error for {path}: {e}")
                continue

            logger.debug(
                f"Match check: {location_name} - Found={found} (Confidence={confidence:.2f})"
            )
            if found:
                xywh = results["found_xywh"]
                center_xy = [int(xywh[0] + xywh[2] / 2), int(xywh[1] + xywh[3] / 2)]
                temp.set("action_log", f"Match Found: {location_name}")
                logger.debug({"xywh": xywh, "center_xy": center_xy})
                return location_name

        logger.warning("No matches found.")
        screenshot_utils.save_screenshot("unknown_location")
        time.sleep(5)
        return None


processor = Processor()
