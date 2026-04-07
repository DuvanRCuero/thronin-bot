from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.lib.logger import logger
from thronin.trackers._base import Tracker
import numpy as np
import time


class FishingPoleCasted(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 5,
            "xywh": (596, 666, 1, 1),
            "target_color": np.array([21, 21, 21]),
        },
        1080: {
            "tolerance": 5,
            "xywh": (881, 984, 1, 1),
            "target_color": np.array([18, 18, 18]),
        },
    }

    def __init__(self):
        super().__init__("fishing_pole_casted")
        self.set("show_roi", False)
        self.set("update_interval", 0.5)

    def analyze_screenshot(self, screenshot):
        # Ensure were allowed to update
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") not in [720, 1080, 1440]:
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        # Extract parameters for the current locationf
        x, y, w, h = config.get("xywh")

        # Define search_region and modify image if needed
        search_region = screenshot[y : y + h, x : x + w]

        # Check if every pixel in the region is within tolerance of the target color.
        # logger.warning(
        #     f"{self.tracker_name}: {search_region}, looking for: {config.get("target_color")}"
        # )
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

        # Finished
        self.set("last_update", time.time())


fishing_pole_casted = FishingPoleCasted()
