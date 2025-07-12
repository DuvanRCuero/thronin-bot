# DO NOT SORT THE FOLLOWING
from thronin.debug_mode import DEBUG_MODE, SUPER_DEBUG_MODE
from thronin.lib.logger import logger
from thronin.lib.application_info import application_title
from thronin.lib.splash_screen import splash_screen
from thronin.global_variables.temp import temp
from thronin.lib.game_manager import game_manager
from thronin.lib.window_manager import window_manager
from thronin.global_variables.assets import assets
from thronin.global_variables.trackers import trackers
from thronin.lib.player import player
from thronin.global_variables.routines import routines
from thronin.lib.gui_manager import gui_manager
from thronin.lib.processor import processor
from thronin.lib.screen_capture import screen_cap
from thronin.lib.prechecks import prechecks
from thronin.lib.thread_manager import thread_manager
from thronin.bot import bot
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
import time


class Application:
    DEBOUNCE_DELAY = 0.5  # 500 ms

    def __init__(self):
        splash_screen.update_status("Validating Tesseract installation...")
        prechecks.validate_tesseract()
        splash_screen.update_status("Checking Windows DPI...")
        prechecks.check_dpi_scaling()
        splash_screen.update_status("Verifying Throne and Liberty is running...")
        game_manager.handle_game_crashed()
        game_manager.handle_game_not_running()
        splash_screen.update_status("Click on Throne and Liberty!")
        window_manager.initialize_window()
        while temp.get("window_size") == 0:
            logger.debug("Waiting for WindowManager to finish.")
            time.sleep(0.1)
        splash_screen.update_status("Loading Assets...")
        assets.load_assets()
        splash_screen.update_status("Loading Trackers...")
        trackers.load()
        splash_screen.update_status("Loading Player...")
        player.load_player()
        splash_screen.update_status("Loading Routines...")
        routines.load()
        splash_screen.update_status("Finished")
        splash_screen.close_splash_screen()
        time.sleep(1)
        thread_manager.start_threads()
        kbm.setup_hotkeys(
            terminate_application=self._terminate_application_button_pressed,
            toggle_bot=bot.toggle,
            toggle_overlay=gui_manager.toggle_overlay,
        )
        logger.info(f"Application {application_title} initialized.")
        self.terminate_flag = False

    def _terminate_application_button_pressed(self):
        self.terminate_flag = True
        logger.debug(f"Terminate Flag Updated: {self.terminate_flag}")

    def _exit_application(self):
        logger.debug("Exit application initiated.")
        temp.set("killswitch_engaged", True)
        if kbm.hotkey_listener:
            kbm.hotkey_listener.stop()
        logger.debug("Hotkey listener stopped.")
        thread_manager.stop_threads()
        logger.info("Application exited successfully.")

    def run(self):
        fps_start_time = time.time()
        frame_count = 0

        while not self.terminate_flag:
            if gui_manager.exit_button_pressed:
                logger.warning("GUI was exited. Closing Application.")
                self.terminate_flag = True
                break

            # Validate game state
            game_manager.handle_game_crashed()
            game_manager.handle_game_not_running()
            if temp.get("game_restarted", False):
                assets.load_assets()
                trackers.load()
                player.load_player()
                routines.load()
                window_manager.initialize_window()
                continue

            # Update Overlay
            gui_manager.update()

            # if the window is not active do not process anything.
            # screen_cap.capture_screenshot() # USED FOR TESTING
            # processor.analyze_screenshot() # USED FOR TESTING
            if window_manager.window_is_active():
                screen_cap.capture_screenshot()
                processor.analyze_screenshot()
                frame_count += 1
                if time.time() - fps_start_time >= 1.0:
                    temp.set("fps", frame_count)
                    frame_count = 0
                    fps_start_time = time.time()
            else:
                logger.debug(f"Window is not active, skipping screen capture.")
                time.sleep(0.1)  # Prevent CPU over usage.

        self._exit_application()
