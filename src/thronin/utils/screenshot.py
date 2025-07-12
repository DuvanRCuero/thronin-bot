from thronin.global_variables.temp import temp
from thronin.lib.application_info import cache_path
from thronin.lib.logger import logger
from thronin.utils.cached_images import cached_images
import cv2 as cv
import datetime
import numpy as np
import os


class ScreenshotUtilities:

    def perform_template_matching(self, what_to_look_for, where_to_look, tolerance=1.0):
        # Cache the image if its not already
        cached_image = cached_images.get_cached_image(what_to_look_for)
        # Perform template matching
        result = cv.matchTemplate(where_to_look, cached_image, cv.TM_CCOEFF_NORMED)
        # Get the maximum value and its location
        _, max_val, _, max_loc = cv.minMaxLoc(result)
        # Check if the match is within tolerance
        found = max_val >= tolerance
        if found:
            # Get the dimensions of the template to define the bounding box
            template_height, template_width = cached_image.shape[:2]
            found_xywh = [max_loc[0], max_loc[1], template_width, template_height]
            match_result = {
                "found": True,
                "found_xywh": found_xywh,
                "confidence": max_val,
            }
        else:
            match_result = {
                "found": False,
                "found_xywh": [],
                "confidence": max_val,
            }
        logger.debug(f"Match Result: {match_result}")
        return match_result

    def apply_hsv_mask(self, image, lower_hsv, upper_hsv, return_with_mask=False):
        """Apply an HSV mask to an image."""
        # logger.debug(f"Applying HSV Mask: lower_hsv: {lower_hsv}")
        # logger.debug(f"Applying HSV Mask: upper_hsv: {upper_hsv}")
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, np.array(lower_hsv), np.array(upper_hsv))
        final_image = cv.bitwise_and(image, image, mask=mask)
        return (final_image, mask) if return_with_mask else final_image

    def invalid_screenshot(self, screenshot):
        if screenshot is None or not isinstance(screenshot, np.ndarray):
            return True
        return False

    def save_screenshot(self, name):
        screenshot = temp.get("screenshot")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        full_name = os.path.join(cache_path, f"{name}_{timestamp}.png")
        cv.imwrite(full_name, screenshot)
        logger.info(f"Screenshot saved: {full_name}")


# Pre-create an instance
screenshot_utils = ScreenshotUtilities()
