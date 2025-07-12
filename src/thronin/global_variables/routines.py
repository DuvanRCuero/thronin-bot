import threading
from thronin.lib.logger import logger

from thronin.routines.routine_abandonedstonemasontown import abandoned_stonemason_town
from thronin.routines.routine_akiduvalley import akidu_valley
from thronin.routines.routine_amitoihouse import amitoi_house
from thronin.routines.routine_battle import battle
from thronin.routines.routine_battle_assist import battle_assist
from thronin.routines.routine_battle_noexit import battle_noexit
from thronin.routines.routine_battle_party import battle_party
from thronin.routines.routine_blackhowlplains import blackhowl_plains
from thronin.routines.routine_caninavillage import canina_village
from thronin.routines.routine_carmineforest import carmine_forest
from thronin.routines.routine_daybreakshore import daybreak_shore
from thronin.routines.routine_death import death
from thronin.routines.routine_fishing import fishing
from thronin.routines.routine_fonosbasin import fonos_basin
from thronin.routines.routine_grayclawforest import grayclaw_forest
from thronin.routines.routine_inamitoihouse import in_amitoi_house
from thronin.routines.routine_inmenu import in_menu
from thronin.routines.routine_kastleton import kastleton
from thronin.routines.routine_kicked import kicked
from thronin.routines.routine_mainmenu import main_menu
from thronin.routines.routine_manawastes import manawastes
from thronin.routines.routine_monolithwastelands import monolith_wastelands
from thronin.routines.routine_moonlightdesert import moonlight_desert
from thronin.routines.routine_nestinggrounds import nesting_grounds
from thronin.routines.routine_purelight import purelight_hills
from thronin.routines.routine_ragingwilds import raging_wilds
from thronin.routines.routine_ruinsofturayne import ruins_of_turayne
from thronin.routines.routine_safezone import safe_zone
from thronin.routines.routine_selectcharacter import select_character
from thronin.routines.routine_shatteredtemple import shattered_temple
from thronin.routines.routine_stonegardcastle import stonegard_castle
from thronin.routines.routine_urstellafields import urstella_fields
from thronin.routines.routine_quietiss_demense import quietiss_demense
from thronin.routines.routine_forest_of_the_great_tree import forest_of_the_great_tree
from thronin.routines.routine_swampofsilence import swamp_of_silence
from thronin.routines.routine_blackanvil import black_anvil
from thronin.routines.routine_bercant_manor import bercant_manor

ROUTINE_LIST = [
    abandoned_stonemason_town,
    akidu_valley,
    amitoi_house,
    battle,
    battle_assist,
    battle_noexit,
    battle_party,
    blackhowl_plains,
    canina_village,
    carmine_forest,
    daybreak_shore,
    death,
    fishing,
    fonos_basin,
    grayclaw_forest,
    in_amitoi_house,
    in_menu,
    kastleton,
    kicked,
    main_menu,
    manawastes,
    monolith_wastelands,
    moonlight_desert,
    nesting_grounds,
    purelight_hills,
    raging_wilds,
    ruins_of_turayne,
    safe_zone,
    select_character,
    shattered_temple,
    stonegard_castle,
    urstella_fields,
    quietiss_demense,
    forest_of_the_great_tree,
    swamp_of_silence,
    black_anvil,
    bercant_manor,
]


class Routines:
    def __init__(self):
        self._routines = {}
        self.lock = threading.Lock()

    def load(self):
        with self.lock:
            for routine in ROUTINE_LIST:
                self._routines[routine.routine_name] = routine
            logger.debug(f"Loaded Routines: {self._routines}")

    def get(self, key, default=None):
        with self.lock:
            if key == "in_game":
                value = self._routines.get("battle", default)
            else:
                value = self._routines.get(key, default)
            if value is None and key not in self._routines:
                logger.warning(f"{key} is not set, returning default value: {default}")
            return value

    def get_all(self):
        with self.lock:
            return self._routines.copy()


routines = Routines()
