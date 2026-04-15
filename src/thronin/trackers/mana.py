from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.trackers._base import Tracker
from thronin.utils.screenshot import screenshot_utils
import numpy as np
import time


class Mana(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "xywh": (53, 46, 105, 1),
            "lower_hsv": [90, 50, 50],
            "upper_hsv": [120, 255, 255],
        },
        1080: {
            "xywh": (92, 83, 185, 1),
            "lower_hsv": [90, 50, 50],
            "upper_hsv": [120, 255, 255],
        },
    }

    def __init__(self):
        super().__init__("mana")
        self.set("show_roi", False)
        self.set("update_interval", 1)
        self.set("ready", True)  # Never not ready
        # Adding new variables specific to this tracker
        self.set("percentage", 1)

    def analyze_screenshot(self, screenshot):
        # Ensure were allowed to update
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") not in [720, 1080, 1440]:
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

        # Find the position of the color line within the mask
        color_positions = np.where(mask[0] > 0)[0]
        percentage = (
            0.99 if color_positions.size == 0 else round(color_positions[-1] / w, 2)
        )
        self.set("percentage", percentage)

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
                        "outline": "green" if percentage > 0.35 else "red",
                        "width": 2,  # Line thickness.
                    },
                }
            )

        # Update the shapes for our debug overlay
        self.set("shapes", shape_data)

        # Update ROI
        if self.get("show_roi"):
            self.set("roi", search_region_image)

        # Finished
        self.set("last_update", time.time())


mana = Mana()
