from thronin.debug_mode import DEBUG_MODE
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.lib.errors import IncorrectWindowSize
from thronin.lib.logger import logger
from thronin.trackers._base import Tracker
import numpy as np
import time


class TrackerQuickSlot(Tracker):
    def __init__(self, tracker_name):
        super().__init__(tracker_name)
        self.set("ready", True)
        self.set("update_interval", 0.5)
        self.set("press_time", 0.15)
        self.set("post_time", 0.5)

    def load(self):
        self.set(
            "casting_skill",
            options.get(f"{self.tracker_name}_casting_skill"),
        )
        self.set(
            "repetitions",
            options.get(f"{self.tracker_name}_repetitions"),
        )

    def analyze_screenshot(self, screenshot):
        # Ensure were allowed to update
        if not self._allowed_to_update():
            return

        # Load Config
        window_size = temp.get("window_size")
        if temp.get("window_size") not in [720, 1080, 1440]:
            raise IncorrectWindowSize(window_size)
        config = self.WINDOW_CONFIGS.get(window_size)

        # Extract parameters for the current location
        x, y, w, h = config.get("xywh")

        # Define search_region and modify image if needed
        search_region = screenshot[y : y + h, x : x + w]

        # Check if every pixel in the region is within tolerance of the target color.
        # logger.warning(
        #     f"{self.tracker_name}: {search_region}, looking for: {config.get("target_color")}"
        # )
        ready = np.all(
            np.abs(search_region - config.get("target_color"))
            <= config.get("tolerance")
        )
        self.set("ready", ready)

        shape_data = []
        # Add a rectangle to the overlay.
        if DEBUG_MODE:
            shape_data.append(
                {
                    "type": "rectangle",
                    "key": self.tracker_name,
                    "config": {
                        "x1": x - 2,
                        "y1": y - 2,
                        "x2": (x + w) + 2,
                        "y2": (y + h) + 2,
                        "outline": "green" if ready else "red",
                        "width": 2,  # Line thickness.
                    },
                }
            )

        # Update the shapes for our debug overlay
        self.set("shapes", shape_data)

        # Update ROI
        if self.get("show_roi"):
            self.set("roi", search_region)

        # Finished
        self.set("last_update", time.time())


class QuickSlot1(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [460, 706, 1, 1],
            "target_color": np.array([46, 59, 73]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [647, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [834, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot1")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_1")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot2(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [490, 706, 1, 1],
            "target_color": np.array([45, 62, 78]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [698, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [906, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot2")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_2")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot3(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [519, 706, 1, 1],
            "target_color": np.array([46, 63, 78]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [749, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [979, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot3")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_3")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot4(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [548, 706, 1, 1],
            "target_color": np.array([45, 62, 78]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [800, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1052, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot4")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_4")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot5(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [577, 706, 1, 1],
            "target_color": np.array([45, 62, 77]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [851, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1125, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot5")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_5")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot6(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [606, 706, 1, 1],
            "target_color": np.array([45, 62, 78]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [902, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1198, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot6")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_6")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot7(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [664, 706, 1, 1],
            "target_color": np.array([45, 62, 77]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1004, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1344, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot7")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_7")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot8(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [693, 706, 1, 1],
            "target_color": np.array([45, 62, 78]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1055, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1417, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot8")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_8")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot9(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [722, 706, 1, 1],
            "target_color": np.array([45, 62, 77]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1106, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1490, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot9")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_9")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot10(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [751, 706, 1, 1],
            "target_color": np.array([40, 52, 64]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1157, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1563, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot10")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_10")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot11(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [780, 706, 1, 1],
            "target_color": np.array([40, 52, 64]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1208, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1636, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot11")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_11")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class QuickSlot12(TrackerQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [810, 706, 1, 1],
            "target_color": np.array([49, 65, 82]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1259, 1054, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1708, 1402, 1, 1],
            "target_color": np.array([38, 51, 66]),
        },
    }

    def __init__(self):
        super().__init__("quickslot12")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_quick_slot_12")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


quickslot1 = QuickSlot1()
quickslot2 = QuickSlot2()
quickslot3 = QuickSlot3()
quickslot4 = QuickSlot4()
quickslot5 = QuickSlot5()
quickslot6 = QuickSlot6()
quickslot7 = QuickSlot7()
quickslot8 = QuickSlot8()
quickslot9 = QuickSlot9()
quickslot10 = QuickSlot10()
quickslot11 = QuickSlot11()
quickslot12 = QuickSlot12()


class TrackerItemQuickSlot(TrackerQuickSlot):
    def __init__(self, tracker_name):
        super().__init__(tracker_name)
        self.set("ready", True)
        self.set("update_interval", 1)
        self.set("press_time", 0.05)
        self.set("post_time", 0.1)

    def load(self):
        self.set("casting_skill", False)
        self.set("repetitions", 1)


class ItemQuickSlot1(TrackerItemQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [736, 670, 1, 1],
            "target_color": np.array([43, 59, 77]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1131, 992, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1526, 1314, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
    }

    def __init__(self):
        super().__init__("itemquickslot1")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_item_quick_slot_1")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class ItemQuickSlot2(TrackerItemQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [765, 670, 1, 1],
            "target_color": np.array([49, 69, 89]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1180, 992, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1595, 1314, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
    }

    def __init__(self):
        super().__init__("itemquickslot2")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_item_quick_slot_2")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class ItemQuickSlot3(TrackerItemQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [793, 670, 1, 1],
            "target_color": np.array([49, 69, 89]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1230, 992, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1667, 1314, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
    }

    def __init__(self):
        super().__init__("itemquickslot3")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_item_quick_slot_3")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


class ItemQuickSlot4(TrackerItemQuickSlot):
    WINDOW_CONFIGS = {
        720: {
            "tolerance": 10,
            "xywh": [821, 670, 1, 1],
            "target_color": np.array([49, 69, 89]),
        },
        1080: {
            "tolerance": 10,
            "xywh": [1279, 992, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
        1440: {
            "tolerance": 10,
            "xywh": [1737, 1314, 1, 1],
            "target_color": np.array([39, 52, 70]),
        },
    }

    def __init__(self):
        super().__init__("itemquickslot4")
        self.set("show_roi", False)

    def load(self):
        super().load()
        keybind = options.get_keybind("keybind_item_quick_slot_4")
        self.set("kb_button", keybind["key"])
        self.set("display", keybind["display"])


# Instantiate ItemQuickSlot 1-2
itemquickslot1 = ItemQuickSlot1()
itemquickslot2 = ItemQuickSlot2()
itemquickslot3 = ItemQuickSlot3()
itemquickslot4 = ItemQuickSlot4()
