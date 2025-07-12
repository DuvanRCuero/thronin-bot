from thronin.lib.application_info import cache_path
from thronin.lib.logger import logger
import json
import os
import threading


class Cache:
    DEFAULTS = {
        "last_run_battle_pass": int(0),
        "last_run_guild_collection": int(0),
        "last_run_guild_recruitment": int(0),
        "last_run_kastleton": int(0),
        "last_run_safe_zone": int(0),
        "last_run_stonegard": int(0),
        "last_use_itemquickslot3": int(0),
        "last_use_itemquickslot4": int(0),
    }

    def __init__(self):
        self._cache = {}
        self.lock = threading.Lock()
        self.file_path = os.path.join(cache_path, "cache.json")
        self._load_from_file()

    def _load_from_file(self):
        with self.lock:
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r") as f:
                        loaded_cache = json.load(f)
                        self._cache.update(loaded_cache)
                        logger.debug("Caches loaded successfully from file.")
                except (json.JSONDecodeError, IOError) as e:
                    logger.error(f"Error loading caches from file: {e}")
            else:
                logger.debug(f"{self.file_path} not found. Using default caches.")

            # Add any missing default caches
            missing_defaults = {
                key: value
                for key, value in self.DEFAULTS.items()
                if key not in self._cache
            }
            if missing_defaults:
                self._cache.update(missing_defaults)
            logger.debug(f"Cache Loaded: {self._cache}")

    def _save_to_file(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self._cache, f, indent=4)
            logger.debug(f"Caches saved successfully.")
            logger.debug(f"{self._cache}")
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error saving caches: {e}")

    def set(self, key, value):
        with self.lock:
            if key in self._cache:
                self._cache[key] = value
                logger.debug(f"Set {key} to {type(value)}({value})")
                self._save_to_file()
            else:
                logger.error(f"{key} is not a valid cache")
                raise KeyError(f"{key} is not a valid cache")

    def get(self, key, default=None):
        with self.lock:
            value = self._cache.get(key, default)
            if value is None and key not in self._cache:
                logger.warning(f"{key} is not set, returning default value: {default}")
            return value

    def reset_to_defaults(self):
        with self.lock:
            self._cache = self.DEFAULTS.copy()
            logger.debug("Caches reset to default values.")
            logger.debug(f"{self._cache}")


cache = Cache()
