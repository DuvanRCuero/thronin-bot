from thronin.lib.logger import logger
import threading


class Temp:
    DEFAULTS = {
        "killswitch_engaged": False,
        "bot_is_running": False,
        "game_restarted": False,
        "current_routine": None,
        "cycles_without_los": 0,
        "cycles_without_target": 0,
        "screenshot": None,
        "window_size": 0,
        "window_xywh": None,
        "fps": 0,
        "action_log": "Loading...",
    }

    def __init__(self):
        self._temp = {}
        self.lock = threading.Lock()
        self.reset_to_defaults()

    def set(self, key, value):
        with self.lock:
            if key in self._temp:
                previous_value = self._temp[key]
                self._temp[key] = value
                if key not in ("screenshot"):
                    if previous_value != value:
                        if key == "action_log" and value not in (
                            "Nothing (Bot Disabled)"
                        ):
                            logger.info(value)
                        logger.debug(f"Set {key} to {value}")
            else:
                logger.error(f"{key} is not a valid temp")
                raise KeyError(f"{key} is not a valid temp")

    def get(self, key, default=None):
        with self.lock:
            value = self._temp.get(key, default)
            if value is None and key not in self._temp:
                logger.warning(f"{key} is not set, returning default value: {default}")
            return value

    def reset_to_defaults(self):
        with self.lock:
            self._temp = self.DEFAULTS.copy()
            logger.debug("Temp reset to default values.")
            logger.debug(f"{self._temp}")

    def raise_if_killswitch_engaged(self):
        if temp.get("killswitch_engaged"):
            logger.warning("Killswitch Engaged. Exiting Early.")
            raise KillswitchEngaged


class KillswitchEngaged(Exception):
    pass


# Instantiate and expose
temp = Temp()
