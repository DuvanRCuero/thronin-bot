from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.trackers._base import Tracker
from thronin.utils.screenshot import screenshot_utils
import cv2 as cv
import numpy as np
import time


class NeedToBlock(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "search_region_width": 800,
            "search_region_height": 550,
            "search_region_y_offset": -40,
            "blur": 5,
            "dp": 1.0,
            "minDist": 10,
            "param1": 375,
            "param2": 28,
            "minRadius": 10,
            "maxRadius": 50,
        },
        1080: {
            "search_region_width": 1100,
            "search_region_height": 800,
            "search_region_y_offset": -50,
            "blur": 15,
            "dp": 1.0,
            "minDist": 10,
            "param1": 375,
            "param2": 28,
            "minRadius": 15,
            "maxRadius": 60,
        },
    }

    def __init__(self):
        super().__init__("need_to_block")
        self.set("show_roi", False)
        self.set("update_interval", 0.2)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_defense_skill")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])

    def analyze_screenshot(self, screenshot):
        # Ensure were allowed to update
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") != 720 and temp.get("window_size") != 1080:
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        # Determine the search region based on the screenshot dimensions.
        screenshot_height, screenshot_width, _ = screenshot.shape
        search_region_x = screenshot_width // 2 - config["search_region_width"] // 2
        search_region_y = (
            screenshot_height // 2 - config["search_region_height"] // 2
        ) + config["search_region_y_offset"]
        search_region = screenshot[
            search_region_y : search_region_y + config["search_region_height"],
            search_region_x : search_region_x + config["search_region_width"],
        ]

        # Apply HSV filters to detect purple or white colors.
        # Purple range: [130, 50, 50] to [160, 255, 255]
        # White range: [0, 0, 200] to [179, 30, 255]
        _, mask_purple = screenshot_utils.apply_hsv_mask(
            search_region, [130, 50, 50], [160, 255, 255], return_with_mask=True
        )
        _, mask_white = screenshot_utils.apply_hsv_mask(
            search_region, [0, 0, 200], [179, 30, 255], return_with_mask=True
        )
        combined_mask = cv.bitwise_or(mask_purple, mask_white)
        filtered_roi = cv.bitwise_and(search_region, search_region, mask=combined_mask)

        # Convert the filtered region to grayscale and blur it.
        gray = cv.cvtColor(filtered_roi, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (config["blur"], config["blur"]), 2)
        final_roi = blurred

        # Detect circles in the processed ROI.
        circles = cv.HoughCircles(
            final_roi,
            cv.HOUGH_GRADIENT,
            dp=config["dp"],
            minDist=config["minDist"],
            param1=config["param1"],
            param2=config["param2"],
            minRadius=config["minRadius"],
            maxRadius=config["maxRadius"],
        )
        ready = True if circles is not None else False
        self.set("ready", ready)
        shape_data = []
        if ready:
            circles = np.round(circles[0, :]).astype("int")
            circle = circles[0]
            circle_x = circle[0] + search_region_x
            circle_y = circle[1] + search_region_y
            circle_r = circle[2] + 2
            if DEBUG_MODE:
                shape_data.append(
                    {
                        "type": "circle",
                        "key": "block_location",
                        "config": {
                            "x1": circle_x - circle_r,
                            "y1": circle_y - circle_r,
                            "x2": circle_x + circle_r,
                            "y2": circle_y + circle_r,
                            "outline": "green" if ready else "red",
                            "width": 2,  # Line thickness
                        },
                    }
                )
            # Temporarily stall further updates since an action will be triggered.
            self.set("last_update", time.time() + 5)

        # Add a rectangle to the overlay.
        if DEBUG_MODE:
            shape_data.append(
                {
                    "type": "rectangle",
                    "key": self.tracker_name,
                    "config": {
                        "x1": search_region_x - 2,
                        "y1": search_region_y - 2,
                        "x2": (search_region_x + config["search_region_width"]) + 2,
                        "y2": (search_region_y + config["search_region_height"]) + 2,
                        "outline": "green" if ready else "red",
                        "width": 2,  # Line thickness.
                    },
                }
            )

        # Update the shapes for our debug overlay
        self.set("shapes", shape_data)

        # Update ROI
        if self.get("show_roi"):
            self.set("roi", final_roi)

        # Finished
        self.set("last_update", time.time())


# Instantiate the tracker.
need_to_block = NeedToBlock()
