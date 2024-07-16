import tkinter as tk, time, psutil, json, threading
from tkinter import messagebox
from tkinter import ttk
from pypresence import Presence

class WoTB_RPC(tk.Tk):
    def __init__(self):
        super().__init__()
        print("Starting WoTB RPC")
        print("Loading json data...")
        with open('main.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        print("Data loaded successfully!")
        self.large_image = self.data['config']['large_image']
        self.large_text = self.data['author']
        self.text = "{tank_name} - Tier {tier} {type_}"
        self.small_image = self.data['config']['small_image']
        self.small_text = self.data['variables']['player']['username']
        self.client_id = self.data['config']['client_id']
        self.icon_path = self.data['config']['icon']
        self.hero_path = self.data['config']['hero']
        self.tanks = ["None"]
        self.title_var = f"{self.data['name']} : {self.data['variables']['player']['username']}"
        self.replacements = self.data['variables']['replacements']
        self.protocol("WM_DELETE_WINDOW", self.fully_close_app)
        print("Connecting to discord...")
        self.RPC = Presence(self.client_id)
        self.RPC.connect()
        self.start_time = time.time()
        print("Connected to discord!")
        
        print("Initializing UI...")
        self.initialize_ui()
        print("UI initialized!")
        self.check_process()
        self.refresh_tank_list()
        
    def initialize_ui(self):
        self.title(self.title_var)
        self.minsize(400, 400)
        self.resizable(False, False)
        self.tk_setPalette(background='#2b2b2b', foreground='white')
        try: 
            self.iconbitmap(self.icon_path)
        except tk.TclError:
            print("Icon not found, using default icon")
            
        # Create frames
        hero_frame = tk.Frame(self)
        hero_frame.pack(pady=10, anchor="w", padx=10)
        process_status_frame = tk.Frame(self)
        process_status_frame.pack(anchor="w", padx=10)
        mode_status_frame= tk.Frame(self)
        mode_status_frame.pack(pady=10, anchor="w", padx=10)
        tank_frame = tk.Frame(self)
        tank_frame.pack(anchor="w", padx=10)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10, anchor="w", padx=10)
        
        self.logo = tk.PhotoImage(file=self.hero_path)
        tk.Label(hero_frame, image=self.logo).pack(side=tk.LEFT, padx=6)
        
        self.process_status_label = tk.Label(process_status_frame, text='World of Tanks Blitz is not running')
        self.process_status_label.pack(side=tk.LEFT, padx=6)
        self.mode_status_label = tk.Label(mode_status_frame, text='Status: Disabled')
        self.mode_status_label.pack(side=tk.LEFT, padx=6)

        tank_label = tk.Label(tank_frame, text='Select the tank (Refresh the list when it says "None"):')
        tank_label.pack(anchor="w", padx=6)

        self.tank_var = tk.StringVar()
        self.tank_var.set(self.tanks[0])
        tank_options = self.tanks
        self.tank_menu = ttk.Combobox(tank_frame, textvariable=self.tank_var, values=tank_options, state='readonly')
        self.tank_menu.pack(anchor="w", padx=10)

        # Update buttons
        self.ingarage_button = tk.Button(
            button_frame, 
            text='In Garage', 
            command=self.in_garage, 
            borderwidth=0, 
            highlightthickness=0, 
            background="#3C3C3C", 
            cursor="hand2")
        self.ingarage_button.pack(side=tk.LEFT, padx=10)
        
        self.inbattle_button = tk.Button(
            button_frame, 
            text='In Battle', 
            command=self.in_battle, 
            borderwidth=0, 
            highlightthickness=0, 
            background="#3C3C3C", 
            cursor="hand2")
        self.inbattle_button.pack(side=tk.LEFT, padx=10) 
        
        self.refresh_tank_list_button = tk.Button(
            button_frame, 
            text='Refresh Tank List', 
            command=self.refresh_tank_list, 
            borderwidth=0, 
            highlightthickness=0, 
            background="#3C3C3C", 
            cursor="hand2")
        self.refresh_tank_list_button.pack(side=tk.LEFT, padx=10) 
        
        self.generic_button = tk.Button(
            button_frame, 
            text='Generic', 
            command=self.generic_status, 
            borderwidth=0, 
            highlightthickness=0, 
            background="#3C3C3C", 
            cursor="hand2")
        self.generic_button.pack(side=tk.LEFT, padx=10)
        self.clearrpc_button = tk.Button(
            button_frame, 
            text='Clear RPC', 
            command=self.clear_rpc, 
            borderwidth=0, 
            highlightthickness=0, 
            background="#3C3C3C", 
            cursor="hand2")
        self.clearrpc_button.pack(side=tk.LEFT, padx=10)
    def replace_multiple(self, text, replacements):
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def refresh_tank_list(self):
        with open('main.json', 'r', encoding='utf-8') as f:
            tanks_data = json.load(f)

        self.tanks = [tank['name'] for tank in tanks_data['variables']['tanks']]
        self.tank_options_list = [self.replace_multiple(tank, self.replacements) for tank in self.tanks]
        self.tank_options_list.sort()
        self.tank_menu.config(values=self.tank_options_list)
        self.tank_var.set(self.tank_options_list[0])
        #print(f"Tank list refreshed:\n {self.tank_options_list}")
        
    def check_process(self):
        def _check():
            if any(proc.name() == 'wotblitz.exe' for proc in psutil.process_iter()):
                self.process_status_label.config(text='World of Tanks Blitz is running')
                self.ingarage_button.config(state='normal', cursor="hand2")
                self.inbattle_button.config(state='normal', cursor="hand2")
            else:
                self.process_status_label.config(text='World of Tanks Blitz is not running')
                self.mode_status_label.config(text='Status: Disabled')
                self.ingarage_button.config(state='disabled', cursor="arrow")
                self.inbattle_button.config(state='disabled', cursor="arrow")
                self.RPC.clear()

            self.after(1000, self.check_process)

        thread = threading.Thread(target=_check)
        thread.start()
        
    def send_notification(self, title, message):
            try: 
                self.tk.call('tk', 'bell') 
            except tk.TclError:
                self.bell() 
            self.title(title)
            self.after(500, lambda: self.title(self.title_var))
            self.deiconify()
            self.lift()
            self.update()
            self.bell()
    
    def in_garage(self):
        tank_name = self.tank_var.get()

        with open('main.json', 'r', encoding='utf-8') as f:
            tanks_data = json.load(f)

        tanks = tanks_data['variables']['tanks']
        tank_info = next((tank for tank in tanks if tank['name'] == tank_name), None)
        
        if tank_info:
            tier = tank_info['tier']
            type_ = tank_info['type']
            
            self.RPC.update(
                large_image=self.large_image,
                large_text=self.text.format(tank_name=tank_name, tier=tier, type_=type_),
                small_image=self.small_image,
                small_text=self.small_text,
                state='In Garage',
                details=f'Selected {tank_name}',
                start=self.start_time
            )
            self.mode_status_label.config(text='Status: In Garage')
            self.send_notification('Updated', 'Discord Rich Presence updated successfully!')
        else:
            self.mode_status_label.config(text='Status: Tank not found; In Garage')
            self.send_notification('Error', 'Selected tank not found in the JSON data.')
        
    def in_battle(self):
        tank_name = self.tank_var.get()

        with open('main.json', 'r', encoding='utf-8') as f:
            tanks_data = json.load(f)

        tanks = tanks_data['variables']['tanks']
        tank_info = next((tank for tank in tanks if tank['name'] == tank_name), None)
        
        if tank_info:
            tier = tank_info['tier']
            type_ = tank_info['type']
            
            self.RPC.update(
                large_image=self.large_image,
                large_text=self.text.format(tank_name=tank_name, tier=tier, type_=type_),
                small_image=self.small_image,
                small_text=self.small_text,
                state=f'In Battle',
                details=f'{tank_name} deployed',
                start=self.start_time
            )
            self.mode_status_label.config(text='Status: In Battle')
            self.send_notification('Updated', 'Discord Rich Presence updated successfully!')
        else:
            self.mode_status_label.config(text='Status: Tank not found; In Battle')
            self.send_notification('Error', 'Selected tank not found in the JSON data.')
            
    def generic_status(self):
        self.RPC.update(
            large_image=self.large_image,
            large_text=self.large_text,
            small_image=self.small_image,
            small_text=self.small_text,
            state=f"Favorite tank: {self.data['variables']['player']['favorite_tank']}",
            details=f"Clan: {self.data['variables']['player']['clan_tag']} {self.data['variables']['player']['clan_name']}",
            start=self.start_time
        )
        self.mode_status_label.config(text='Status: Generic')
        
    def clear_rpc(self):
        self.RPC.clear()
        
    def fully_close_app(self):
        self.RPC.clear()
        self.RPC.close()
        self.destroy()
        
if __name__ == "__main__":
    app = WoTB_RPC()
    app.mainloop()