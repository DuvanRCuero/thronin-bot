from thronin.global_variables.temp import temp
from thronin.lib.logger import logger
from thronin.lib.gui_manager import gui_manager
import psutil
import subprocess
import time
import win32con
import win32gui


class GameManager:
    TITLE_BAR_HEIGHT = 31
    BORDER_WIDTH = 8
    GAME_LAUNCH_WAIT_TIME = 60  # seconds
    CRASH_WAIT_TIME = 10  # seconds
    WINDOW_CHECK_INTERVAL = 5  # seconds

    def __init__(self):
        self.crash_window_title = "Unreal Engine 4 Crash Reporter"
        self.process_name = "TL.exe"
        self.steam_app_id = "2429640"
        self.steam_exe = r"C:\\Program Files (x86)\\Steam\\steam.exe"
        logger.debug(f"Game is Running: {self._game_is_running()}")

    def _game_is_running(self):
        return any(
            proc.info["name"].lower() == self.process_name.lower()
            for proc in psutil.process_iter(["pid", "name"])
        )

    # Check for the crash window, if its open close the crash windows
    def handle_game_crashed(self):
        def enum_windows_callback(hwnd, windows_list):
            """Callback function to collect windows with the specified title."""
            if self.crash_window_title in win32gui.GetWindowText(hwnd):
                windows_list.append(hwnd)

        # Find all windows with the crash window title
        crash_windows = []
        win32gui.EnumWindows(enum_windows_callback, crash_windows)

        if crash_windows:
            logger.warning(f"Detected crash window '{self.crash_window_title}'.")
            for hwnd in crash_windows:
                try:
                    logger.info(f"Closing crash window: {win32gui.GetWindowText(hwnd)}")
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                except Exception as e:
                    logger.error(f"Failed to close crash window: {e}")

            temp.set("current_routine", None)
            logger.info(
                f"Waiting {self.CRASH_WAIT_TIME} seconds for Steam to clean up."
            )
            time.sleep(self.CRASH_WAIT_TIME)

    def handle_game_not_running(self):
        if self._game_is_running():
            return

        gui_manager.hide_overlay()

        logger.warning(
            f"Process '{self.process_name}' not running, attempting to launch game."
        )
        temp.set("current_routine", None)
        self.handle_game_crashed()
        temp.set("action_log", "Launching Game")
        try:
            # Launch the game.
            subprocess.Popen([self.steam_exe, f"steam://rungameid/{self.steam_app_id}"])
            logger.info(f"Launching Steam game with App ID {self.steam_app_id}.")

            # Wait until the game process is detected or self.GAME_LAUNCH_WAIT_TIME seconds have passed.
            start_time = time.time()
            elapsed_time = 0
            while not self._game_is_running():
                temp.raise_if_killswitch_engaged()
                if elapsed_time >= self.GAME_LAUNCH_WAIT_TIME:
                    raise RuntimeError(
                        f"Game failed to start within {self.GAME_LAUNCH_WAIT_TIME} seconds."
                    )

                logger.info(
                    f"Waiting for game to start... {self.GAME_LAUNCH_WAIT_TIME - elapsed_time} seconds remaining."
                )
                time.sleep(self.WINDOW_CHECK_INTERVAL)
                elapsed_time = int(time.time() - start_time)

            # When the game is detected running for the first time,
            # wait an additional GAME_LAUNCH_WAIT_TIME seconds for the game to fully load,
            # checking every WINDOW_CHECK_INTERVAL seconds and reporting the time remaining.
            remaining_time = self.GAME_LAUNCH_WAIT_TIME
            while remaining_time > 0:
                temp.raise_if_killswitch_engaged()
                logger.info(
                    f"Game detected running; waiting {remaining_time} seconds for full initialization."
                )
                time.sleep(self.WINDOW_CHECK_INTERVAL)
                remaining_time -= self.WINDOW_CHECK_INTERVAL

            logger.info("Game should be fully loaded now.")
            temp.set("game_restarted", True)
            gui_manager.show_overlay()
        except Exception as e:
            raise RuntimeError(f"Failed to launch Steam game: {e}")


game_manager = GameManager()
