DEFAULT_MONITOR = True
DEFAULT_CASTING = False
DEFAULT_TYPE = "Combat"  # can also be "Health Recovery" or "Mana Recovery"
DEFAULT_REPETITIONS = 1


class BowStaff:
    def __init__(self):
        self.label_name = "Bow/Staff"
        self.config = {
            "quickslot1_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot1_casting_skill": DEFAULT_CASTING,
            "quickslot1_type": DEFAULT_TYPE,
            "quickslot1_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot2_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot2_casting_skill": DEFAULT_CASTING,
            "quickslot2_type": DEFAULT_TYPE,
            "quickslot2_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot3_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot3_casting_skill": DEFAULT_CASTING,
            "quickslot3_type": DEFAULT_TYPE,
            "quickslot3_repetitions": 3,
            #
            "quickslot4_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot4_casting_skill": DEFAULT_CASTING,
            "quickslot4_type": DEFAULT_TYPE,
            "quickslot4_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot5_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot5_casting_skill": True,
            "quickslot5_type": DEFAULT_TYPE,
            "quickslot5_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot6_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot6_casting_skill": DEFAULT_CASTING,
            "quickslot6_type": DEFAULT_TYPE,
            "quickslot6_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot7_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot7_casting_skill": DEFAULT_CASTING,
            "quickslot7_type": DEFAULT_TYPE,
            "quickslot7_repetitions": 2,
            #
            "quickslot8_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot8_casting_skill": DEFAULT_CASTING,
            "quickslot8_type": DEFAULT_TYPE,
            "quickslot8_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot9_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot9_casting_skill": True,
            "quickslot9_type": DEFAULT_TYPE,
            "quickslot9_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot10_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot10_casting_skill": DEFAULT_CASTING,
            "quickslot10_type": "Health Recovery",
            "quickslot10_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot11_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot11_casting_skill": True,
            "quickslot11_type": "Mana Recovery",
            "quickslot11_repetitions": DEFAULT_REPETITIONS,
            #
            "quickslot12_monitored_by_bot": DEFAULT_MONITOR,
            "quickslot12_casting_skill": DEFAULT_CASTING,
            "quickslot12_type": "Health Recovery",
            "quickslot12_repetitions": DEFAULT_REPETITIONS,
        }
