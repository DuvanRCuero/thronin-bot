from thronin.global_variables.options import options
from thronin.global_variables.routines import routines
from thronin.global_variables.temp import temp, KillswitchEngaged
from thronin.lib.logger import logger
from thronin.lib.window_manager import window_manager
import time


class Bot:
    def __init__(self):
        self.running = True
        self.actually_running = True
        self.active = False

    def run(self):
        while self.running:
            self.actually_running = True
            if self.active:
                window_manager.bring_window_to_foreground()

                # Handle forced routines
                force_routine = options.get("force_routine")
                forced_txt = ""
                routine_name = temp.get("current_routine")
                if force_routine:
                    forced_txt = " (Forced)"
                    if routine_name not in (
                        "amitoi_house",
                        "kastleton",
                        "stonegard_castle",
                    ):
                        routine_name = force_routine

                # Skip routine if None
                if not routine_name:
                    logger.warning(f"Routine: {routine_name}, nothing to do.")
                    time.sleep(1)
                    continue

                # Run the routine
                routine = routines.get(routine_name)
                if routine:
                    message = "=========================="
                    message += f" Starting Routine: {routine_name}{forced_txt}"
                    logger.debug(message)
                    try:
                        routine.run()
                    except KillswitchEngaged:
                        logger.error("Killswitch Caught")
                        self.active = False
                        self.running = False
                    message = "=========================="
                    message += f" Ending Routine: {routine_name}{forced_txt}"
                    logger.debug(message)
                else:
                    raise ValueError(f"Routine '{routine_name}' not found")
            else:
                temp.set("action_log", "Nothing (Bot Disabled)")
                time.sleep(1)
        logger.debug(f"Run loop completed.")
        self.actually_running = False

    def toggle(self):
        self.active = not self.active
        temp.set("bot_is_running", self.active)
        logger.warning(f"Bot toggled. Active: {self.is_active()}")

    def stop(self):
        logger.debug("Stop Thread Initiated.")
        if self.is_active():
            self.toggle()
        self.running = False
        while self.actually_running:
            logger.warning(f"Waiting for bot to complete its run.")
            time.sleep(0.1)
        logger.debug("Stop Thread Complete.")

    def is_active(self):
        return self.active


bot = Bot()
