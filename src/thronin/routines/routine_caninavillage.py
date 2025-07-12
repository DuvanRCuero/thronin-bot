from difflib import SequenceMatcher
from thronin.global_variables.assets import assets
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from thronin.routines._base import Routine
from thronin.utils.screenshot import screenshot_utils
import cv2 as cv
import numpy as np
import pytesseract
import re
import time
from pynput.keyboard import Key


class CaninaVillageRoutine(Routine):
    def __init__(self):
        super().__init__("canina_village")
        self._required_trackers = []
        self.pretty_name = "Canina Village"
        self.search_name = "canina"
        self.map_tp_coords = {
            720: [641, 321],
            1080: [962, 472],
        }
        self.contract_regions = {
            720: [
                (445, 170, 163, 20),
                (635, 170, 163, 20),
                (445, 290, 163, 20),
                (635, 290, 163, 20),
                (445, 410, 163, 20),
                (635, 410, 163, 20),
                (445, 530, 163, 20),
                (635, 530, 163, 20),
            ],
            1080: [
                (668, 258, 245, 30),
                (953, 258, 245, 30),
                (668, 436, 245, 30),
                (953, 436, 245, 30),
                (668, 617, 245, 30),
                (953, 617, 245, 30),
                (668, 798, 245, 30),
                (953, 798, 245, 30),
            ],
        }
        self._contract_count = 0
        self._contract_rights_count = 0
        self.wanted_contracts = [
            "A Deadly Dance",
            "A Dwarf's Sad Story",
            "Avellan Luxury Goods",
            "Border Sentries",
            "Collect Rogue Tokens",
            "Confront the Kowazan Clan",
            "Crossing the Line",
            "Expensive Wolf Fur",
            "Fighters' Duel",
            "Forest Bounty",
            "Gray Wolves Hunting",
            "Harsh Punishment",
            "Howling Provocateurs",
            "Hunting Gray Wolves",
            "Keeping the Faith",
            "Kowazan Clan Wolves",
            "Loyal Grayclaws",
            "Lycan Bounty",
            "Lycan's Ambition",
            "Only Bad Owners",
            "Ornate Brushes",
            "Prevent the Expansion",
            "Raised by Werewolves",
            "Rise of the Lycan Clan",
            "Senseless Beasts",
            "Smash Their Ambitions",
            "Something Precious",
            "Southward Bound Wolves",
            "Stop the Lycans",
            "Subdue the Beast",
            "Symbol of Pride",
            "The Butcher's Protections",
            "Totem Guardians",
            "Vengeful Bloodbath",
            "Werewolf's Conviction",
            "Wolf, Draw Your Sword!",
            "Wolf's Pride",
        ]

    def run(self):
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        time.sleep(1)
        x, y = self.map_tp_coords.get(temp.get("window_size"), [0, 0])
        if not self._teleport(self.pretty_name, self.search_name, x, y):
            self._complete_routine(next_routine=None)
            return
        temp.raise_if_killswitch_engaged()
        # Move forward to reveal the merchants
        temp.set("action_log", "Traveling to the Contract Manager")
        kbm.use_keyboard(Key.right, press_time=0.6)
        time.sleep(0.3)
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(options.get_keybind_key("keybind_move_forward"), press_time=4)
        time.sleep(0.3)
        temp.raise_if_killswitch_engaged()
        kbm.use_keyboard(Key.right, press_time=0.6)
        time.sleep(0.3)
        temp.raise_if_killswitch_engaged()

        # Search and interact with Contract Manager
        vendor_not_found = False
        if self._travel_to_vendor("contract-manager"):
            in_contract_vendor = assets.get("contracts", "in_contract_vendor")
            found = self._find_and_click_target(in_contract_vendor)
            if not found:
                logger.error(f"Cannot verify we are in the contract manager window.")
                vendor_not_found = True
            logger.info("Verified we are in vendor window.")
            temp.raise_if_killswitch_engaged()

            # Click Contract List Button
            if temp.get("window_size") == 720:
                kbm.move_mouse(218, 91, click=True)
                temp.raise_if_killswitch_engaged()
            elif temp.get("window_size") == 1080:
                kbm.move_mouse(327, 134, click=True)
                temp.raise_if_killswitch_engaged()

            # Start Shopping
            still_shopping = True
            max_attempts = 20  # Define the maximum number of loop executions
            attempts = 0  # Initialize the attempts counter
            shopping_list = self.wanted_contracts.copy()  # Copy the wanted contracts
            temp.set("action_log", "Looking for Contracts")
            while still_shopping and attempts < max_attempts:
                temp.raise_if_killswitch_engaged()
                still_shopping = self._perform_shopping(shopping_list)
                attempts += 1  # Increment the counter
                if still_shopping == False or attempts >= max_attempts:
                    time.sleep(0.5)
                    kbm.use_keyboard(Key.esc)
                    time.sleep(0.5)

            logger.info("Resetting wanted contracts to default.")
            shopping_list = self.wanted_contracts.copy()  # Reset after shopping

        if vendor_not_found:
            self._handle_vendor_not_found()
            return  # Restart the routine

        temp.set("action_log", "Traveling to Storage Manager")
        kbm.use_keyboard(Key.right, press_time=1)
        temp.raise_if_killswitch_engaged()
        if self._travel_to_vendor("storage-manager"):
            self._deposit_items()
            kbm.use_keyboard(Key.esc)
            time.sleep(0.5)
        else:
            self._handle_vendor_not_found()
            return  # Restart the routine

        temp.raise_if_killswitch_engaged()
        temp.set("action_log", "Fixing Contracts")
        kbm.use_keyboard(options.get_keybind_key("keybind_questlog"))
        time.sleep(0.25)
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        kbm.use_keyboard(Key.esc)
        time.sleep(0.25)

        self._complete_routine(next_routine="grayclaw_forest")

    def _perform_shopping(self, shopping_list):
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        temp.raise_if_killswitch_engaged()
        accepted_contract = self._accept_contracts(shopping_list)
        if accepted_contract:
            time.sleep(0.5)
            return True

        logger.info("No contracts accepted.")
        if not self._can_accept_contracts():
            return False
        temp.raise_if_killswitch_engaged()
        can_refresh = self._get_refresh_status()
        if can_refresh:
            temp.set("action_log", "Refreshing contracts")
            self._click_refresh_button()
            logger.debug("Resetting wanted contracts to default.")
            shopping_list = self.wanted_contracts.copy()  # Reset after shopping
            return True
        temp.raise_if_killswitch_engaged()
        logger.info("Cannot refresh contracts. Exiting.")
        # IF we still have contract rights.
        if not self._contract_rights_at_0():
            if not options.get("drop_contract_when_none_available"):
                logger.info("Skipping accept/abandon quest.")
                return False
            logger.info("Attempting to accept/abandon quest.")
            # Click first contract and accept
            xywh = self.contract_regions.get(temp.get("window_size"))[0]
            contract_name = self._detect_text(xywh)
            logger.debug(f"Accepting Contract to recycle: {contract_name}")
            contract_to_recycle = []
            contract_to_recycle.append(contract_name)
            click_x = xywh[0] + (xywh[2] / 2)
            click_y = xywh[1] + (xywh[3] / 2)
            kbm.move_mouse(click_x, click_y, click=True)
            temp.raise_if_killswitch_engaged()
            self._click_accept_button()
            temp.raise_if_killswitch_engaged()
            # Go to second tab. Abandon first shown contract.
            if temp.get("window_size") == 720:
                kbm.move_mouse(379, 91, click=True)
            elif temp.get("window_size") == 1080:
                kbm.move_mouse(569, 134, click=True)
            temp.raise_if_killswitch_engaged()
            # Find the accepted contract for recyclying and abandon it by using the same location as accept button
            abandoned_contract = self._accept_contracts(contract_to_recycle)
            kbm.use_keyboard(options.get_keybind_key("keybind_accept"), post_time=1)
            temp.raise_if_killswitch_engaged()
            # Go back to first tab.
            if temp.get("window_size") == 720:
                kbm.move_mouse(218, 91, click=True)
            elif temp.get("window_size") == 1080:
                kbm.move_mouse(327, 134, click=True)
            return True
        return False

    def _accept_contracts(self, shopping_list):
        if not self._can_accept_contracts():
            return False

        contract_regions = self.contract_regions.get(temp.get("window_size"))

        def is_similar(name1, name2, threshold=0.7):
            return SequenceMatcher(None, name1, name2).ratio() > threshold

        for xywh in contract_regions:
            temp.raise_if_killswitch_engaged()
            contract_name = self._detect_text(xywh)
            logger.debug(f"Detected Contract: {contract_name}")
            for wanted in shopping_list:
                if is_similar(contract_name, wanted):
                    click_x = xywh[0] + (xywh[2] / 2)
                    click_y = xywh[1] + (xywh[3] / 2)
                    kbm.move_mouse(click_x, click_y, click=True)
                    if not self._contract_already_signed():
                        self._click_accept_button()
                        logger.info(f"Accepted contract: {contract_name}")
                        shopping_list.remove(wanted)  # Remove from the list
                        return True
                    else:
                        logger.warning(f"{contract_name} is already signed, skipping.")
        return False

    def _click_refresh_button(self):
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(624, 674, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(936, 1019, click=True)
        time.sleep(0.15)
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        time.sleep(0.15)

    def _click_accept_button(self):
        temp.raise_if_killswitch_engaged()
        if temp.get("window_size") == 720:
            kbm.move_mouse(1025, 674, click=True)
        elif temp.get("window_size") == 1080:
            kbm.move_mouse(1538, 1019, click=True)
        time.sleep(0.15)
        temp.raise_if_killswitch_engaged()
        kbm.reset_mouse()
        time.sleep(0.15)

    def _detect_text(self, xywh):
        screenshot = temp.get("screenshot")
        x, y, w, h = xywh
        search_region = screenshot[y : y + h, x : x + w]
        gray_image = cv.cvtColor(np.array(search_region), cv.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image, lang="eng").strip()
        return text

    def _detect_number(self, xywh):
        screenshot = temp.get("screenshot")
        x, y, w, h = xywh
        search_region = screenshot[y : y + h, x : x + w]
        gray_image = cv.cvtColor(np.array(search_region), cv.COLOR_BGR2GRAY)
        custom_config = r"--psm 6 -c tessedit_char_whitelist=0123456789"
        text = pytesseract.image_to_string(gray_image, config=custom_config).strip()
        cleaned_text = re.sub(r"/.*", "", text)
        if cleaned_text == "o":
            detection = 0
        else:
            try:
                detection = int(cleaned_text)
            except ValueError:
                detection = 0
        log_results = {
            "Extracted Text": text,
            "Cleaned Text": cleaned_text,
            "Detection": detection,
        }
        return log_results

    def _get_refresh_status(self):
        results = screenshot_utils.perform_template_matching(
            assets.get("contracts", "contract-cannot-refresh"),
            temp.get("screenshot"),
            0.95,
        )
        logger.debug(results)
        return not results["found"]

    def _contract_already_signed(self):
        results = screenshot_utils.perform_template_matching(
            assets.get("contracts", "contract-already-signed"),
            temp.get("screenshot"),
            0.95,
        )
        logger.debug(results)
        return results["found"]

    def _contracts_at_max(self):
        logger.debug("Checking for max contracts.")
        results = screenshot_utils.perform_template_matching(
            assets.get("contracts", "contractcount_5"),
            temp.get("screenshot"),
            0.95,
        )
        logger.debug(results)
        return results["found"]

    def _contract_rights_at_0(self):
        logger.debug("Checking if contract rights at 0.")
        results = screenshot_utils.perform_template_matching(
            assets.get("contracts", "contractrights_0"),
            temp.get("screenshot"),
            0.97,
        )
        logger.debug(results)
        return results["found"]

    def _can_accept_contracts(self):
        if self._contract_rights_at_0():
            logger.warning("Can NOT accept contracts: 0 Contract Rights.")
            return False
        if self._contracts_at_max():
            logger.warning("Can NOT accept contracts: Max Contracts.")
            return False
        logger.debug("Can accept contracts.")
        return True


canina_village = CaninaVillageRoutine()
