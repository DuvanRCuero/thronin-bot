from thronin.global_variables.temp import temp
from thronin.global_variables.trackers import trackers
from thronin.lib.logger import logger
import cv2 as cv
import numpy as np
import time


class BotVision:
    """
    Provides real-time visualization and color masking (HSV-based) for bot operations.
    Allows live adjustment of color ranges through OpenCV trackbars, as well as
    displaying region-of-interest (ROI) windows from active trackers.
    """

    def __init__(self) -> None:
        """
        Initializes the BotVision class with default HSV boundaries and window names.
        """
        self.running: bool = False
        self.trackbar_window: str = "Bot Vision - Trackbars"
        self.output_window: str = "Bot Vision"

        # Default HSV range values
        self.h_min, self.s_min, self.v_min = 0, 0, 0
        self.h_max, self.s_max, self.v_max = 179, 255, 255

        # Mapping of trackbar names to their corresponding attributes and max range
        self.trackbar_mapping = {
            "HMin": ("h_min", 0, 179),
            "SMin": ("s_min", 0, 255),
            "VMin": ("v_min", 0, 255),
            "HMax": ("h_max", 179, 179),
            "SMax": ("s_max", 255, 255),
            "VMax": ("v_max", 255, 255),
        }

    def run(self) -> None:
        """
        Starts the vision loop:
        - Sets up trackbars in a dedicated window
        - Continuously captures the latest screenshot from `temp`
        - Applies an HSV mask and displays the result
        - Displays ROIs for active trackers
        """
        self.running = True
        self._setup_trackbar_window()

        while self.running:
            screenshot = temp.get("screenshot")
            if screenshot is not None:
                self._display_output(screenshot)

            # Allow some minimal CPU rest
            # Also a convenient place to potentially check for user keypress if desired
            cv.waitKey(1)
        logger.debug(f"Run loop completed.")

    def stop(self) -> None:
        """
        Gracefully stops the BotVision process:
        - Allows the loop to exit
        - Destroys OpenCV windows after a short delay
        """
        self.running = False
        time.sleep(1)
        cv.destroyAllWindows()

    def _setup_trackbar_window(self) -> None:
        """
        Creates a trackbar window in OpenCV for dynamically adjusting HSV thresholds.
        The trackbars update instance attributes via a simple lambda callback.
        """
        cv.namedWindow(self.trackbar_window, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.trackbar_window, 300, 400)

        for trackbar_name, (
            attribute,
            default,
            max_val,
        ) in self.trackbar_mapping.items():
            cv.createTrackbar(
                trackbar_name,
                self.trackbar_window,
                default,
                max_val,
                lambda value, attr=attribute: setattr(self, attr, value),
            )

    def _display_output(self, screenshot: np.ndarray) -> None:
        """
        Displays the processed bot vision output and any relevant ROIs from trackers.

        :param screenshot: The raw image (BGR) to be displayed and masked.
        """
        # Apply the HSV mask/filter
        image = self._apply_hsv_mask(screenshot)

        # Optionally zoom image for easier viewing
        height, width = image.shape[:2]
        if height <= 720:
            zoom_factor = 1.5
            image = cv.resize(
                image, (int(width * zoom_factor), int(height * zoom_factor))
            )
        cv.imshow(self.output_window, image)

        # Show Tracker ROIs if the tracker is active and ROI display is requested
        for tracker_name, tracker in trackers.get_all().items():
            if tracker.get("enabled") and tracker.get("show_roi"):
                roi = tracker.get("roi")
                if isinstance(roi, np.ndarray):
                    # If the window for this ROI isn't marked as active, mark it
                    if not tracker.get("roi_window_active"):
                        tracker.set("roi_window_active", True)
                    self._display_roi(tracker_name, roi)
            else:
                # If a window is marked active but tracker or show_roi has been disabled
                if tracker.get("roi_window_active"):
                    logger.debug(f"Destroying ROI window for: {tracker_name}")
                    tracker.set("roi_window_active", False)
                    cv.destroyWindow(f"{tracker_name} - ROI")

    def _apply_hsv_mask(self, image: np.ndarray) -> np.ndarray:
        """
        Converts the input BGR image to HSV, applies an in-range filter using
        trackbar-based min/max thresholds, and returns the masked image.

        :param image: BGR image to be color-filtered.
        :return: Masked image in BGR space.
        """
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        mask = cv.inRange(
            hsv,
            (self.h_min, self.s_min, self.v_min),
            (self.h_max, self.s_max, self.v_max),
        )
        return cv.bitwise_and(image, image, mask=mask)

    def _display_roi(self, tracker_name: str, roi_image: np.ndarray) -> None:
        """
        Displays a region-of-interest (ROI) in a separate OpenCV window,
        scaled up if necessary.

        :param tracker_name: Name of the tracker to use in the window title.
        :param roi_image: The image array representing the ROI.
        """
        height, width = roi_image.shape[:2]
        # Ensure that the ROI is displayed at a minimum 30px dimension in either axis
        zoom_factor = max(30 / width, 30 / height, 1)
        zoomed = cv.resize(
            roi_image, (int(width * zoom_factor), int(height * zoom_factor))
        )
        cv.imshow(f"{tracker_name} - ROI", zoomed)


bot_vision = BotVision()
