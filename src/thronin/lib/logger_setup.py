import logging
import queue
import os
import sys
import colorlog
from logging.handlers import QueueHandler



class LoggerSetup:
    def __init__(
        self,
        name="Thronin",
        log_file="cache/logfile.log",
        queue_level=logging.INFO,
        console_level=logging.DEBUG,
        file_level=logging.DEBUG,
    ):
        self.logger = colorlog.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.log_queue = queue.Queue()

        if not self.logger.handlers:  # Avoid duplicate handlers
            # Add handlers (ensure QueueHandler is first)
            self._add_queue_handler(queue_level)
            self._add_console_handler(console_level)
            self._add_file_handler(log_file, file_level)

    def _add_queue_handler(self, level):
        queue_handler = QueueHandler(self.log_queue)
        queue_handler.setLevel(level)
        queue_formatter = logging.Formatter(
            "%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        queue_handler.setFormatter(queue_formatter)
        self.logger.addHandler(queue_handler)

    def _add_console_handler(self, level):
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = CustomColoredFormatter(
            "%(asctime)s | %(log_color)s%(levelname)s | %(pathname)s | %(funcName)s || %(message)s%(reset)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "light_black",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self, log_file, level):
        file_handler = logging.FileHandler(
            self._get_filepath(log_file),
            mode="w",
        )
        file_handler.setLevel(level)
        file_formatter = CustomFormatter(
            "%(asctime)s | %(levelname)s | %(pathname)s | %(funcName)s || %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

    def get_log_queue(self):
        return self.log_queue

    def _get_filepath(self, relative_filepath: str) -> str:
        # Determine the base path
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")

        # Construct the absolute file path for the log file
        absolute_filepath = os.path.join(base_path, relative_filepath)

        # Ensure the directory exists
        directory = os.path.dirname(absolute_filepath)
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create directory {directory}: {e}")

        return absolute_filepath


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Get the full pathname
        full_path = record.pathname
        # Modify the pathname to start from 'thronin\src\thronin\'
        src_index = full_path.lower().find("thronin\\src\\thronin\\")
        if src_index != -1:
            # Slice the path to start from after 'thronin\src\thronin\'
            record.pathname = full_path[src_index + len("thronin\\src\\thronin\\") :]

            # Remove the .py extension from the pathname
            base, ext = os.path.splitext(record.pathname)
            record.pathname = base

        # Call the original formatter's format method to process the log message
        return super().format(record)


class CustomColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        # Get the full pathname
        full_path = record.pathname
        # Modify the pathname to start from 'thronin\src\thronin\'
        src_index = full_path.lower().find("thronin\\src\\thronin\\")
        if src_index != -1:
            # Slice the path to start from after 'thronin\src\thronin\'
            record.pathname = full_path[src_index + len("thronin\\src\\thronin\\") :]

            # Remove the .py extension from the pathname
            base, ext = os.path.splitext(record.pathname)
            record.pathname = base

        # Call the original formatter's format method to process the log message
        return super().format(record)
