from thronin.debug_mode import DEBUG_MODE

from thronin.lib.logger import logger
import copy
import threading
import time


class Tracker:
    def __init__(self, tracker_name):
        self.tracker_name = tracker_name
        self._variables = {
            "show_roi": False,
            "roi": None,
            "roi_window_active": False,
            "last_update": 0,
            "update_interval": 1,
            "enabled": False,
            "ready": False,
            "shapes": [],
        }
        self._lock = threading.Lock()

    def set(self, key, value):
        """Thread-safe setter method."""
        with self._lock:
            self._variables[key] = value

    def get(self, key, default=None):
        """Thread-safe getter method with default value support."""
        with self._lock:
            return copy.deepcopy(self._variables.get(key, default))

    def load(self):
        # Will override in subsclasses when needed.
        return

    def enable(self):
        self.set("enabled", True)
        self.set("last_update", 0)
        logger.debug(f"Enabled {self.tracker_name}")

    def disable(self):
        self.set("enabled", False)
        self.set("last_update", 0)
        logger.debug(f"Disabled {self.tracker_name}")

    #######################################################################################################################
    # Functions used by the trackers
    #######################################################################################################################
    def _allowed_to_update(self):
        """Check if the tracker is enabled and if the update interval has elapsed."""
        return bool(self.get("enabled")) and (
            time.time() - self.get("last_update")
        ) >= self.get("update_interval")
