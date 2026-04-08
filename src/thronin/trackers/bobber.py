from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.trackers._base import Tracker
from thronin.utils.screenshot import screenshot_utils
import cv2 as cv
import time


class Bobber(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "search_region_width": 400,
            "search_region_height": 150,
            "search_region_y_offset": -200,
        },
        1080: {
            "search_region_width": 500,
            "search_region_height": 150,
            "search_region_y_offset": -250,
        },
    }

    def __init__(self):
        super().__init__("bobber")
        self.set("show_roi", False)
        self.set("update_interval", 0)
        self.set("last_bobber_x", 0)

    def analyze_screenshot(self, screenshot):
        # Ensure were allowed to update
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") != 720 and temp.get("window_size") != 1080:
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        # Define search_region and modify image if needed
        screenshot_height, screenshot_width, _ = screenshot.shape
        search_region_x = screenshot_width // 2 - config["search_region_width"] // 2
        search_region_y = (
            screenshot_height // 2 - config["search_region_height"] // 2
        ) + config["search_region_y_offset"]
        search_region = screenshot[
            search_region_y : search_region_y + config["search_region_height"],
            search_region_x : search_region_x + config["search_region_width"],
        ]
        # # Update the coords for the bobber window in the overlay

        # Apply HSV mask - GREEN
        search_region_image, mask = screenshot_utils.apply_hsv_mask(
            search_region,
            [38, 70, 155],
            [85, 255, 255],
            return_with_mask=True,
        )
        non_zero_pixels = cv.findNonZero(mask)

        # Find non-zero pixels in the mask
        bobber_is_found = None  # False
        ready = False
        if non_zero_pixels is not None:
            pixel = non_zero_pixels[0][0]  # (x, y) of the first non-zero pixel
            x, y = pixel[0], pixel[1]
            # Convert coordinates to global frame
            global_x = search_region_x + x
            global_y = search_region_y + y
            # Update found_coords
            bobber_is_found = (global_x, global_y)  # True
            self.set("last_bobber_x", global_x)  # This is used by the fishing routine
            ready = True
        self.set("ready", ready)

        shape_data = []
        # Add a rectangle to the overlay. UNLIKE OTHERS WE ARE DOING THIS WHETHER OR NOT WE ARE IN DEBUG MODE.
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

        # Add a circle to the overlay. UNLIKE OTHERS WE ARE DOING THIS WHETHER OR NOT WE ARE IN DEBUG MODE.
        if bobber_is_found:
            x, y = bobber_is_found
            shape_data.append(
                {
                    "type": "circle",
                    "key": "bobber_location",
                    "config": {
                        "x1": x - 5,
                        "y1": y - 5,
                        "x2": x + 5,
                        "y2": y + 5,
                        "outline": "blue",
                        "width": 2,  # Line thickness
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


bobber = Bobber()
