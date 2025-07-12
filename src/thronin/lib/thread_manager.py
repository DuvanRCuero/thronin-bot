from thronin.debug_mode import DEBUG_MODE, SUPER_DEBUG_MODE
from thronin.lib.logger import logger
import threading
from thronin.lib.gui_manager import gui_manager
from thronin.output import bot_vision
from thronin.bot import bot
from mttkinter import mtTkinter as tk


class ThreadManager:
    def _start_thread(self, target, name):
        thread = threading.Thread(target=target, daemon=True, name=name)
        thread.start()
        logger.debug(f"{name} started.")

    def start_threads(self):
        self._start_thread(target=gui_manager.run, name="GUI Thread")
        self._start_thread(target=bot.run, name="Bot Thread")
        if SUPER_DEBUG_MODE:
            self._start_thread(target=bot_vision.run, name="Bot Vision Thread")

    def stop_threads(self):
        if SUPER_DEBUG_MODE:
            bot_vision.stop()
        bot.stop()
        gui_manager.stop()


thread_manager = ThreadManager()
