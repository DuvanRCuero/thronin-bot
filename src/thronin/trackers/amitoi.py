from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.lib.logger import logger
from thronin.trackers._base import Tracker
import numpy as np
import time


class Amitoi(Tracker):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 5,
            "stage_1_xywh_list": [
                (1079, 17, 1, 1),  # slot 1 was 1102
                (1079, 38, 1, 1),  # slot 2
                (1079, 59, 1, 1),  # slot 3
                (1079, 81, 1, 1),  # slot 4
            ],
            "stage_1_target_colors": [
                np.array([170, 43, 124]),
                np.array([170, 43, 125]),
                np.array([170, 43, 125]),  # was 140, 36, 102
                np.array([170, 43, 124]),
            ],
            "stage_2_xywh_list": [
                (1089, 17, 1, 1),  # was 1113
                (1089, 38, 1, 1),
                (1089, 59, 1, 1),
                (1089, 81, 1, 1),
            ],
            "stage_2_target_colors": [
                np.array([25, 18, 157]),  # was 18, 18, 148
                np.array([25, 18, 157]),  # was 18, 18, 148
                np.array([25, 18, 157]),  # was 18, 18, 148
                np.array([25, 18, 157]),  # was 18, 18, 148
            ],
        },
        1080: {
            "tolerance": 5,
            "stage_1_xywh_list": [
                (1569, 30, 1, 1),  # was 1609
                (1569, 67, 1, 1),
                (1569, 105, 1, 1),
                (1569, 142, 1, 1),
            ],
            "stage_1_target_colors": [
                np.array([170, 43, 124]),
                np.array([170, 43, 124]),
                np.array([170, 43, 124]),
                np.array([170, 43, 124]),
            ],
            "stage_2_xywh_list": [
                (1585, 30, 1, 1),  # was 1626
                (1585, 67, 1, 1),
                (1585, 105, 1, 1),
                (1585, 142, 1, 1),
            ],
            "stage_2_target_colors": [
                np.array([21, 18, 151]),  # was 20, 13, 125
                np.array([21, 18, 151]),
                np.array([21, 18, 151]),
                np.array([21, 18, 151]),
            ],
        },
    }

    def __init__(self):
        super().__init__("amitoi")
        self.set("show_roi", False)
        self.set("update_interval", 60)

    def _process_stage(self, screenshot, xywh, target_color, tolerance, stage_num):
        """Check if a stage passes and log the results."""
        x, y, w, h = xywh
        search_region = screenshot[y : y + h, x : x + w]
        pixel_value = search_region[0, 0]
        stage_1_result = np.all(np.abs(pixel_value - target_color) <= tolerance)
        # logger.warning(
        #     f"{self.tracker_name}: stage_{stage_num}_result: {stage_1_result}, pixel_value: {pixel_value}, target_color: {target_color}"
        # )
        return stage_1_result

    def analyze_screenshot(self, screenshot):
        """Analyzes the screenshot to determine if Amitoi condition is met."""
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") not in [720, 1080, 1440]:
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        is_ready = False
        row_num = 1
        shape_data = []
        for stage_1_xywh, stage_1_color, stage_2_xywh, stage_2_color in zip(
            config.get("stage_1_xywh_list"),
            config.get("stage_1_target_colors"),
            config.get("stage_2_xywh_list"),
            config.get("stage_2_target_colors"),
        ):
            # Check stage 1 (purple at top of button)
            stage_1_result = self._process_stage(
                screenshot, stage_1_xywh, stage_1_color, config.get("tolerance"), 1
            )
            # search_region = stage_1_xywh
            x, y, w, h = stage_1_xywh
            # Add a rectangle to the overlay.
            if DEBUG_MODE:
                shape_data.append(
                    {
                        "type": "rectangle",
                        "key": f"{self.tracker_name}_stage1_{row_num}",
                        "config": {
                            "x1": x - 2,
                            "y1": y - 2,
                            "x2": (x + w) + 2,
                            "y2": (y + h) + 2,
                            "outline": "green" if stage_1_result else "red",
                            "width": 2,  # Line thickness.
                        },
                    }
                )

            # Check stage 2 if stage 1 found (red in top right corner of button)
            if stage_1_result:
                stage_2_result = self._process_stage(
                    screenshot, stage_2_xywh, stage_2_color, config.get("tolerance"), 2
                )
                x, y, w, h = stage_2_xywh
                # Add a rectangle to the overlay.
                if DEBUG_MODE:
                    shape_data.append(
                        {
                            "type": "rectangle",
                            "key": f"{self.tracker_name}_stage2_{row_num}",
                            "config": {
                                "x1": x - 2,
                                "y1": y - 2,
                                "x2": (x + w) + 2,
                                "y2": (y + h) + 2,
                                "outline": "green" if stage_2_result else "red",
                                "width": 2,  # Line thickness.
                            },
                        }
                    )
                if stage_2_result:
                    is_ready = True
                    logger.debug("Match found. Stopping further checks.")
                    break
            # Increment Row Counter for next check
            row_num += 1

        # Set Result
        self.set("ready", is_ready)

        # Update the shapes for our debug overlay
        self.set("shapes", shape_data)

        # # # Update ROI
        # if self.get("show_roi"):
        #     self.set("roi", search_region)

        self.set("last_update", time.time())


amitoi = Amitoi()
