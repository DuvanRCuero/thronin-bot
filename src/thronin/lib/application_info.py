from importlib.metadata import version
from thronin.lib.logger import logger
import os
import sys


class ApplicationInfo:
    def __init__(self):
        # Parse the version string and determine expiration
        version_str = version("thronin")
        version_parts = version_str.split(".")
        major = int(version_parts[0])
        minor = int(version_parts[1])
        patch = int(version_parts[2])

        # Create the application title
        application_title = f"Thronin v{version_str}"
        self.application_title = application_title

        if getattr(sys, "frozen", False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.abspath(".")

        self.cache_path = os.path.join(self.application_path, "cache")
        try:
            os.makedirs(self.cache_path, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create directory {self.cache_path}: {e}")

        try:
            self.source_path = sys._MEIPASS
        except Exception:
            self.source_path = os.path.abspath("./src/thronin")

        self.assets_path = os.path.join(self.source_path, "assets")
        self.ico_path = os.path.join(self.assets_path, "thronin.ico")

        logger.debug(f"Application Title: {self.application_title}")
        logger.debug(f"Version: {version_str}")
        logger.debug(f"Application Path: {self.application_path}")
        logger.debug(f"Cache Path: {self.cache_path}")
        logger.debug(f"Source Path: {self.source_path}")
        logger.debug(f"Assets Path: {self.assets_path}")
        logger.debug(f"ICO Path: {self.ico_path}")


# Instantiate and expose
appinfo = ApplicationInfo()
application_title = appinfo.application_title
application_path = appinfo.application_path
cache_path = appinfo.cache_path
source_path = appinfo.source_path
assets_path = appinfo.assets_path
ico_path = appinfo.ico_path
