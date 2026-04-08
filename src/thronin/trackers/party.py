from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.trackers._base import Tracker
import numpy as np
import time


class Party(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 5,
            "xywh": (22, 90, 1, 1),
            "target_color": np.array([255, 149, 72]),
        },
        1080: {
            "tolerance": 5,
            "xywh": (39, 157, 1, 1),
            "target_color": np.array([255, 149, 72]),
        },
    }

    def __init__(self):
        super().__init__("party")
        self.set("show_roi", False)
        self.set("update_interval", 1)

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

        # Check if every pixel in the region is within tolerance of the target color.
        ready = np.all(
            np.abs(search_region - config.get("target_color"))
            <= config.get("tolerance")
        )
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

        # Finished
        self.set("last_update", time.time())


party = Party()
