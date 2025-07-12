from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.trackers._base import Tracker
from thronin.utils.screenshot import screenshot_utils
import numpy as np
import time


class LineOfSight(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "xywh": (50, 280, 4, 8),
            "lower_hsv": [0, 75, 78],
            "upper_hsv": [113, 255, 255],
        },
        1080: {
            "xywh": (75, 495, 3, 12),
            "lower_hsv": [0, 75, 78],
            "upper_hsv": [113, 255, 255],
        },
    }

    def __init__(self):
        super().__init__("line_of_sight")
        self.set("show_roi", False)
        self.set("update_interval", 0.2)

    def analyze_screenshot(self, screenshot):
        # Ensure were allowed to update
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") != 720 and temp.get("window_size") != 1080:
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        # Extract parameters for the current location
        x, y, w, h = config.get("xywh")

        # Define search_region and modify image if needed
        search_region = screenshot[y : y + h, x : x + w]
        search_region_image, mask = screenshot_utils.apply_hsv_mask(
            search_region,
            config.get("lower_hsv"),
            config.get("upper_hsv"),
            return_with_mask=True,
        )

        # Check if any pixel in the mask is greater than 0.
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

        self.set("last_update", time.time())


line_of_sight = LineOfSight()
