from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.lib.logger import logger
import ctypes
import time
import win32api
import win32con
import win32gui


class WindowManager:
    TITLE_BAR_HEIGHT = 31
    BORDER_WIDTH = 8
    WINDOW_CHECK_INTERVAL = 5  # seconds
    GAME_TITLE = "TL"

    def __init__(self):
        self.hwnd = None
        self.window_rect = {}
        ctypes.windll.user32.AllowSetForegroundWindow(-1)
        # self.initialize_window()
        logger.debug(f"WindowManager started")

    #######################################################################################################################
    # Private Functions
    #######################################################################################################################
    def initialize_window(self):
        """Initialize the game window and verify its dimensions."""
        self._find_window()

        # Verify window size
        # self._update_window_xywh()
        _, _, _, h = temp.get("window_xywh", (0, 0, 0, 0))
        if h not in (1080, 720):
            raise IncorrectWindowSize(h)

        # This allows the correct assets to be loaded.
        temp.set("window_size", h)
        temp.set("game_restarted", False)

    def _find_window(self):
        """Find the game window and retrieve its dimensions."""

        def window_enum_callback(hwnd, results):
            title = win32gui.GetWindowText(hwnd)
            if title.startswith(self.GAME_TITLE):  # Match any title starting with "TL"
                results.append(hwnd)

        windows = []
        win32gui.EnumWindows(window_enum_callback, windows)

        if not windows:
            raise RuntimeError(
                f"Failed to find window starting with '{self.GAME_TITLE}'"
            )

        self.hwnd = windows[0]
        logger.debug(f"Window found: '{self.GAME_TITLE}' ({self.hwnd})")
        self.bring_window_to_foreground()

        # Adjust the window rect to exclude title bar and borders
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.window_rect = {
            "left": left + self.BORDER_WIDTH,
            "top": top + self.TITLE_BAR_HEIGHT,
            "width": right - left - 2 * self.BORDER_WIDTH,
            "height": bottom - top - self.TITLE_BAR_HEIGHT - self.BORDER_WIDTH,
        }

        logger.debug(
            f"Dimensions: {self.window_rect['width']}x{self.window_rect['height']}"
        )
        logger.debug(f"Adjusted window dimensions: {self.window_rect}")
        x, y, w, h = (
            self.window_rect["left"],
            self.window_rect["top"],
            self.window_rect["width"],
            self.window_rect["height"],
        )
        temp.set("window_xywh", (x, y, w, h))

    def _is_window_minimized(self):
        """Check if the window is currently minimized using GetWindowPlacement."""
        try:
            # Get window placement, which includes window state
            placement = win32gui.GetWindowPlacement(self.hwnd)
            # placement[1] should be one of: SW_SHOWNORMAL, SW_SHOWMINIMIZED, SW_SHOWMAXIMIZED
            if placement[1] == win32con.SW_SHOWMINIMIZED:
                return True
            else:
                return False
        except Exception as e:
            logger.warning(f"Failed to check window state: {e}")
            return False  # If the check fails, assume it's not minimized

    def _simulate_user_input(self):
        """Simulate ALT key press to enable foreground window change."""
        win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Press ALT
        time.sleep(0.05)
        win32api.keybd_event(
            win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0
        )  # Release ALT

    #######################################################################################################################
    # Public Functions
    #######################################################################################################################
    def window_is_active(self):
        """Check if the window is currently active."""
        active_hwnd = win32gui.GetForegroundWindow()
        return self.hwnd == active_hwnd

    def bring_window_to_foreground(self):
        """Bring the window to the foreground, with fallback for minimized and inactive states."""
        if self._is_window_minimized():
            logger.debug("Window was minimized, restoring...")
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            time.sleep(1)  # Allow time for window to restore

        if not self.window_is_active():
            try:
                win32gui.SetForegroundWindow(self.hwnd)
                logger.debug("Window brought to foreground.")
            except Exception as e:
                logger.debug(f"Failed to bring window to foreground: {e}")
                logger.debug("Simulating user input as fallback.")
                self._simulate_user_input()
                try:
                    win32gui.SetForegroundWindow(self.hwnd)
                    logger.debug("Window brought to foreground.")
                except Exception as e:
                    logger.error(f"Failed to bring window to foreground: {e}")
                    raise e


window_manager = WindowManager()
