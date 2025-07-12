from pathlib import Path
from thronin.global_variables.temp import temp
from thronin.lib.application_info import assets_path
from thronin.lib.logger import logger
from typing import Dict
import os
import threading


class Assets:

    def __init__(self):
        self._assets = {}
        self.lock = threading.Lock()

    def load_assets(self):
        with self.lock:
            self._assets = {
                "contracts": self._get_files_dict("contracts"),
                "locations": self._get_files_dict("locations", recursive=True),
                "shopping": self._get_files_dict("shopping"),
                "trackers": self._get_files_dict("trackers"),
                "vendors": self._get_files_dict("vendors"),
            }

    def get(self, key, subkey, default=None):
        with self.lock:
            assets_dict = self._assets.get(key)
            if assets_dict is None or subkey not in assets_dict:
                logger.warning(
                    f"{'Key' if assets_dict is None else 'Subkey'} '{key if assets_dict is None else subkey}' "
                    f"not found, returning default: {default}"
                )
                return default
            return assets_dict[subkey]

    def get_all(self, key: str) -> Dict[str, str]:
        with self.lock:
            if key not in self._assets:
                logger.warning(f"Key '{key}' not found in assets.")
                return {}
            return self._assets[key].copy()

    def _get_files_dict(self, folder: str, recursive: bool = False) -> Dict[str, str]:
        window_size = temp.get("window_size")
        directory = os.path.join(assets_path, str(window_size))
        folder_path = Path(directory) / folder
        files_dict = {}
        if recursive:
            files = folder_path.rglob("*")  # Recursively list all files
        else:
            files = folder_path.glob("*")  # Only list files in the top-level folder
        for file_path in files:
            if file_path.is_file():  # Only process files
                file_name_without_ext = file_path.stem
                files_dict[file_name_without_ext] = str(file_path)
                logger.debug(
                    f"Importing Asset: self._assets.{folder}[{file_name_without_ext}] = {file_path}"
                )
        return files_dict


assets = Assets()
