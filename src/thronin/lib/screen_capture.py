from thronin.lib.logger import logger
import cv2 as cv
import mss
import numpy as np
from thronin.global_variables.temp import temp


class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()

    def capture_screenshot(self):
        try:
            xywh = temp.get("window_xywh")
            if not xywh:
                raise ValueError(
                    "Window dimensions not found; cannot capture screenshot."
                )
            x, y, w, h = xywh
            screenshot = self.sct.grab({"left": x, "top": y, "width": w, "height": h})
            img_bgr = cv.cvtColor(np.array(screenshot), cv.COLOR_BGRA2BGR)
            temp.set("screenshot", img_bgr)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            temp.set("screenshot", None)


screen_cap = ScreenCapture()
