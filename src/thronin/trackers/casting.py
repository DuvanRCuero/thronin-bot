from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.trackers._base import Tracker
from thronin.utils.screenshot import screenshot_utils
import numpy as np
import time


class Casting(Tracker):
    WINDOW_CONFIGS = {
        720: {"xywh": (680, 568, 1, 1)},
        1080: {"xywh": (1039, 814, 1, 1)},
    }

    def __init__(self):
        super().__init__("casting")
        self.set("show_roi", False)
        self.set("update_interval", 99999999999)  # Only needed when casting.

    def analyze_screenshot(self, screenshot):
        # Ensure we're allowed to update.
        if not self._allowed_to_update():
            return

        # Load Config.
        window_size = temp.get("window_size")
        if window_size not in (720, 1080):
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        x, y, w, h = config["xywh"]

        # Define search_region and modify image if needed.
        search_region = screenshot[y : y + h, x : x + w]
        search_region_image, mask = screenshot_utils.apply_hsv_mask(
            search_region,
            lower_hsv=[119, 95, 0],
            upper_hsv=[179, 255, 50],
            return_with_mask=True,
        )

        # Check for any colored pixels in the region.
        ready = np.any(mask > 0)
        self.set("ready", ready)

        shape_data = []
        # Add a rectangle to the overlay.
        if DEBUG_MODE:
            shape_data.append(
                {
                    "type": "rectangle",
                    "key": self.tracker_name,
                    "config": {
                        "x1": x - 2,
                        "y1": y - 2,
                        "x2": (x + w) + 2,
                        "y2": (y + h) + 2,
                        "outline": "green" if ready else "red",
                        "width": 2,  # Line thickness.
                    },
                }
            )

        # Update the shapes for our debug overlay
        self.set("shapes", shape_data)

        # Update ROI
        if self.get("show_roi"):
            self.set("roi", search_region)

        # Mark finished update.
        self.set("last_update", time.time())


casting = Casting()
