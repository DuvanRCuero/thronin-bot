import threading
from thronin.lib.logger import logger

from thronin.trackers.amitoi import amitoi
from thronin.trackers.bobber import bobber
from thronin.trackers.casting import casting
from thronin.trackers.death import death
from thronin.trackers.fish_on_line import fish_on_line
from thronin.trackers.fishing_pole_casted import fishing_pole_casted
from thronin.trackers.fishing_pole_equipped import fishing_pole_equipped
from thronin.trackers.health import health
from thronin.trackers.line_of_sight import line_of_sight
from thronin.trackers.mana import mana
from thronin.trackers.need_to_block import need_to_block
from thronin.trackers.party import party
from thronin.trackers.party_invite import party_invite
from thronin.trackers.pvp_z import pvp_z
from thronin.trackers.quick_slot import quickslot1
from thronin.trackers.quick_slot import quickslot2
from thronin.trackers.quick_slot import quickslot3
from thronin.trackers.quick_slot import quickslot4
from thronin.trackers.quick_slot import quickslot5
from thronin.trackers.quick_slot import quickslot6
from thronin.trackers.quick_slot import quickslot7
from thronin.trackers.quick_slot import quickslot8
from thronin.trackers.quick_slot import quickslot9
from thronin.trackers.quick_slot import quickslot10
from thronin.trackers.quick_slot import quickslot11
from thronin.trackers.quick_slot import quickslot12
from thronin.trackers.quick_slot import itemquickslot1
from thronin.trackers.quick_slot import itemquickslot2
from thronin.trackers.quick_slot import itemquickslot3
from thronin.trackers.quick_slot import itemquickslot4
from thronin.trackers.resources_nearby import resources_nearby
from thronin.trackers.target import target

TRACKER_LIST = [
    amitoi,
    bobber,
    casting,
    death,
    fish_on_line,
    fishing_pole_casted,
    fishing_pole_equipped,
    health,
    line_of_sight,
    mana,
    need_to_block,
    party,
    party_invite,
    pvp_z,
    quickslot1,
    quickslot2,
    quickslot3,
    quickslot4,
    quickslot5,
    quickslot6,
    quickslot7,
    quickslot8,
    quickslot9,
    quickslot10,
    quickslot11,
    quickslot12,
    itemquickslot1,
    itemquickslot2,
    itemquickslot3,
    itemquickslot4,
    resources_nearby,
    target,
]


class Trackers:
    def __init__(self):
        self._trackers = {}
        self.lock = threading.Lock()

    def load(self):
        with self.lock:
            for tracker in TRACKER_LIST:
                tracker.load()
                self._trackers[tracker.tracker_name] = tracker
            logger.debug(f"Loaded Trackers: {self._trackers}")

    def get(self, key, default=None):
        with self.lock:
            value = self._trackers.get(key, default)
            if value is None and key not in self._trackers:
                logger.warning(f"{key} is not set, returning default value: {default}")
            return value

    def get_all(self):
        with self.lock:
            return self._trackers.copy()


trackers = Trackers()
