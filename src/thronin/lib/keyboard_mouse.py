from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.global_variables.trackers import trackers
from thronin.lib.logger import logger
import pyautogui
import pyperclip
import re
import string
import time


class KeyboardMouse:
    def __init__(self):
        self.keyboard = KeyboardController()
        self.last_hotkey_press_time = {}
        self.DEBOUNCE_DELAY = 0.5  # seconds
        self.hotkey_listener = None
        # Store callbacks so that we can restart the listener later.
        self._hotkey_callbacks = None

    def release_friendly_target(self):
        with self.keyboard.pressed(Key.ctrl):
            time.sleep(0.1)
            self.keyboard.press(options.get_keybind_key("keybind_clear_target"))
            time.sleep(0.1)
            self.keyboard.release(options.get_keybind_key("keybind_clear_target"))
            time.sleep(0.1)

    def use_keyboard(
        self,
        kb_button,
        press_time=0.2,
        post_time=0.6,
        casting_skill=False,
        modifier=None,
    ):
        logger.debug(
            f"kb_button: {kb_button}, press_time: {press_time}, "
            f"post_time: {post_time}, casting_skill: {casting_skill}, "
            f"modifier: {modifier}"
        )

        if modifier:
            self.keyboard.press(modifier)
            time.sleep(0.1)

        self.keyboard.press(kb_button)

        if casting_skill:
            casting_tracker = trackers.get("casting")
            casting_tracker.set("update_interval", 0)
            start_time = time.time()
            time.sleep(1)
            while casting_tracker.get("ready"):
                elapsed_time = time.time() - start_time
                logger.debug(f"Casting Detected: {elapsed_time:.2f}")
                time.sleep(0.1)
                if elapsed_time > 10:
                    casting_tracker.set("ready", False)
                    logger.warning(f"Casting Stopped: {elapsed_time:.2f}")
            casting_tracker.set("update_interval", 99999999999)
            logger.debug(f"Casting Completed: {time.time() - start_time:.2f}")
        else:
            time.sleep(press_time)

        self.keyboard.release(kb_button)

        if modifier:
            time.sleep(0.1)
            self.keyboard.release(modifier)

        if post_time != 0:
            time.sleep(post_time)

    def run_and_jump(self, time_to_perform=1):
        logger.debug(f"running and jumping for {time_to_perform} seconds")
        # Morph to move faster
        self.use_keyboard(Key.shift)
        # Hold forward key and jump for time_to_perform
        self.keyboard.press(options.get_keybind_key("keybind_move_forward"))
        start_time = time.time()
        while time.time() - start_time < time_to_perform:
            self.keyboard.tap(options.get_keybind_key("keybind_jump"))
            time.sleep(0.3)
        self.keyboard.release(options.get_keybind_key("keybind_move_forward"))

    def type_with_kb(self, msg):
        logger.debug(f"Typing: {msg}")
        self.keyboard.type(msg)

    def set_message_to_clipboard(self, message):
        pyperclip.copy(message)

    def paste_with_kb(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press("v")
        self.keyboard.release("v")
        self.keyboard.release(Key.ctrl)
        time.sleep(0.1)

    def reset_camera(self):
        self.keyboard.press(Key.down)
        start_time = time.time()
        while time.time() - start_time < 1.5:
            pyautogui.scroll(-500)
            time.sleep(0.1)
        self.keyboard.release(Key.down)

    def setup_hotkeys(self, terminate_application, toggle_bot, toggle_overlay):
        self._hotkey_callbacks = (terminate_application, toggle_bot, toggle_overlay)
        keybind_kill_bot = options.get_keybind_key("keybind_kill_bot")
        keybind_start_stop_bot = options.get_keybind_key("keybind_start_stop_bot")
        keybind_toggle_overlay = options.get_keybind_key("keybind_toggle_overlay")
        if (
            not keybind_kill_bot
            or not keybind_start_stop_bot
            or not keybind_toggle_overlay
        ):
            raise SystemExit("Need to set Keybinds")

        def on_press(key):
            try:
                if key == keybind_kill_bot:
                    logger.debug(f"Kill Bot Keybind Pressed: {keybind_kill_bot}")
                    terminate_application()
                elif key == keybind_start_stop_bot:
                    logger.debug(
                        f"Start/Stop Keybind Pressed: {keybind_start_stop_bot}"
                    )
                    toggle_bot()
                elif key == keybind_toggle_overlay:
                    logger.debug(
                        f"Toggle Overlay Keybind Pressed: {keybind_toggle_overlay}"
                    )
                    toggle_overlay()
            except AttributeError:
                pass

        self.hotkey_listener = keyboard.Listener(on_press=on_press)
        self.hotkey_listener.start()
        logger.debug("Hotkey listener started.")

    def stop_hotkeys(self):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
            self.hotkey_listener = None
            logger.debug("Hotkey listener stopped.")

    def restart_hotkeys(self):
        self.stop_hotkeys()
        if self._hotkey_callbacks:
            terminate_application, toggle_bot, toggle_overlay = self._hotkey_callbacks
            self.setup_hotkeys(terminate_application, toggle_bot, toggle_overlay)
            logger.debug("Hotkey listener restarted.")

    #######################################################################################################################
    # MOUSE FUNCTIONALITY
    #######################################################################################################################
    def reset_mouse(self):
        logger.debug("Resetting Mouse")
        self.move_mouse(5, 5, duration_to_move=0.1)

    def move_mouse(
        self, x, y, click=False, hold_shift=False, num_clicks=1, duration_to_move=0.45
    ):
        window_x, window_y, _, _ = temp.get("window_xywh")
        screen_x = x + window_x
        screen_y = y + window_y
        logger.debug(f"Moving mouse to {screen_x}, {screen_y}. Click: {click}")
        pyautogui.moveTo(screen_x, screen_y, duration=duration_to_move)
        if hold_shift:
            self.keyboard.press(Key.shift)
        if click:
            for i in range(num_clicks):
                pyautogui.click()
                time.sleep(0.2)
        if hold_shift:
            self.keyboard.release(Key.shift)


keyboard_mouse = KeyboardMouse()
