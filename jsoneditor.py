import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class JSONEditorApp:
    def __init__(self, root):
        self.colors = {
            "background": "#2b2b2b",
            "foreground": "#ffffff",
            "highlight": "#3b3b3b",
            "disabled": "#4b4b4b",
        }
        self.root = root
        self.root.resizable(False, False)
        self.root.tk_setPalette(background=self.colors["background"], foreground=self.colors["foreground"])
        try:
            self.root.iconbitmap("assets/editor.ico")
        except tk.TclError:
            print("Icon not found, using default icon")
        self.root.title("WoTB RPC JSON Configurator")

        self.create_widgets()

        self.json_data = None

    def create_widgets(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('default')
        self.style.configure("Treeview",
                             background=self.colors["background"],
                             foreground=self.colors["foreground"],
                             fieldbackground="#3C3C3C",
                             font=("TkDefaultFont", 10),
                             rowheight=25)
        self.style.configure("Treeview.Heading",
                             background=self.colors["background"],
                             foreground=self.colors["foreground"],
                             font=("TkDefaultFont", 10))
        # Configuration frame
        self.config_frame = tk.LabelFrame(self.root, text="Configuration", background=self.colors["background"], foreground=self.colors["foreground"])
        self.config_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Configuration entries
        self.config_entries = {}
        config_keys = ["client_id", "icon", "hero", "large_image", "small_image"]
        for idx, key in enumerate(config_keys):
            tk.Label(self.config_frame, text=key, background=self.colors["background"], foreground=self.colors["foreground"]).grid(row=idx, column=0, sticky='e')
            entry = tk.Entry(self.config_frame, width=50, background=self.colors["background"], foreground=self.colors["foreground"])
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.config_entries[key] = entry

        # Player frame
        self.player_frame = tk.LabelFrame(self.root, text="Variables - Player", background=self.colors["background"], foreground=self.colors["foreground"])
        self.player_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

        # Player entries
        self.player_entries = {}
        player_keys = ["username", "avatar_url", "clan_tag", "clan_name", "favorite_tank"]
        for idx, key in enumerate(player_keys):
            tk.Label(self.player_frame, text=key, background=self.colors["background"], foreground=self.colors["foreground"]).grid(row=idx, column=0, sticky='e')
            entry = tk.Entry(self.player_frame, width=50, background=self.colors["background"], foreground=self.colors["foreground"])
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.player_entries[key] = entry

        # Tanks frame
        self.tanks_frame = tk.LabelFrame(self.root, text="Variables - Tanks", background=self.colors["background"], foreground=self.colors["foreground"])
        self.tanks_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nw')

        # Tanks table
        self.tanks_table = ttk.Treeview(self.tanks_frame, columns=("name", "tier", "type"), show='headings')
        self.tanks_table.heading("name", text="Tank name")
        self.tanks_table.heading("tier", text="Tier")
        self.tanks_table.heading("type", text="Type")
        self.tanks_table.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        # Add a scroll bar
        self.scrollbar = ttk.Scrollbar(self.tanks_frame, orient="vertical", command=self.tanks_table.yview)
        self.scrollbar.grid(row=0, column=3, sticky='ns')
        self.tanks_table.configure(yscroll=self.scrollbar.set)

        # Table control buttons
        self.add_button = tk.Button(
            self.tanks_frame, 
            text="Add", 
            command=self.add_tank,
            borderwidth=0, 
            highlightthickness=0, 
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.add_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.edit_button = tk.Button(
            self.tanks_frame, 
            text="Edit", 
            command=self.edit_tank,
            borderwidth=0, 
            highlightthickness=0, 
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.edit_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self.delete_button = tk.Button(
            self.tanks_frame, 
            text="Delete", 
            command=self.delete_tank,
            borderwidth=0, 
            highlightthickness=0, 
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.delete_button.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

        # File open/save buttons
        self.button_frame = tk.Frame(self.root, background=self.colors["background"])
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.open_button = tk.Button(
            self.button_frame, 
            text="Open JSON", 
            command=self.open_json,
            borderwidth=0, 
            highlightthickness=0, 
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.open_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(
            self.button_frame, 
            text="Save JSON", 
            command=self.save_to_default_location,
            borderwidth=0, 
            highlightthickness=0, 
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.save_button.grid(row=0, column=1, padx=10)
        
        self.default_button = tk.Button(
            self.button_frame, 
            text="Load default", 
            command=self.load_default_json,
            borderwidth=0, 
            highlightthickness=0,  
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.default_button.grid(row=0, column=2, padx=10)
        
        self.save_as_button = tk.Button(
            self.button_frame, 
            text="Save as JSON", 
            command=self.save_as_json,
            borderwidth=0, 
            highlightthickness=0, 
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            cursor="hand2")
        self.save_as_button.grid(row=0, column=3, padx=10)
    
    def load_default_json(self):
        with open("./main.json", 'r', encoding='utf-8') as file:    
            self.json_data = json.load(file)
            self.populate_fields()

    def open_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.json_data = json.load(file)
                self.populate_fields()
    

    def populate_fields(self):
        if self.json_data:
            config = self.json_data.get("config", {})
            for key, entry in self.config_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, config.get(key, ""))

            player = self.json_data.get("variables", {}).get("player", {})
            for key, entry in self.player_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, player.get(key, ""))

            self.tanks_table.delete(*self.tanks_table.get_children())
            tanks = self.json_data.get("variables", {}).get("tanks", [])
            for tank in tanks:
                self.tanks_table.insert("", "end", values=(tank["name"], tank["tier"], tank["type"]))

    def save_to_default_location(self):
        self.save_json("./main.json")

    def save_as_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.save_json(file_path)

    def save_json(self, file_path):
        try:
            self.update_json_data()
            if file_path.endswith(".json"):
                with open(file_path, 'r', encoding='utf-8') as file:
                    existing_data = file.read()
                if existing_data:
                    overwrite = messagebox.askyesno("Overwrite file", "This file already exists. Do you want to overwrite it?")
                    if not overwrite:
                        return
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.json_data, file, indent=4)
            messagebox.showinfo("Success", "File saved successfully")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format")

    def update_json_data(self):
        config = {key: entry.get() for key, entry in self.config_entries.items()}
        player = {key: entry.get() for key, entry in self.player_entries.items()}
        tanks = [self.tanks_table.item(item)["values"] for item in self.tanks_table.get_children()]

        self.json_data["config"] = config
        self.json_data["variables"]["player"] = player
        self.json_data["variables"]["tanks"] = [{"name": t[0], "tier": t[1], "type": t[2]} for t in tanks]

    def add_tank(self):
        self.open_tank_editor()

    def edit_tank(self):
        selected_item = self.tanks_table.selection()
        if selected_item:
            values = self.tanks_table.item(selected_item)["values"]
            self.open_tank_editor(values, selected_item)

    def delete_tank(self):
        selected_item = self.tanks_table.selection()
        if selected_item:
            self.tanks_table.delete(selected_item)

    def open_tank_editor(self, values=None, item_id=None):
        editor = tk.Toplevel(self.root)
        editor.title("Tank Editor")
        try:
            editor.iconbitmap("assets/editor.ico")
        except tk.TclError:
            print("Icon not found, using default icon")
        editor.resizable(False, False)
        editor.configure(background=self.colors["background"])

        tk.Label(editor, text="Tank name", background=self.colors["background"], foreground=self.colors["foreground"]).grid(row=0, column=0, padx=5, pady=5)
        tank_name_entry = tk.Entry(editor, width=50, background=self.colors["background"], foreground=self.colors["foreground"])
        tank_name_entry.grid(row=0, column=1, padx=5, pady=5)
        if values:
            tank_name_entry.insert(0, values[0])

        tk.Label(editor, text="Tier", background=self.colors["background"], foreground=self.colors["foreground"]).grid(row=1, column=0, padx=5, pady=5)
        tank_tier_entry = ttk.Combobox(editor, values=["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"], state="readonly")
        tank_tier_entry.grid(row=1, column=1, padx=5, pady=5)
        if values:
            tank_tier_entry.set(values[1])

        tk.Label(editor, text="Type", background=self.colors["background"], foreground=self.colors["foreground"]).grid(row=2, column=0, padx=5, pady=5)
        tank_type_entry = ttk.Combobox(editor, values=["Tech Tree", "Premium", "Collector"], state="readonly")
        tank_type_entry.grid(row=2, column=1, padx=5, pady=5)
        if values:
            tank_type_entry.set(values[2])

        def save_tank():
            tank_name = tank_name_entry.get()
            tank_tier = tank_tier_entry.get()
            tank_type = tank_type_entry.get()
            if item_id:
                self.tanks_table.item(item_id, values=(tank_name, tank_tier, tank_type))
            else:
                self.tanks_table.insert("", "end", values=(tank_name, tank_tier, tank_type))
            editor.destroy()

        save_button = tk.Button(
            editor, 
            text="Save", 
            borderwidth=0, 
            highlightthickness=0,
            background=self.colors["highlight"], 
            foreground=self.colors["foreground"],
            command=save_tank,
            cursor="hand2")
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditorApp(root)
    root.mainloop()
