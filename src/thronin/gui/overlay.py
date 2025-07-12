from mttkinter import mtTkinter as tk
from thronin.global_variables.cache import cache
from thronin.global_variables.options import options
from thronin.global_variables.temp import temp
from thronin.global_variables.trackers import trackers
from thronin.lib.errors import IncorrectWindowSize
from thronin.lib.logger import logger
from tkinter import font
import time


class Overlay:

    def __init__(self, root, application_title):
        self.application_title = application_title
        self.previous_game_window_coords = None
        self.sections = {}
        self.last_routine = None
        if temp.get("window_size") == 720:
            self._update_fonts("Calibri", 9, 8)
            self.popout_wrapper_width = 228
        elif temp.get("window_size") == 1080:
            self._update_fonts("Calibri", 12, 11)
            self.popout_wrapper_width = 402
        else:
            raise IncorrectWindowSize(temp.get("window_size"))
        self.overlay = self._create_overlay(root)
        self.canvas = self._create_canvas()
        self.popout_wrapper = self._create_popout_wrapper()

    def _update_fonts(self, font_family, title_size, standard_size):
        # self.font_family = font_family
        self.font_title = font.Font(family=font_family, size=title_size, underline=1)
        self.font_standard = font.Font(family=font_family, size=standard_size)
        self.font_underline = font.Font(
            family=font_family, size=standard_size, underline=1
        )
        self.font_strikeout = font.Font(
            family=font_family, size=standard_size, overstrike=1
        )

    def _create_overlay(self, root):
        overlay = tk.Toplevel(root)
        overlay.attributes("-topmost", True)
        overlay.attributes("-transparentcolor", "purple")
        overlay.overrideredirect(True)
        overlay.geometry("0x0+1+1")
        overlay.config(bg="purple")
        return overlay

    def _create_canvas(self):
        canvas = tk.Canvas(self.overlay, bg="purple", bd=0, highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        return canvas

    def _create_popout_wrapper(self):
        popout_wrapper = tk.Frame(
            self.overlay, bg="black", width=self.popout_wrapper_width
        )
        popout_wrapper.place(
            relx=0, rely=1, anchor="sw", width=self.popout_wrapper_width
        )
        popout_wrapper.grid_columnconfigure(0, weight=1)
        return popout_wrapper

    def _update_overlay_position(self, game_window_coords):
        if game_window_coords != self.previous_game_window_coords:
            logger.debug("Repositioning Overlay")
            x, y, width, height = game_window_coords
            self.overlay.geometry(f"{width}x{height}+{x}+{y}")
            self.previous_game_window_coords = game_window_coords

    def _destroy_unused_sections(self, used_sections):
        # Identify and destroy unused sections
        for section_name in list(self.sections.keys()):
            if section_name not in used_sections:
                logger.debug(f"Destroying unused section: {section_name}")

                # Get the section details
                section = self.sections[section_name]

                # Destroy all labels in content and title frames
                if section["title"]["labels"]:
                    for label in section["title"]["labels"].values():
                        label.destroy()
                if section["content"]["labels"]:
                    for label in section["content"]["labels"].values():
                        label.destroy()

                # Destroy the frames (content and title)
                if section["title"]["frame"]:
                    section["title"]["frame"].destroy()
                if section["content"]["frame"]:
                    section["content"]["frame"].destroy()

                # Destroy the wrapper frame
                section["wrapper"].destroy()

                # Remove the section from the dictionary
                del self.sections[section_name]

    def _create_section_if_needed(
        self, section_name, window_wrapper_row, include_title_frame=True
    ):
        # Initialize section dictionary if not present
        if section_name not in self.sections:
            self.sections[section_name] = {
                "wrapper": tk.Frame(),
                "title": {
                    "frame": None if not include_title_frame else tk.Frame(),
                    "labels": {} if include_title_frame else None,
                },
                "content": {
                    "frame": tk.Frame(),
                    "labels": {},
                },
            }

            # Position this section in the popout_wrapper
            self.sections[section_name]["wrapper"] = tk.Frame(
                master=self.popout_wrapper
            )
            self.sections[section_name]["wrapper"].grid(
                row=window_wrapper_row, column=0, sticky="nsew", pady=0
            )
            self.popout_wrapper.grid_rowconfigure(window_wrapper_row, weight=1)
            self.sections[section_name]["wrapper"].grid_columnconfigure(0, weight=1)

            # Optional Row 0 - Title Frame
            if include_title_frame:
                self.sections[section_name]["title"]["frame"] = tk.Frame(
                    master=self.sections[section_name]["wrapper"], bg="black"
                )
                self.sections[section_name]["title"]["frame"].grid(
                    row=0, column=0, sticky="nsew"
                )
                self.sections[section_name]["title"]["frame"].grid_columnconfigure(
                    0, weight=1
                )

            # Row 1 - Content Frame
            content_row = 1 if include_title_frame else 0
            self.sections[section_name]["content"]["frame"] = tk.Frame(
                master=self.sections[section_name]["wrapper"], bg="black"
            )
            self.sections[section_name]["content"]["frame"].grid(
                row=content_row, column=0, sticky="nsew"
            )

    def _create_label(self, parent, **label_options):
        label_options_with_defaults = {
            "fg": "grey",
            "bg": "black",
            "font": self.font_standard,
            "padx": 0,
            "pady": 0,
            "anchor": "w",
            "relief": "flat",
        }
        label_options_with_defaults.update(label_options)
        return tk.Label(parent, **label_options_with_defaults)

    def _update_or_create_label(self, key, parent, text, row, column, **label_options):
        frame = parent.get("frame")
        labels = parent.get("labels")
        label = labels.get(key)
        if not label:
            label = self._create_label(frame, text=text, **label_options)
            label.grid(row=row, column=column, sticky="w")
            parent["labels"].update({key: label})
        else:
            label.config(text=text, **label_options)

    #######################################################################################################################
    # Public Functions
    #######################################################################################################################
    def toggle_overlay(self):
        if self.overlay.state() == "normal":
            self.hide_overlay()
        else:
            self.show_overlay()

    def hide_overlay(self):
        self.overlay.withdraw()  # Hide the overlay
        logger.debug("Overlay hidden.")

    def show_overlay(self):
        self.overlay.deiconify()  # Show the overlay
        logger.debug("Overlay shown.")

    def update(self):
        # Check if the overlay is visible (normal state) before updating
        if self.overlay.state() != "normal":
            return  # Skip updating if the overlay is not visible

        game_window_coords = temp.get("window_xywh")

        if not game_window_coords or len(game_window_coords) != 4:
            logger.error("Game window coordinates not found.")
            return

        self._update_overlay_position(game_window_coords)
        self.canvas.delete("all")

        # Update the children, adding frames and labels if needed.
        self._update_stats_window(window_wrapper_row=0)
        used_sections = {"stats_section"}
        next_window_wrapper_row = 1
        current_routine = temp.get("current_routine")
        if self.last_routine != current_routine:
            self._destroy_unused_sections(used_sections)
            self.last_routine = current_routine

        # Add Player windows in battle
        if str(current_routine).startswith("battle") or str(current_routine).startswith(
            "in_game"
        ):
            self._update_player_window(window_wrapper_row=1)
            self._update_battle_window(window_wrapper_row=2)
            self._update_cooldowns_window(window_wrapper_row=3)
            used_sections.update(
                [
                    "player_section",
                    "battle_section",
                    "cooldowns_section",
                ]
            )
            next_window_wrapper_row = 4

        self._update_other_trackers_window(window_wrapper_row=next_window_wrapper_row)
        used_sections.update(["other_trackers_section"])

    #######################################################################################################################
    # Stats Window
    #######################################################################################################################
    def _update_stats_window(self, window_wrapper_row):
        # Create Section Wrapper with Frames for title and content.
        section_name = "stats_section"
        self._create_section_if_needed(
            section_name=section_name,
            window_wrapper_row=window_wrapper_row,
        )

        # Adjust Title
        self._update_or_create_label(
            key="application_title",
            parent=self.sections[section_name]["title"],
            text=self.application_title,
            row=0,
            column=0,
            fg="white",
            font=self.font_title,
        )

        # Update Labels
        current_row = 0
        current_column = 0
        # New Label
        color = "grey"
        self._update_or_create_label(
            key="keybind_start_stop_bot",
            parent=self.sections[section_name]["content"],
            text=f"{options.get_keybind("keybind_start_stop_bot")["display"]}: Start/Stop the bot",
            row=current_row,
            column=current_column,
            fg=color,
        )
        current_row += 1
        # New Label
        color = "grey"
        self._update_or_create_label(
            key="keybind_kill_bot",
            parent=self.sections[section_name]["content"],
            text=f"{options.get_keybind("keybind_kill_bot")["display"]}: Kill the bot",
            row=current_row,
            column=current_column,
            fg=color,
        )
        current_row += 1
        # New Label
        color = "grey"
        self._update_or_create_label(
            key="keybind_toggle_overlay",
            parent=self.sections[section_name]["content"],
            text=f"{options.get_keybind("keybind_toggle_overlay")["display"]}: Toggle Overylay",
            row=current_row,
            column=current_column,
            fg=color,
        )
        current_row += 1
        # New Label
        bot_is_running = temp.get("bot_is_running")
        color = "green" if bot_is_running else "red"
        self._update_or_create_label(
            key="bot_is_running",
            parent=self.sections[section_name]["content"],
            text=f"Running: {bot_is_running}",
            row=current_row,
            column=current_column,
            fg=color,
        )
        current_row += 1
        # New Label
        self._update_or_create_label(
            key="action_log_label",
            parent=self.sections[section_name]["content"],
            text=f"Action: {temp.get('action_log', 'None')}",
            row=current_row,
            column=current_column,
            fg="white",
        )
        current_row += 1
        # New Label
        self._update_or_create_label(
            key="routine_label",
            parent=self.sections[section_name]["content"],
            text=f"Routine: {temp.get('current_routine', 'None')}",
            row=current_row,
            column=current_column,
            fg="white",
        )
        current_row += 1
        # New Label
        self._update_or_create_label(
            key="fps_label",
            parent=self.sections[section_name]["content"],
            text=f"FPS: {temp.get('fps', 'None')}",
            row=current_row,
            column=current_column,
            fg="white",
        )
        current_row += 1

    #######################################################################################################################
    # Player Window
    #######################################################################################################################
    def _update_player_window(self, window_wrapper_row):
        # Create Section Wrapper with Frames for title and content.
        section_name = "player_section"
        self._create_section_if_needed(
            section_name=section_name,
            window_wrapper_row=window_wrapper_row,
        )

        # Adjust Title
        self._update_or_create_label(
            key="player_section_title_label",
            parent=self.sections[section_name]["title"],
            text=f"Player: ",
            row=0,
            column=0,
            fg="white",
            font=self.font_underline,
        )

        # Update Labels
        current_row = 0
        current_column = 0

        wanted_trackers = {
            "health": "Health",
            "mana": "Mana",
        }
        for tracker_name, tracker in trackers.get_all().items():
            if tracker_name in wanted_trackers.keys():
                # New Label
                self._update_or_create_label(
                    key=f"{tracker_name}_label_title",
                    parent=self.sections[section_name]["content"],
                    text=f"{wanted_trackers.get(tracker_name)}:",
                    row=current_row,
                    column=current_column,
                    fg="grey",
                )
                self.sections[section_name]["content"]["frame"].grid_columnconfigure(
                    current_column, weight=0
                )
                current_column += 1
                # New Label
                percentage = tracker.get("percentage")
                percentage *= 100
                color = "green" if percentage > 30 else "red4"
                font_to_use = self.font_standard
                if not tracker.get("enabled"):
                    color = "grey15"
                    font_to_use = self.font_strikeout
                self._update_or_create_label(
                    key=f"{tracker_name}_label",
                    parent=self.sections[section_name]["content"],
                    text=f"{int(percentage)}%",
                    row=current_row,
                    column=current_column,
                    fg=color,
                    font=font_to_use,
                )
                self.sections[section_name]["content"]["frame"].grid_columnconfigure(
                    current_column, weight=1
                )
                current_column += 1
                # # move to next row - comment above if using.
                # current_column = 0
                # current_row += 1

    #######################################################################################################################
    # Battle Window
    #######################################################################################################################
    def _update_battle_window(self, window_wrapper_row):
        # Create Section Wrapper with Frames for title and content.
        section_name = "battle_section"
        self._create_section_if_needed(
            section_name=section_name,
            window_wrapper_row=window_wrapper_row,
            include_title_frame=False,
        )

        # Update Labels
        current_row = 0
        current_column = 0

        # New Labels
        wanted_trackers = {
            "target": "TARGET",
            "line_of_sight": "LOS",
            "casting": "CASTING",
            "need_to_block": "BLOCK",
            "pvp_z": "COUNTER",
        }
        for tracker_name, tracker in trackers.get_all().items():
            if tracker_name in wanted_trackers.keys():
                color = "green3" if tracker.get("ready") else "red4"
                font_to_use = self.font_standard
                if not tracker.get("enabled"):
                    color = "grey15"
                    font_to_use = self.font_strikeout
                self._update_or_create_label(
                    key=f"{tracker_name}_label",
                    parent=self.sections[section_name]["content"],
                    text=wanted_trackers.get(tracker_name),
                    row=current_row,
                    column=current_column,
                    fg=color,
                    font=font_to_use,
                )
                # Evenly space columns
                self.sections[section_name]["content"]["frame"].grid_columnconfigure(
                    current_column, weight=1
                )
                current_column += 1

    #######################################################################################################################
    # Cooldowns Window
    #######################################################################################################################
    def _update_cooldowns_window(self, window_wrapper_row):
        # Create Section Wrapper with Frames for title and content.
        section_name = "cooldowns_section"
        self._create_section_if_needed(
            section_name=section_name,
            window_wrapper_row=window_wrapper_row,
            include_title_frame=False,
        )
        # Update Labels
        current_row = 0
        current_column = 0
        # New Label
        self._update_or_create_label(
            key="cooldowns_skills_title_label",
            parent=self.sections[section_name]["content"],
            text=f"⚔",
            row=current_row,
            column=current_column,
            fg="grey",
        )
        current_column += 1
        # New Labels
        for tracker_name, tracker in trackers.get_all().items():
            if tracker_name.startswith("quickslot"):
                color = "green" if tracker.get("ready") else "grey"
                self._update_or_create_label(
                    key=f"{tracker_name}_label",
                    parent=self.sections[section_name]["content"],
                    text=tracker.get("display"),
                    row=current_row,
                    column=current_column,
                    fg=color,
                )
                current_column += 1
        # New Label
        self._update_or_create_label(
            key="cooldowns_items_spacer_label",
            parent=self.sections[section_name]["content"],
            text=f"",
            row=current_row,
            column=current_column,
            fg="black",
            padx=4,
        )
        current_column += 1
        # New Label
        self._update_or_create_label(
            key="cooldowns_items_title_label",
            parent=self.sections[section_name]["content"],
            text=f"⛏",
            row=current_row,
            column=current_column,
            fg="grey",
        )
        current_column += 1
        # New Labels
        for tracker_name, tracker in trackers.get_all().items():
            if tracker_name.startswith("itemquickslot"):
                color = "green" if tracker.get("ready") else "grey"
                self._update_or_create_label(
                    key=f"{tracker_name}_label",
                    parent=self.sections[section_name]["content"],
                    text=tracker.get("display"),
                    row=current_row,
                    column=current_column,
                    fg=color,
                )
                current_column += 1

    #######################################################################################################################
    # Other Trackers Window
    #######################################################################################################################
    def _update_other_trackers_window(self, window_wrapper_row):
        # Create Section Wrapper with Frames for title and content.
        section_name = "other_trackers_section"
        self._create_section_if_needed(
            section_name=section_name,
            window_wrapper_row=window_wrapper_row,
        )

        # Adjust Title
        self._update_or_create_label(
            key=f"{section_name}_title_label",
            parent=self.sections[section_name]["title"],
            text=f"Other Trackers:",
            row=0,
            column=0,
            fg="white",
            font=self.font_underline,
        )

        # Update Labels
        current_row = 0
        current_column = 0

        # Determine Labels to use by Current Routine
        current_routine = temp.get("current_routine")
        wanted_trackers = {}
        match current_routine:
            case "battle" | "in_game":
                wanted_trackers = {
                    "amitoi": "Amitoi Ready",
                    "death": "Player Dead",
                    "resources_nearby": "Nearby Resources",
                }
            case "battle_assist":
                wanted_trackers = {}
            case "battle_noexit":
                wanted_trackers = {
                    "resources_nearby": "Nearby Resources",
                }
            case "battle_party":
                wanted_trackers = {
                    "party": "In Party",
                    "party_invite": "Invite Pending",
                }
            case "fishing":
                wanted_trackers = {
                    "bobber": "Bobber",
                    "fishing_pole_equipped": "Fishing Pole Equipped",
                    "fishing_pole_casted": "Fishing Pole Casted",
                    "fish_on_line": "Fish on Line",
                }
            case "safe_zone":
                wanted_trackers = {
                    "amitoi": "Amitoi Ready",
                }
            case _:
                wanted_trackers = {}
        if wanted_trackers == {}:
            self._update_or_create_label(
                key=f"no_trackers_label",
                parent=self.sections[section_name]["content"],
                text=f"No additional trackers needed for this routine.",
                row=current_row,
                column=current_column,
                fg="grey",
            )
            return
        for tracker_name, tracker in trackers.get_all().items():
            if tracker_name in wanted_trackers.keys():
                # Check for the specific case of "amitoi"
                if tracker_name == "amitoi":
                    if options.get("perform_amitoi") == False:
                        text = f"Farm Amitoi Never"
                        color = "grey"  # Set color for "Never" text
                        self._update_or_create_label(
                            key=f"{tracker_name}_label",
                            parent=self.sections[section_name]["content"],
                            text=text,
                            row=current_row,
                            column=current_column,
                            fg=color,
                        )
                        self.sections[section_name]["content"][
                            "frame"
                        ].grid_columnconfigure(current_column, weight=1)
                        current_row += 1
                        continue  # Skip further timer processing for this specific case

                color = "green3" if tracker.get("ready") else "red4"
                font_to_use = self.font_standard
                if not tracker.get("enabled"):
                    color = "grey15"
                    font_to_use = self.font_strikeout
                self._update_or_create_label(
                    key=f"{tracker_name}_label",
                    parent=self.sections[section_name]["content"],
                    text=f"{wanted_trackers.get(tracker_name)}",
                    row=current_row,
                    column=current_column,
                    fg=color,
                    font=font_to_use,
                )
                # Evenly space columns
                self.sections[section_name]["content"]["frame"].grid_columnconfigure(
                    current_column, weight=1
                )
                current_row += 1

        wanted_timers = {}
        match current_routine:
            case "battle" | "in_game":
                wanted_timers = {
                    "last_run_safe_zone": {
                        "last_run": cache.get("last_run_safe_zone"),
                        "interval": options.get("perform_safe_zone_every"),
                        "prefix": "Farm Safe Zone",
                    },
                }
            case "safe_zone":
                wanted_timers = {
                    "last_run_battle_pass": {
                        "last_run": cache.get("last_run_battle_pass"),
                        "interval": options.get("perform_battle_pass_every"),
                        "prefix": "Farm Battle Pass",
                    },
                    "last_run_guild_collection": {
                        "last_run": cache.get("last_run_guild_collection"),
                        "interval": options.get("perform_guild_collection_every"),
                        "prefix": "Perform Guild Collection",
                    },
                    "last_run_guild_recruitment": {
                        "last_run": cache.get("last_run_guild_recruitment"),
                        "interval": options.get("perform_guild_recruitment_every"),
                        "prefix": "Perform Guild Recruitment",
                    },
                    "last_run_kastleton": {
                        "last_run": cache.get("last_run_kastleton"),
                        "interval": options.get("perform_kastleton_every"),
                        "prefix": "Perform Kastleton (Storage)",
                    },
                    "last_run_stonegard": {
                        "last_run": cache.get("last_run_stonegard"),
                        "interval": options.get("perform_stonegard_every"),
                        "prefix": "Perform Stonegard Castle",
                    },
                }
            case _:
                wanted_timers = {}
        for tracker_name, timer_data in wanted_timers.items():
            last_run = timer_data["last_run"]
            interval = timer_data["interval"]
            prefix = timer_data["prefix"]

            # Check for the specific case of "Farm Battle Pass"
            if prefix == "Farm Battle Pass":
                if options.get("perform_battle_pass") == False:
                    text = f"{prefix} Never"
                    color = "grey"  # Set color for "Never" text
                    self._update_or_create_label(
                        key=f"{tracker_name}_label",
                        parent=self.sections[section_name]["content"],
                        text=text,
                        row=current_row,
                        column=current_column,
                        fg=color,
                    )
                    self.sections[section_name]["content"][
                        "frame"
                    ].grid_columnconfigure(current_column, weight=1)
                    current_row += 1
                    continue  # Skip further timer processing for this specific case
            # Check for the specific case of "Perform Guild Collection"
            if prefix == "Perform Guild Collection":
                if options.get("perform_guild_collection") == False:
                    text = f"{prefix} Never"
                    color = "grey"  # Set color for "Never" text
                    self._update_or_create_label(
                        key=f"{tracker_name}_label",
                        parent=self.sections[section_name]["content"],
                        text=text,
                        row=current_row,
                        column=current_column,
                        fg=color,
                    )
                    self.sections[section_name]["content"][
                        "frame"
                    ].grid_columnconfigure(current_column, weight=1)
                    current_row += 1
                    continue  # Skip further timer processing for this specific case
            # Check for the specific case of "Perform Guild Recruitment"
            if prefix == "Perform Guild Recruitment":
                if options.get("perform_guild_recruitment") == False:
                    text = f"{prefix} Never"
                    color = "grey"  # Set color for "Never" text
                    self._update_or_create_label(
                        key=f"{tracker_name}_label",
                        parent=self.sections[section_name]["content"],
                        text=text,
                        row=current_row,
                        column=current_column,
                        fg=color,
                    )
                    self.sections[section_name]["content"][
                        "frame"
                    ].grid_columnconfigure(current_column, weight=1)
                    current_row += 1
                    continue  # Skip further timer processing for this specific case
            # Check for the specific case of "Perform Kastleton (Storage)"
            if prefix == "Perform Kastleton (Storage)":
                if options.get("perform_kastleton") == False:
                    text = f"{prefix} Never"
                    color = "grey"  # Set color for "Never" text
                    self._update_or_create_label(
                        key=f"{tracker_name}_label",
                        parent=self.sections[section_name]["content"],
                        text=text,
                        row=current_row,
                        column=current_column,
                        fg=color,
                    )
                    self.sections[section_name]["content"][
                        "frame"
                    ].grid_columnconfigure(current_column, weight=1)
                    current_row += 1
                    continue  # Skip further timer processing for this specific case
            # Check for the specific case of "Perform Stonegard Castle"
            if prefix == "Perform Stonegard Castle":
                if options.get("perform_stonegard") == False:
                    text = f"{prefix} Never"
                    color = "grey"  # Set color for "Never" text
                    self._update_or_create_label(
                        key=f"{tracker_name}_label",
                        parent=self.sections[section_name]["content"],
                        text=text,
                        row=current_row,
                        column=current_column,
                        fg=color,
                    )
                    self.sections[section_name]["content"][
                        "frame"
                    ].grid_columnconfigure(current_column, weight=1)
                    current_row += 1
                    continue  # Skip further timer processing for this specific case

            if last_run is not None and interval is not None:
                next_run = last_run + interval
                current_time = time.time()
                time_until_next_run = max(0, next_run - current_time)
                color = "grey"

                if time_until_next_run == 0:
                    text = f"{prefix} Now"
                    color = "white"
                else:
                    hours, remainder = divmod(time_until_next_run, 3600)
                    minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
                    human_readable = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                    text = f"{prefix} in {human_readable}"

                self._update_or_create_label(
                    key=f"{tracker_name}_label",
                    parent=self.sections[section_name]["content"],
                    text=text,
                    row=current_row,
                    column=current_column,
                    fg=color,
                )
                self.sections[section_name]["content"]["frame"].grid_columnconfigure(
                    current_column, weight=1
                )
                current_row += 1
