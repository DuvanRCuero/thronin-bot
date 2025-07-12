from mttkinter import mtTkinter as tk
from thronin.global_variables.temp import temp
from thronin.global_variables.trackers import trackers
from thronin.lib.logger import logger
import time


class DebugOverlay:

    def __init__(self, root):
        self.root = root
        self.overlay = None
        self.overlay_x = 0
        self.overlay_y = 0
        self.overlay_w = 0
        self.overlay_h = 0
        self.canvas = None
        self.shapes = {}
        self.cached_shapes = {}
        game_window_coords = temp.get("window_xywh")
        if not game_window_coords:
            raise SystemExit("Unable to retrieve window coords.")

        # Create a Toplevel overlay window.
        self.overlay = self._create_overlay()
        self.overlay_x, self.overlay_y, self.overlay_w, self.overlay_h = (
            game_window_coords
        )
        self.overlay.geometry(
            f"{self.overlay_w}x{self.overlay_h}+{self.overlay_x}+{self.overlay_y}"
        )

        # Create the canvas inside the overlay.
        self.canvas = self._create_canvas()

        # Make UI update every 200ms
        self.root.after(200, self.update)

    def _create_circle(self, circle_name, config):
        # Create an oval on the canvas and return its ID.
        return self.canvas.create_oval(
            config.get("x1"),
            config.get("y1"),
            config.get("x2"),
            config.get("y2"),
            outline=config.get("outline"),
            width=config.get("width"),
            tag=circle_name,
        )

    def _update_circle(self, shape_id, config):
        # Update circle coordinates and appearance.
        self.canvas.coords(
            shape_id,
            config.get("x1"),
            config.get("y1"),
            config.get("x2"),
            config.get("y2"),
        )
        self.canvas.itemconfig(
            shape_id,
            outline=config.get("outline"),
            width=config.get("width"),
        )

    def _create_rectangle(self, rect_name, config):
        # Create a rectangle on the canvas and return its ID.
        return self.canvas.create_rectangle(
            config.get("x1"),
            config.get("y1"),
            config.get("x2"),
            config.get("y2"),
            outline=config.get("outline"),
            width=config.get("width"),
            tag=rect_name,
        )

    def _update_rectangle(self, shape_id, config):
        # Update rectangle coordinates and appearance.
        self.canvas.coords(
            shape_id,
            config.get("x1"),
            config.get("y1"),
            config.get("x2"),
            config.get("y2"),
        )
        self.canvas.itemconfig(
            shape_id,
            outline=config.get("outline"),
            width=config.get("width"),
        )

    def _create_overlay(self):
        # Create a borderless, topmost overlay window.
        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)
        overlay.attributes("-transparentcolor", "purple")
        overlay.config(bg="purple")
        # overlay.attributes("-alpha", 0.2)
        return overlay

    def _create_canvas(self):
        # Create a canvas that fills the overlay.
        canvas = tk.Canvas(self.overlay, bg="purple", bd=0, highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        return canvas

    def update(self):
        # Skip updating if the overlay is not visible.
        if self.overlay.state() != "normal":
            return

        # Clear previous shapes so only current tracker shapes remain.
        self.shapes.clear()

        # Process shapes from each enabled tracker and update our self.shapes.
        for tracker_name, tracker in trackers.get_all().items():
            if not tracker.get("enabled"):
                continue

            tracker_shapes = tracker.get("shapes")
            if not tracker_shapes:
                continue
            # logger.warning(f"{tracker_name}: shapes: {tracker_shapes}")
            # tracker_shapes example:
            # [{'type': 'rectangle', 'key': 'bobber', 'config': {'x1': 438, 'y1': 83, 'x2': 842, 'y2': 237, 'outline': 'red', 'width': 2}}]

            for shape in tracker_shapes:
                # Expect each shape to be a dict with keys: "type", "key", "config"
                shape_type = shape.get("type")
                shape_key = shape.get("key")
                config = shape.get("config")
                if shape_type and shape_key and config:
                    self.shapes[shape_key] = {"type": shape_type, "config": config}
                else:
                    logger.debug(
                        f"Incomplete shape data from tracker {tracker_name}: {shape}"
                    )

        # #  DEBUG: Display contract regions.
        # if temp.get("window_size") == 720:
        #     contract_regions = [
        #         (445, 170, 163, 20),
        #         (635, 170, 163, 20),
        #         (445, 290, 163, 20),
        #         (635, 290, 163, 20),
        #         (445, 410, 163, 20),
        #         (635, 410, 163, 20),
        #         (445, 530, 163, 20),
        #         (635, 530, 163, 20),
        #     ]
        # elif temp.get("window_size") == 1080:
        #     contract_regions = [
        #         (668, 258, 245, 30),
        #         (953, 258, 245, 30),
        #         (668, 436, 245, 30),
        #         (953, 436, 245, 30),
        #         (668, 617, 245, 30),
        #         (953, 617, 245, 30),
        #         (668, 798, 245, 30),
        #         (953, 798, 245, 30),
        #     ]
        # count = 0
        # for xywh in contract_regions:
        #     self._create_rectangle(
        #         f"contract_{count}",
        #         {
        #             "x1": xywh[0],
        #             "y1": xywh[1],
        #             "x2": xywh[0] + xywh[2],
        #             "y2": xywh[1] + xywh[3],
        #             "outline": "red",
        #             "width": 2,
        #         },
        #     )
        #     count = count + 1

        # 1) For each shape in self.shapes, create or update the shape on the canvas.
        for key, shape_data in self.shapes.items():
            shape_type = shape_data.get("type")
            config = shape_data.get("config")

            if key in self.cached_shapes:
                # Update existing shape.
                if shape_type == "circle":
                    self._update_circle(self.cached_shapes[key], config)
                elif shape_type == "rectangle":
                    self._update_rectangle(self.cached_shapes[key], config)
                else:
                    logger.debug(f"Unsupported shape type for key {key}: {shape_type}")
            else:
                # Create new shape.
                if shape_type == "circle":
                    shape_id = self._create_circle(key, config)
                elif shape_type == "rectangle":
                    shape_id = self._create_rectangle(key, config)
                else:
                    logger.debug(f"Unsupported shape type for key {key}: {shape_type}")
                    continue
                self.cached_shapes[key] = shape_id

        # 2) Remove shapes from the canvas that are no longer needed.
        for key in list(self.cached_shapes.keys()):
            if key not in self.shapes:
                self.canvas.delete(self.cached_shapes[key])
                del self.cached_shapes[key]

        # Schedule the next update after 200ms.
        self.root.after(200, self.update)

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
