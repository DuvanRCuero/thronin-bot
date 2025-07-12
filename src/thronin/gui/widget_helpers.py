import tkinter as tk
from tkinter import ttk
from thronin.lib.keyboard_mouse import keyboard_mouse as kbm
from thronin.lib.logger import logger
from pynput import keyboard
from thronin.gui.gui_config import LABEL_FONT, COMBOBOX_FONT, ENTRY_FONT


def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent, highlightthickness=0, bd=0)
    scrollbar = ttk.Scrollbar(
        parent, orient="vertical", command=canvas.yview, takefocus=0
    )
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Define the mouse wheel scroll behavior.
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind mouse wheel events only when the cursor is inside the canvas.
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Create a frame within the canvas to hold all the option widgets.
    frame = ttk.Frame(canvas)
    frame_id = canvas.create_window((0, 0), window=frame, anchor="nw")

    # Update the scroll region when the frame changes.
    frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    # Update the frame width when the canvas resizes.
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(frame_id, width=e.width))

    return frame, canvas


def create_combobox(frame, options, widgets, label_text, values, option_key, row):
    label = ttk.Label(frame, text=label_text, font=LABEL_FONT)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
    combobox = ttk.Combobox(frame, values=values, takefocus=0, font=COMBOBOX_FONT)
    combobox.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
    value = options.get(option_key)
    if option_key == "force_routine" and value is None:
        value = "None"
    combobox.set(value)
    widgets[option_key] = combobox
    return row + 1


def create_entry(frame, options, widgets, label_text, option_key, row):
    label = ttk.Label(frame, text=label_text, font=LABEL_FONT)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
    entry = ttk.Entry(frame, takefocus=0, font=ENTRY_FONT)
    entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
    entry.insert(0, str(options.get(option_key)))
    widgets[option_key] = entry
    return row + 1


def create_keybinding_entry(frame, options, widgets, label_text, option_key, row):
    label = ttk.Label(frame, text=label_text, font=LABEL_FONT)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

    # Load the current keybind from options
    initial_value = options.get_keybind(option_key)

    # Display-only entry for showing the pretty name (disabled)
    display_entry = ttk.Entry(frame, justify="center", takefocus=0, font=ENTRY_FONT)
    display_entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
    display_text = initial_value["display"] if initial_value else ""
    display_entry.insert(0, display_text)
    display_entry.config(state="disabled")

    # Create a button instead of an entry field
    keybind_button = ttk.Button(
        frame, text="Click to Set", command=lambda: start_listening()
    )
    keybind_button.grid(row=row, column=2, padx=5, pady=5, sticky="ew")

    # State to manage listening
    listening = {"active": False, "listener": None}

    def on_key_press(key):
        try:
            # Stop listening after capturing one key
            frame.after(0, update_ui, key)
            return False
        except Exception as e:
            logger.error(f"Error in key capture: {e}")

    def update_ui(key):
        listening["active"] = False
        frame.focus_set()

        # Save the keybind using the new set_keybind function
        try:
            options.set_keybind(option_key, key, key.char)
        except AttributeError:
            options.set_keybind(option_key, key, key.name)

        # Update the UI button text and display entry
        keybind_button.config(text="Click to Set")
        new_display = options.get_keybind(option_key)["display"]
        display_entry.config(state="normal")
        display_entry.delete(0, tk.END)
        display_entry.insert(0, new_display)
        display_entry.config(state="disabled")
        kbm.restart_hotkeys()

    def start_listening():
        if not listening["active"]:
            kbm.stop_hotkeys()
            listening["active"] = True
            display_entry.config(state="normal")
            display_entry.delete(0, tk.END)
            display_entry.insert(0, "Press a Key...")
            display_entry.config(state="disabled")
            listener = keyboard.Listener(on_press=on_key_press)
            listening["listener"] = listener
            listener.start()

    widgets[option_key] = display_entry
    return row + 1


def create_radiobutton(frame, options, widgets, label_text, option_key, values, row):
    label = ttk.Label(frame, text=label_text, font=LABEL_FONT)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="nw")

    # Create a StringVar to hold the selected radio button value.
    var = tk.StringVar(value=options.get(option_key))

    # Create a frame for the radio buttons.
    radio_frame = ttk.Frame(frame)
    radio_frame.grid(row=row, column=1, padx=5, pady=5, sticky="w")

    for index, val in enumerate(values):
        rb = ttk.Radiobutton(
            radio_frame, text=val, value=val, variable=var, takefocus=0
        )
        rb.grid(row=0, column=index, padx=(0, 5), pady=5, sticky="w")

    widgets[option_key] = var
    return row + 1


def create_checkbox(frame, options, widgets, label_text, option_key, row):
    label = ttk.Label(frame, text=label_text, font=LABEL_FONT)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

    # Create a BooleanVar for the checkbox.
    var = tk.BooleanVar(value=options.get(option_key, False))
    chk = ttk.Checkbutton(frame, variable=var, takefocus=0)
    chk.grid(row=row, column=1, padx=5, pady=5, sticky="w")

    widgets[option_key] = var
    return row + 1


def create_textbox(
    frame, options, widgets, label_text, option_key, row, height=4, width=67
):
    label = ttk.Label(frame, text=label_text, font=LABEL_FONT)
    label.grid(row=row, column=0, padx=5, pady=5, sticky="nw")

    # Create a sub-frame to hold the textbox.
    text_frame = ttk.Frame(frame)
    text_frame.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

    # Retrieve the default value.
    value = options.get(option_key, "")
    text_var = tk.StringVar(value=value)

    # Create the textbox widget.
    textbox = tk.Text(
        text_frame,
        height=height,
        width=width,
        wrap="word",
        takefocus=0,
        font=ENTRY_FONT,
    )
    textbox.insert("1.0", value)
    textbox.pack(fill="both", expand=True)

    # Bind changes to update the associated StringVar.
    def on_text_change(event):
        new_val = textbox.get("1.0", tk.END).strip()
        text_var.set(new_val)

    textbox.bind("<KeyRelease>", on_text_change)

    # Save both the text widget and the variable.
    widgets[option_key] = {"var": text_var, "widget": textbox}
    return row + 1
