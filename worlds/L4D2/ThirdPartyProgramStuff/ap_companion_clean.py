import asyncio
import websockets
import json
import re
import os
import sys
import traceback
import time
import random
import threading
import winreg
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

DEBUG = False
stop_event = threading.Event()
gui_instance = None

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def find_all_l4d2_paths():
    """Find all L4D2 installation paths"""
    found_paths = []
    
    try:
        # Try Steam registry key
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            l4d2_path = os.path.join(steam_path, "steamapps", "common", "Left 4 Dead 2")
            if os.path.exists(l4d2_path):
                found_paths.append(l4d2_path)
    except:
        pass
    
    # Common installation paths
    common_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2",
        r"C:\Program Files\Steam\steamapps\common\Left 4 Dead 2",
        r"D:\Steam\steamapps\common\Left 4 Dead 2",
        r"E:\Steam\steamapps\common\Left 4 Dead 2",
        r"F:\SteamLibrary\steamapps\common\Left 4 Dead 2",
        r"D:\SteamLibrary\steamapps\common\Left 4 Dead 2",
        r"E:\SteamLibrary\steamapps\common\Left 4 Dead 2",
        r"G:\SteamLibrary\steamapps\common\Left 4 Dead 2",
        r"H:\SteamLibrary\steamapps\common\Left 4 Dead 2"
    ]
    
    for path in common_paths:
        if os.path.exists(path) and path not in found_paths:
            found_paths.append(path)
    
    if not found_paths:
        # Ask user if not found
        print("Could not auto-detect L4D2 installation.")
        while True:
            user_path = input("Please enter your L4D2 installation path (e.g., C:\\Program Files (x86)\\Steam\\steamapps\\common\\Left 4 Dead 2): ")
            if os.path.exists(user_path):
                found_paths.append(user_path)
                break
            print("Path not found. Please try again.")
    
    return found_paths

# Auto-detect all L4D2 paths
L4D2_PATHS = find_all_l4d2_paths()
# print(f"Found L4D2 installations: {L4D2_PATHS}")
L4D2_BASE_PATH = L4D2_PATHS[0]  # Use first one for status file

# ===== GUI CLASS =====
class L4D2CompanionGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.is_dark = False
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.title("L4D2 AP Companion Client")
        self.geometry("800x700")
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Input fields
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(input_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.host_entry = ttk.Entry(input_frame, width=40)
        self.host_entry.grid(row=0, column=1, sticky=tk.EW)
        self.host_entry.insert(0, "archipelago.gg:38281")
        ttk.Label(input_frame, text="Slot Name:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.slot_entry = ttk.Entry(input_frame, width=40)
        self.slot_entry.grid(row=1, column=1, sticky=tk.EW, pady=(5, 0))
        ttk.Label(input_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.password_entry = ttk.Entry(input_frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, sticky=tk.EW, pady=(5, 0))
        input_frame.columnconfigure(1, weight=1)
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        self.connect_button = ttk.Button(button_frame, text="Connect", command=self.connect)
        self.connect_button.pack(side=tk.LEFT, padx=(0, 5))
        self.disconnect_button = ttk.Button(button_frame, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT)
        self.theme_button = ttk.Button(button_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Log tab
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Log")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=70, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("info", foreground="blue")
        
        # Campaigns tab
        campaigns_frame = ttk.Frame(self.notebook)
        self.notebook.add(campaigns_frame, text="Campaigns")
        
        campaigns_inner = ttk.Frame(campaigns_frame, padding="10")
        campaigns_inner.pack(fill=tk.BOTH, expand=True)
        
        self.campaigns_text = tk.Text(campaigns_inner, height=20, width=70, state=tk.DISABLED, wrap=tk.WORD)
        self.campaigns_text.pack(fill=tk.BOTH, expand=True)
        self.campaigns_text.tag_config("unlocked", foreground="green")
        self.campaigns_text.tag_config("locked", foreground="gray")
        
        # Status bar
        self.status_label = tk.Label(main_frame, text="● Disconnected", relief=tk.SUNKEN, anchor=tk.W, bg="white", fg="black", padx=5, pady=5)
        self.status_label.pack(fill=tk.X)
        self._load_theme_preference()
        self._apply_theme()

    def _apply_theme(self):
        if self.is_dark:
            # Dracula-inspired dark theme
            bg_dark = '#282a36'
            fg_light = '#f8f8f2'
            
            self.style.configure('TFrame', background=bg_dark)
            self.style.configure('TLabel', background=bg_dark, foreground=fg_light)
            self.style.configure('TLabelFrame', background=bg_dark, foreground=fg_light)
            self.style.configure('TLabelFrame.Label', background=bg_dark, foreground=fg_light)
            self.style.configure('TButton', background='#44475a', foreground=fg_light)
            self.style.configure('TEntry', fieldbackground='#44475a', foreground=fg_light)
            
            # Find and update the log frame
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.LabelFrame):
                            subchild.config(bg=bg_dark, fg=fg_light)
                            
            self.log_text.config(bg=bg_dark, fg=fg_light)
            self.log_text.tag_config('error', foreground='#ff5555')
            self.log_text.tag_config('success', foreground='#50fa7b')
            self.log_text.tag_config('info', foreground='#8be9fd')
            self.status_label.config(bg=bg_dark, fg=fg_light)
            self.configure(bg=bg_dark)
        else:
            self.style.configure('TFrame', background='white')
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TLabelFrame', background='white', foreground='black')
            self.style.configure('TLabelFrame.Label', background='white', foreground='black')
            self.style.configure('TButton', background='lightgray', foreground='black')
            self.style.configure('TEntry', fieldbackground='white', foreground='black')
            
            # Find and update the log frame
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    for subchild in child.winfo_children():
                        if isinstance(subchild, tk.LabelFrame):
                            subchild.config(bg='white', fg='black')
                            
            self.log_text.config(bg='white', fg='black')
            self.log_text.tag_config('error', foreground='red')
            self.log_text.tag_config('success', foreground='green')
            self.log_text.tag_config('info', foreground='blue')
            self.status_label.config(bg='white', fg='black')
            self.configure(bg='white')

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self._apply_theme()
        self._save_theme_preference()
        self.log_message(f"Theme switched to {'Dark' if self.is_dark else 'Light'} mode", 'info')

    def _save_theme_preference(self):
        theme_config_path = get_resource_path('theme_config.json')
        try:
            with open(theme_config_path, 'w') as f:
                json.dump({'is_dark': self.is_dark}, f)
        except Exception as e:
            self.log_message(f"Failed to save theme preference: {e}", "error")

    def _load_theme_preference(self):
        theme_config_path = get_resource_path('theme_config.json')
        try:
            with open(theme_config_path, 'r') as f:
                config = json.load(f)
                self.is_dark = config.get('is_dark', False)
        except (FileNotFoundError, json.JSONDecodeError):
            self.is_dark = False

    def connect(self):
        host = self.host_entry.get().strip()
        slot = self.slot_entry.get().strip()
        password = self.password_entry.get().strip()
        if not host or not slot:
            messagebox.showerror("Input Error", "Host and Slot Name are required")
            return
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)
        self.status_label.config(text="● Connecting...", fg="#ffb86c")
        self.log_message(f"Connecting to {host} as {slot}...", "info")
        stop_event.clear()
        self.connection_thread = threading.Thread(target=self._run_connection, args=(host, slot, password), daemon=True)
        self.connection_thread.start()

    def _run_connection(self, host, slot, password):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(connect_to_archipelago(host, slot, password))
            self.after(0, self._on_connect_success)
        except Exception as e:
            self.after(0, lambda: self._on_connect_fail(str(e)))
        finally:
            loop.close()

    def disconnect(self):
        stop_event.set()
        self.log_message("Disconnecting...", "info")
        if hasattr(self, 'connection_thread') and self.connection_thread.is_alive():
            self.connection_thread.join(timeout=2.0)
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.status_label.config(text="● Disconnected", fg="red")
        self.log_message("Disconnected", "info")

    def _on_connect_success(self):
        # Guard against callbacks arriving after disconnect initiated
        if stop_event.is_set():
            return
        self.status_label.config(text="● Connected", fg="green")
        self.log_message("Connected to server successfully", "success")
        self.update_campaigns_display()

    def _on_connect_fail(self, error_message):
        # Guard against callbacks arriving after disconnect initiated
        if stop_event.is_set():
            return
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.status_label.config(text="● Disconnected", fg="red")
        self.log_message(f"Connection failed: {error_message}", "error")
        messagebox.showerror("Connection Failed", f"Could not connect to server:\n{error_message}")

    def log_message(self, message, tag=None):
        timestamp = time.strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        self.log_text.config(state=tk.NORMAL)
        if tag:
            self.log_text.insert(tk.END, formatted, tag)
        else:
            self.log_text.insert(tk.END, formatted)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_campaigns_display(self):
        """Update the campaigns tab with unlock status"""
        self.campaigns_text.config(state=tk.NORMAL)
        self.campaigns_text.delete(1.0, tk.END)
        
        campaigns = ["Dead Center", "The Passing", "Dark Carnival", "Swamp Fever", "Hard Rain", 
                    "The Parish", "Cold Stream", "The Sacrifice", "No Mercy", "Crash Course",
                    "Death Toll", "Dead Air", "Blood Harvest", "The Last Stand"]
        
        self.campaigns_text.insert(tk.END, "Campaign Progress\n", "unlocked")
        self.campaigns_text.insert(tk.END, "=" * 30 + "\n\n")
        
        for campaign in campaigns:
            if campaign in unlocked_campaigns:
                self.campaigns_text.insert(tk.END, f"✓ {campaign}\n", "unlocked")
            else:
                self.campaigns_text.insert(tk.END, f"✗ {campaign}\n", "locked")
        
        self.campaigns_text.config(state=tk.DISABLED)

def log(message, tag=None):
    if gui_instance is not None:
        gui_instance.after(0, lambda: gui_instance.log_message(message, tag))
        # Update campaigns display when items are received
        if tag == "success" and "Received:" in message:
            gui_instance.after(0, lambda: gui_instance.update_campaigns_display())
    else:
        print(message)

AP_COMMAND_FILE = get_resource_path("mod_data/ap_commands.txt")
AP_EVENTS_FILE = get_resource_path("mod_data/ap_events.txt")
# Status file will be written to all installations via update_status()

# Item category tracking
ALL_CAMPAIGNS = ["Dead Center", "The Passing", "Dark Carnival", "Swamp Fever", "Hard Rain", "The Parish", 
                "Cold Stream", "No Mercy", "Crash Course", "Death Toll", "Dead Air", "Blood Harvest", 
                "The Sacrifice", "The Last Stand"]

ALL_HEALING = ["First Aid Kit", "Defib", "Pills", "Adrenaline"]

ALL_WEAPON_UPGRADES = ["Laser Sight", "Incendiary", "Explosive Ammo"]

ALL_T1_WEAPONS = ["Pump Shotgun", "Chrome Shotgun", "Submachine Gun", "Silenced Submachine Gun", "MP5"]

ALL_T2_WEAPONS = ["Tactical Shotgun", "Combat Shotgun", "Hunting Rifle", "Sniper Rifle", "M-16", 
                 "Scar-H", "AK-47", "SG 552", "Scout", "AWP"]

ALL_HEAVY_WEAPONS = ["Grenade Launcher", "M60"]

ALL_GRENADES = ["Molotov", "Pipe Bomb", "Bile Bomb"]

ALL_MELEE = ["Fireaxe", "Baseball Bat", "Cricket Bat", "Crowbar", "Frying Pan", "Golf Club", 
            "Guitar", "Katana", "Machete", "Nightstick", "Pitchfork", "Shovel", "Knife", "Chainsaw", "Riot Shield"]

ALL_EXPLOSIVES = ["Gas Can", "Oxygen Tank", "Propane Tank", "Fireworks"]

ALL_MISC = ["P220 Pistol", "Glock", "Magnum", "Gnome Chompski", "Gutted Medkit", "Empty Gas Can", "Expired Pills", "Dud Pipe Bomb", "Bent Laser Sight", "Punctured Oxygen Tank"]

def get_seed_based_starter_items(seed):
    """Get minimal starting items: just pistol"""
    log("Using minimal starting inventory", "info")
    
    # Minimal starting inventory
    starters = {
        "campaigns": [],  # Default starting campaign
        "healing": [],
        "weapon_upgrades": [],
        "t1_weapons": [],
        "t2_weapons": [],
        "heavy_weapons": [],
        "grenades": [],
        "melee": [],
        "explosives": [],
        "misc": []
    }
    
    return starters

# Initialize with placeholder - will be set when connected to server
unlocked_campaigns = []
unlocked_healing = []
unlocked_weapon_upgrades = []
unlocked_t1_weapons = []
unlocked_t2_weapons = []
unlocked_heavy_weapons = []
unlocked_grenades = []
unlocked_melee = []
unlocked_explosives = []
unlocked_misc = []

# Goal tracking
goal_campaigns = 1  # Will be set from slot_data
goal_completed = False
completed_campaigns = set()  # Track unique campaigns with a completed finale

# Goal completion persistence (will be set per seed)
GOAL_COMPLETED_FILE = None

# Item ID to name mapping
ITEM_ID_TO_NAME = {
    # Trap items
    69420065: "Trap: Boomer",
    69420066: "Trap: Hunter",
    69420067: "Trap: Smoker",
    69420068: "Trap: Tank",
    69420069: "Trap: Witch",
    69420070: "Trap: Charger",
    69420071: "Trap: Jockey",
    69420072: "Trap: Spitter",
    # Campaigns
    69420001: "Dead Center",
    69420002: "The Passing", 
    69420003: "Dark Carnival",
    69420004: "Swamp Fever",
    69420005: "Hard Rain",
    69420006: "The Parish",
    69420007: "Cold Stream",
    69420008: "No Mercy",
    69420009: "Crash Course",
    69420010: "Death Toll",
    69420011: "Dead Air",
    69420012: "Blood Harvest",
    69420013: "The Sacrifice",
    69420014: "The Last Stand",
    # Junk items
    69420015: "Glock",
    69420016: "AWP",
    69420017: "Scout",
    # Healing
    69420018: "First Aid Kit",
    69420019: "Defib",
    69420020: "Pills",
    69420021: "Adrenaline",
    # Weapon upgrades
    69420022: "Laser Sight",
    69420023: "Incendiary",
    69420024: "Explosive Ammo",
    # T1 weapons
    69420025: "Pump Shotgun",
    69420026: "Chrome Shotgun",
    69420027: "Submachine Gun",
    69420028: "Silenced Submachine Gun",
    69420029: "MP5",
    # T2 weapons
    69420030: "Tactical Shotgun",
    69420031: "Combat Shotgun",
    69420032: "Hunting Rifle",
    69420033: "Sniper Rifle",
    69420034: "M-16",
    69420035: "Scar-H",
    69420036: "AK-47",
    69420037: "SG 552",
    # Heavy weapons
    69420038: "Grenade Launcher",
    69420039: "M60",
    # Grenades
    69420040: "Molotov",
    69420041: "Pipe Bomb",
    69420042: "Bile Bomb",
    # Melee
    69420043: "Fireaxe",
    69420044: "Baseball Bat",
    69420045: "Cricket Bat",
    69420046: "Crowbar",
    69420047: "Frying Pan",
    69420048: "Golf Club",
    69420049: "Guitar",
    69420050: "Katana",
    69420051: "Machete",
    69420052: "Nightstick",
    69420053: "Pitchfork",
    69420054: "Shovel",
    69420055: "Knife",
    69420056: "Chainsaw",
    69420057: "Riot Shield",
    # Explosives
    69420058: "Gas Can",
    69420059: "Oxygen Tank",
    69420060: "Propane Tank",
    69420061: "Fireworks",
    # Misc
    69420062: "P220 Pistol",
    69420063: "Magnum",
    69420064: "Gnome Chompski",
    # Filler items
    69420658: "Gutted Medkit",
    69420659: "Empty Gas Can",
    69420660: "Expired Pills",
    69420661: "Dud Pipe Bomb",
    69420662: "Bent Laser Sight",
    69420663: "Punctured Oxygen Tank",
}

def update_status(player_name, connected=True):
    """Write current item status to ALL L4D2 SourceMod data folders"""
    status = {
        "connected": connected,
        "player_name": player_name,
        "unlocked_campaigns": unlocked_campaigns,
        "locked_campaigns": [c for c in ALL_CAMPAIGNS if c not in unlocked_campaigns],
        "unlocked_healing": unlocked_healing,
        "locked_healing": [h for h in ALL_HEALING if h not in unlocked_healing],
        "unlocked_weapon_upgrades": unlocked_weapon_upgrades,
        "locked_weapon_upgrades": [w for w in ALL_WEAPON_UPGRADES if w not in unlocked_weapon_upgrades],
        "unlocked_t1_weapons": unlocked_t1_weapons,
        "locked_t1_weapons": [w for w in ALL_T1_WEAPONS if w not in unlocked_t1_weapons],
        "unlocked_t2_weapons": unlocked_t2_weapons,
        "locked_t2_weapons": [w for w in ALL_T2_WEAPONS if w not in unlocked_t2_weapons],
        "unlocked_heavy_weapons": unlocked_heavy_weapons,
        "locked_heavy_weapons": [w for w in ALL_HEAVY_WEAPONS if w not in unlocked_heavy_weapons],
        "unlocked_grenades": unlocked_grenades,
        "locked_grenades": [g for g in ALL_GRENADES if g not in unlocked_grenades],
        "unlocked_melee": unlocked_melee,
        "locked_melee": [m for m in ALL_MELEE if m not in unlocked_melee],
        "unlocked_explosives": unlocked_explosives,
        "locked_explosives": [e for e in ALL_EXPLOSIVES if e not in unlocked_explosives],
        "unlocked_misc": unlocked_misc,
        "locked_misc": [m for m in ALL_MISC if m not in unlocked_misc],
        "last_updated": int(time.time())
    }

    total_unlocked = len(unlocked_campaigns) + len(unlocked_healing) + len(unlocked_weapon_upgrades) + len(unlocked_t1_weapons) + len(unlocked_t2_weapons) + len(unlocked_heavy_weapons) + len(unlocked_grenades) + len(unlocked_melee) + len(unlocked_explosives) + len(unlocked_misc)

    # Write to ALL L4D2 installations
    for l4d2_path in L4D2_PATHS:
        status_file = os.path.join(l4d2_path, "left4dead2", "addons", "sourcemod", "data", "archipelago_status.json")
        try:
            os.makedirs(os.path.dirname(status_file), exist_ok=True)
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            log(f"Failed to write status file: {e}", "error")

async def send_packet(websocket, packet):
    """Send packets (dict or list of dicts)."""
    if isinstance(packet, list):
        await websocket.send(json.dumps(packet))
    elif isinstance(packet, dict) and "cmd" in packet:
        await websocket.send(json.dumps(packet))
    else:
        log(f"Invalid packet: {packet}", "error")
        return

async def send_location_check(websocket, location_id):
    """Send location check to server"""
    packet = [{"cmd": "LocationChecks", "locations": [location_id]}]
    await send_packet(websocket, packet)
    location_name = get_location_name_from_id(location_id)
    if location_name:
        log(f"Checked: {location_name}", "info")
    else:
        log(f"Checked location ID: {location_id}", "info")

def write_item_spawn_command(item_name):
    """Write item spawn command to ALL L4D2 installations"""
    for l4d2_path in L4D2_PATHS:
        mod_data_path = os.path.join(l4d2_path, "left4dead2", "addons", "sourcemod", "data", "archipelago", "mod_data")
        spawn_file = os.path.join(mod_data_path, "item_spawn.txt")
        
        try:
            os.makedirs(mod_data_path, exist_ok=True)
            with open(spawn_file, 'w') as f:
                f.write(item_name)
        except Exception as e:
            log(f"Failed to write item spawn: {e}", "error")

def get_trap_type_from_name(trap_name):
    """Convert trap item name to trap type number"""
    trap_mapping = {
        "Trap: Boomer": 1,
        "Trap: Hunter": 2,
        "Trap: Smoker": 3,
        "Trap: Tank": 4,
        "Trap: Witch": 5,
        "Trap: Charger": 6,
        "Trap: Jockey": 7,
        "Trap: Spitter": 8
    }
    return trap_mapping.get(trap_name, 0)

def write_trap_command(trap_type):
    """Write trap command to file for SourceMod plugin to read"""
    infected_map = {
        1: "boomer",
        2: "hunter",
        3: "smoker",
        4: "tank",
        5: "witch",
        6: "charger",
        7: "jockey",
        8: "spitter"
    }

    if trap_type not in infected_map:
        log(f"Invalid trap type: {trap_type}", "error")
        return

    infected_name = infected_map[trap_type]

    # Write to ALL locations that the SourceMod plugin checks
    for l4d2_path in L4D2_PATHS:
        # Write to all three locations the plugin checks
        possible_paths = [
            os.path.join(l4d2_path, "left4dead2", "addons", "sourcemod", "data", "archipelago", "mod_data"),
            os.path.join(l4d2_path, "left4dead2", "addons", "sourcemod", "data", "archipelago"),
            os.path.join(l4d2_path, "left4dead2")  # For ../../../trap_command.txt relative to scripting
        ]

        for mod_data_path in possible_paths:
            trap_file = os.path.join(mod_data_path, "trap_command.txt")

            try:
                os.makedirs(mod_data_path, exist_ok=True)
                with open(trap_file, 'w') as f:
                    f.write(infected_name + '\n')  # Add newline for better file reading
            except Exception as e:
                log(f"Failed to write trap command: {e}", "error")
                continue

    # Also try writing to the current working directory as a fallback
    try:
        trap_file = "trap_command.txt"
        with open(trap_file, 'w') as f:
            f.write(infected_name + '\n')
    except Exception as e:
        log(f"Failed to write trap file: {e}", "error")

# Hardcoded location table for finale detection (avoids import issues)
location_table = {
    # Dead Center finales
    "Dead Center - Atrium Finale(Ellis)": 69420012,
    "Dead Center - Atrium Finale(Rochelle)": 69420013,
    "Dead Center - Atrium Finale(Coach)": 69420014,
    "Dead Center - Atrium Finale(Nick)": 69420015,
    # The Passing finales
    "The Passing - Port Finale(Ellis)": 69420025,
    "The Passing - Port Finale(Rochelle)": 69420026,
    "The Passing - Port Finale(Coach)": 69420027,
    "The Passing - Port Finale(Nick)": 69420028,
    # Dark Carnival finales
    "Dark Carnival - Concert Finale(Ellis)": 69420045,
    "Dark Carnival - Concert Finale(Coach)": 69420046,
    "Dark Carnival - Concert Finale(Rochelle)": 69420047,
    "Dark Carnival - Concert Finale(Nick)": 69420048,
    # Swamp Fever finales
    "Swamp Fever - Plantation Finale(Ellis)": 69420061,
    "Swamp Fever - Plantation Finale(Coach)": 69420062,
    "Swamp Fever - Plantation Finale(Rochelle)": 69420063,
    "Swamp Fever - Plantation Finale(Nick)": 69420064,
    # Hard Rain finales
    "Hard Rain - Town Escape Finale(Ellis)": 69420081,
    "Hard Rain - Town Escape Finale(Coach)": 69420082,
    "Hard Rain - Town Escape Finale(Rochelle)": 69420083,
    "Hard Rain - Town Escape Finale(Nick)": 69420084,
    # The Parish finales
    "The Parish - Bridge Finale(Ellis)": 69420101,
    "The Parish - Bridge Finale(Coach)": 69420102,
    "The Parish - Bridge Finale(Rochelle)": 69420103,
    "The Parish - Bridge Finale(Nick)": 69420104,
    # The Sacrifice finales
    "The Sacrifice - Port Finale(Francis)": 69420113,
    "The Sacrifice - Port Finale(Bill)": 69420114,
    "The Sacrifice - Port Finale(Zoey)": 69420115,
    "The Sacrifice - Port Finale(Louis)": 69420116,
    # No Mercy finales
    "No Mercy - Rooftop Finale(Francis)": 69420133,
    "No Mercy - Rooftop Finale(Bill)": 69420134,
    "No Mercy - Rooftop Finale(Zoey)": 69420135,
    "No Mercy - Rooftop Finale(Louis)": 69420136,
    # Crash Course finales
    "Crash Course - Truck Depot Finale(Francis)": 69420141,
    "Crash Course - Truck Depot Finale(Bill)": 69420142,
    "Crash Course - Truck Depot Finale(Zoey)": 69420143,
    "Crash Course - Truck Depot Finale(Louis)": 69420144,
    # Death Toll finales
    "Death Toll - Boathouse Finale(Francis)": 69420161,
    "Death Toll - Boathouse Finale(Bill)": 69420162,
    "Death Toll - Boathouse Finale(Zoey)": 69420163,
    "Death Toll - Boathouse Finale(Louis)": 69420164,
    # Dead Air finales
    "Dead Air - Runway Finale(Francis)": 69420181,
    "Dead Air - Runway Finale(Bill)": 69420182,
    "Dead Air - Runway Finale(Zoey)": 69420183,
    "Dead Air - Runway Finale(Louis)": 69420184,
    # Blood Harvest finales
    "Blood Harvest - Farmhouse Finale(Francis)": 69420201,
    "Blood Harvest - Farmhouse Finale(Bill)": 69420202,
    "Blood Harvest - Farmhouse Finale(Zoey)": 69420203,
    "Blood Harvest - Farmhouse Finale(Louis)": 69420204,
    # Cold Stream finales
    "Cold Stream - Cut Throat Creek Finale(Ellis)": 69420217,
    "Cold Stream - Cut Throat Creek Finale(Coach)": 69420218,
    "Cold Stream - Cut Throat Creek Finale(Rochelle)": 69420219,
    "Cold Stream - Cut Throat Creek Finale(Nick)": 69420220,
    # The Last Stand finales
    "The Last Stand - Lighthouse Finale(Francis)": 69420225,
    "The Last Stand - Lighthouse Finale(Bill)": 69420226,
    "The Last Stand - Lighthouse Finale(Zoey)": 69420227,
    "The Last Stand - Lighthouse Finale(Louis)": 69420228,
}

def get_location_name_from_id(location_id):
    """Get location name from location ID"""
    # Reverse lookup from location_table
    for name, loc_id in location_table.items():
        if loc_id == location_id:
            return name
    return None

def parse_printjson_message(msg):
    """Parse a PrintJSON message and return (log_message, tag) or None to suppress."""
    if not isinstance(msg, dict):
        return None
    
    # Handle structured messages with 'type'
    if 'type' in msg:
        msg_type = msg['type']
        if msg_type in ['ItemSend', 'ItemCheat']:
            item_id = msg.get('item')
            if item_id and item_id in ITEM_ID_TO_NAME:
                item_name = ITEM_ID_TO_NAME[item_id]
                receiving = msg.get('receiving')
                found = msg.get('found')
                if receiving and found:
                    return f"{found} sent {item_name} to {receiving}", "info"
                elif receiving:
                    return f"{receiving} received {item_name}", "success"
                else:
                    return f"Received: {item_name}", "success"
            else:
                return f"Unknown item ID: {item_id}", "info"
        # For other types (e.g., Hint), fall back to text processing if present
        if 'text' in msg:
            text = msg['text']
            text = re.sub(r'694200+(\d+)', lambda m: ITEM_ID_TO_NAME.get(int(m.group(0)), m.group(0)), text)
            return f"Info: {text}", "info"
        return f"Info: {msg}", "info"
    
    # Handle text-only messages
    if 'text' in msg:
        text = msg['text']
        
        # Check for trap messages and handle without logging
        if "sending \"Trap:" in text and "to Player1" in text:
            if "Trap: Hunter" in text:
                trap_type = 2
            elif "Trap: Boomer" in text:
                trap_type = 1
            elif "Trap: Smoker" in text:
                trap_type = 3
            elif "Trap: Tank" in text:
                trap_type = 4
            elif "Trap: Witch" in text:
                trap_type = 5
            elif "Trap: Charger" in text:
                trap_type = 6
            elif "Trap: Jockey" in text:
                trap_type = 7
            elif "Trap: Spitter" in text:
                trap_type = 8
            else:
                return None
            write_trap_command(trap_type)
            return None  # Suppress logging
        
        # Suppress pure ID messages
        if re.match(r'^[\(\)\[\]\d\s]+$', text):
            return None
        
        # Replace IDs in text
        text = re.sub(r'694200+(\d+)', lambda m: ITEM_ID_TO_NAME.get(int(m.group(0)), m.group(0)), text)
        return f"Info: {text}", "info"
    
    # Fallback for unknown messages
    return f"Info: {msg}", "info"

def extract_campaign_from_location_name(location_name):
    """Extract campaign name from a location name like 'Dead Center - Atrium Finale(Ellis)'."""
    if not location_name or " - " not in location_name:
        return None
    prefix = location_name.split(" - ", 1)[0]
    # Normalize known inconsistencies
    normalize = {
        "HardRain": "Hard Rain",
        "HardRain - TownEscape Finale": "Hard Rain",
        "Hard Rain - Town Escape Finale": "Hard Rain",
    }
    if prefix in normalize:
        return normalize[prefix]
    if prefix in ALL_CAMPAIGNS:
        return prefix
    # Some entries in Locations.py have slightly different spacing; try fuzzy match by startswith
    for camp in ALL_CAMPAIGNS:
        if prefix.replace(" ", "").lower().startswith(camp.replace(" ", "").lower()[:5]):
            return camp
    return None

async def check_goal_completion(websocket, player_name):
    """Check if goal has been completed and send remaining location checks if so"""
    global goal_completed, completed_campaigns

    if goal_completed:
        return  # Already completed

    if len(completed_campaigns) >= goal_campaigns:
        goal_completed = True
        log(f"GOAL COMPLETED! {len(completed_campaigns)}/{goal_campaigns} campaigns finished!", "success")

        # Save goal completion to file
        if GOAL_COMPLETED_FILE:
            try:
                with open(GOAL_COMPLETED_FILE, 'w') as f:
                    f.write("1")
            except Exception as e:
                log(f"Failed to save goal completion: {e}", "error")

        # Mark client status as GOAL (silent, no new location in console)
        try:
            await send_packet(websocket, [{"cmd": "StatusUpdate", "status": 30}])
            log("Goal status sent to server", "info")
        except Exception as e:
            log(f"Failed to send status update: {e}", "error")

        # Force a sync to ensure the server knows about the goal completion
        try:
            await send_packet(websocket, [{"cmd": "Sync"}])
            log("Syncing goal completion", "info")
        except Exception as e:
            log(f"Failed to send sync: {e}", "error")

        # Send all remaining location checks to complete the game
        log("Sending remaining location checks...", "info")
        # Send a sweep across the full location ID range for this world.
        # The server will ignore invalid IDs; valid ones will mark remaining locations checked.
        min_id = 69420000
        max_id = 69420250  # covers all defined locations in Locations.py
        all_location_ids = list(range(min_id, max_id + 1))

        # Send in batches to avoid overwhelming the server
        batch_size = 50
        for i in range(0, len(all_location_ids), batch_size):
            batch = all_location_ids[i:i + batch_size]
            packet = [{"cmd": "LocationChecks", "locations": batch}]
            await send_packet(websocket, packet)
            await asyncio.sleep(0.1)  # Small delay between batches

        log("All remaining checks sent", "info")

def write_starting_items():
    """Write starting items file to ALL L4D2 installations"""
    all_starting = unlocked_healing + unlocked_weapon_upgrades + unlocked_t1_weapons + unlocked_t2_weapons + unlocked_heavy_weapons + unlocked_grenades + unlocked_melee + unlocked_explosives + unlocked_misc

    for l4d2_path in L4D2_PATHS:
        mod_data_path = os.path.join(l4d2_path, "left4dead2", "addons", "sourcemod", "data", "archipelago", "mod_data")
        starting_file = os.path.join(mod_data_path, "starting_items.txt")

        try:
            os.makedirs(mod_data_path, exist_ok=True)
            with open(starting_file, 'w') as f:
                # Write all starting items, one per line
                for item in all_starting:
                    f.write(item + "\n")
            log("Starting items written", "info")
        except Exception as e:
            log(f"Failed to write starting items: {e}", "error")

async def handle_server_message(message, player_name, websocket):
    """Handle messages from Archipelago server"""
    global unlocked_campaigns, unlocked_healing, unlocked_weapon_upgrades, unlocked_t1_weapons, unlocked_t2_weapons, unlocked_heavy_weapons, unlocked_grenades, unlocked_melee, unlocked_explosives, unlocked_misc
    
    cmd = message.get("cmd")
    
    if cmd == "ReceivedItems":
        items = message.get("items", [])
        
        for item in items:
            # Extract item ID
            item_id = None
            if isinstance(item, dict):
                item_id = item.get("item") or item.get("id")
            elif isinstance(item, int):
                item_id = item
            
            if item_id and item_id in ITEM_ID_TO_NAME:
                item_name = ITEM_ID_TO_NAME[item_id]
                
                # Check if this is a trap item (special handling)
                if item_name.startswith("Trap: "):
                    trap_type = get_trap_type_from_name(item_name)
                    if trap_type > 0:
                        log(f"Trap activated: {item_name.replace('Trap: ', '')}", "error")
                        write_trap_command(trap_type)
                        continue

                # Check item category and add to appropriate list
                if item_name in ALL_CAMPAIGNS and item_name not in unlocked_campaigns:
                    unlocked_campaigns.append(item_name)
                    log(f"Received: {item_name}", "success")
                    # Campaigns are unlocked, but goal is based on finale completions
                elif item_name in ALL_HEALING:
                    if item_name not in unlocked_healing:
                        unlocked_healing.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_WEAPON_UPGRADES:
                    if item_name not in unlocked_weapon_upgrades:
                        unlocked_weapon_upgrades.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_T1_WEAPONS:
                    if item_name not in unlocked_t1_weapons:
                        unlocked_t1_weapons.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_T2_WEAPONS:
                    if item_name not in unlocked_t2_weapons:
                        unlocked_t2_weapons.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_HEAVY_WEAPONS:
                    if item_name not in unlocked_heavy_weapons:
                        unlocked_heavy_weapons.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_GRENADES:
                    if item_name not in unlocked_grenades:
                        unlocked_grenades.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_MELEE:
                    if item_name not in unlocked_melee:
                        unlocked_melee.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_EXPLOSIVES:
                    if item_name not in unlocked_explosives:
                        unlocked_explosives.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
                elif item_name in ALL_MISC:
                    if item_name not in unlocked_misc:
                        unlocked_misc.append(item_name)
                    log(f"Received: {item_name}", "success")
                    write_item_spawn_command(item_name)
        
        update_status(player_name, True)
    
    elif cmd == "Connected":
        # Only process Connected if we're not in the process of disconnecting
        if stop_event.is_set():
            # Ignore buffered Connected messages after disconnect initiated
            return None
        
        log("Successfully connected!", "success")
        # Update GUI status to connected
        if gui_instance is not None:
            gui_instance.after(0, gui_instance._on_connect_success)

        # Get the actual multiworld seed from slot_data
        slot_data = message.get("slot_data", {})
        seed = slot_data.get("Seed")

        if seed:
            log(f"Connected to seed: {seed}", "info")
            global GOAL_COMPLETED_FILE
            GOAL_COMPLETED_FILE = get_resource_path(f"goal_completed_{seed}.txt")
        else:
            log("Warning: No seed found in slot_data", "error")
            # No persistence without seed
            GOAL_COMPLETED_FILE = None

        # Get starting campaign from slot_data options
        options = slot_data.get("options", {})
        # Support both internal snake_case keys and class-name-style keys for resilience
        start_campaign_option = options.get("starting_campaign")
        if start_campaign_option is None:
            start_campaign_option = options.get("StartWithCampaign", 1)  # Default to Dead Center

        # Get goal from slot_data options
        global goal_campaigns, goal_completed, completed_campaigns
        raw_goal = options.get("goal")
        if raw_goal is None:
            raw_goal = options.get("L4D2Goal", 1)  # Default to 1 campaign
        try:
            goal_campaigns = int(raw_goal)
        except (TypeError, ValueError):
            goal_campaigns = 1
        goal_completed = False
        completed_campaigns.clear()

        # Restore goal completion from persistence file if it exists
        if GOAL_COMPLETED_FILE and os.path.exists(GOAL_COMPLETED_FILE):
            try:
                with open(GOAL_COMPLETED_FILE, 'r') as f:
                    content = f.read().strip()
                    if content == "1":
                        goal_completed = True
                        print("Goal completion restored from persistence file.")
                        try:
                            await send_packet(websocket, [{"cmd": "StatusUpdate", "status": 30}])
                        except Exception as e:
                            print(f"Failed to send StatusUpdate on restore: {e}")
            except Exception as e:
                print(f"Failed to read goal completion file: {e}")

        log(f"Goal: Complete {goal_campaigns} campaign(s)", "info")

        # Map option numbers to campaign names
        campaign_map = {
            1: "Dead Center",
            2: "The Passing",
            3: "Dark Carnival",
            4: "Swamp Fever",
            5: "Hard Rain",
            6: "The Parish",
            7: "The Sacrifice",
            8: "No Mercy",
            9: "Crash Course",
            10: "Death Toll",
            11: "Dead Air",
            12: "Blood Harvest",
            13: "The Last Stand",
            14: "Cold Stream"
        }

        starting_campaign = campaign_map.get(start_campaign_option, "Dead Center")

        # Check if all campaigns should start unlocked
        all_campaigns_unlocked = options.get("all_campaigns_start")
        if all_campaigns_unlocked is None:
            all_campaigns_unlocked = options.get("AllCampaignsStart", False)

        if all_campaigns_unlocked:
            unlocked_campaigns = ALL_CAMPAIGNS.copy()
            log("All campaigns unlocked at start", "info")
        else:
            unlocked_campaigns = [starting_campaign]
            log(f"Starting campaign: {starting_campaign}", "info")

        starter_items = get_seed_based_starter_items(seed)
        unlocked_healing = starter_items["healing"]
        unlocked_weapon_upgrades = starter_items["weapon_upgrades"]
        unlocked_t1_weapons = starter_items["t1_weapons"]
        unlocked_t2_weapons = starter_items["t2_weapons"]
        unlocked_heavy_weapons = starter_items["heavy_weapons"]
        unlocked_grenades = starter_items["grenades"]
        unlocked_melee = starter_items["melee"]
        unlocked_explosives = starter_items["explosives"]
        unlocked_misc = starter_items["misc"]

        all_starting = unlocked_healing + unlocked_weapon_upgrades + unlocked_t1_weapons + unlocked_t2_weapons + unlocked_heavy_weapons + unlocked_grenades + unlocked_melee + unlocked_explosives + unlocked_misc
        log(f"Starting items loaded", "info")

        # Write starting items file for the item remover plugin immediately
        write_starting_items()

        update_status(player_name, True)
        # Seed completed campaigns from already-checked locations (handles checks sent outside the companion)
        try:
            checked_locations = message.get("checked_locations", []) or message.get("checked", [])
            seeded = 0
            for loc_id in checked_locations:
                name = get_location_name_from_id(loc_id)
                if name and "Finale" in name:
                    camp = extract_campaign_from_location_name(name)
                    if camp and camp not in completed_campaigns:
                        completed_campaigns.add(camp)
                        seeded += 1
            if seeded:
                log(f"Restored {seeded} completed campaign(s)", "info")
                # Check goal completion only if not already completed
                if not goal_completed:
                    await check_goal_completion(websocket, player_name)
        except Exception as e:
            print(f"Failed to seed completed campaigns from checked_locations: {e}")

        # Request sync of existing items - use array format
        return [{"cmd": "Sync"}]
        
    elif cmd == "RoomInfo":
        log("Received room info", "info")
    
    elif cmd == "RoomUpdate":
        try:
            checked_locations = message.get("checked_locations", [])
            new_campaigns = 0
            for loc_id in checked_locations:
                location_name = get_location_name_from_id(loc_id)
                if location_name and "Finale" in location_name:
                    campaign = extract_campaign_from_location_name(location_name)
                    if campaign and campaign not in completed_campaigns:
                        completed_campaigns.add(campaign)
                        new_campaigns += 1
            if new_campaigns:
                log(f"Synced {new_campaigns} campaign(s)", "info")
                if not goal_completed:
                    await check_goal_completion(websocket, player_name)
        except Exception as e:
            print(f"Error processing RoomUpdate: {e}")

    elif cmd == "LocationInfo":
        checked = message.get("checked", [])
        seeded = 0
        for loc_id in checked:
            location_name = get_location_name_from_id(loc_id)
            if location_name and "Finale" in location_name:
                campaign = extract_campaign_from_location_name(location_name)
                if campaign and campaign not in completed_campaigns:
                    completed_campaigns.add(campaign)
                    seeded += 1
        if seeded:
            log(f"Synced {seeded} campaign(s)", "info")
            # Check goal completion only if not already completed
            if not goal_completed:
                await check_goal_completion(websocket, player_name)

    elif cmd == "ConnectionRefused":
        log(f"Connection refused: {message.get('text', 'Unknown reason')}", "error")
    
    elif cmd == "PrintJSON":
        # Suppress PrintJSON messages - actual item receives are logged via ReceivedItems
        pass
    elif cmd == "InvalidPacket":
        log(f"Server rejected packet: {message.get('text', 'Unknown error')}", "error")
    else:
        log(f"Unknown command: {cmd}", "error")

async def main_loop(websocket, player_name):
    iteration = 0
    while True:
        if stop_event.is_set():
            log("Disconnecting...", "info")
            await websocket.close()
            break
        try:
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=0.1)
            except asyncio.TimeoutError:
                msg = None
            except websockets.exceptions.ConnectionClosed:
                log("Connection closed", "error")
                break

            if msg:
                try:
                    message = json.loads(msg)
                    
                    if isinstance(message, list):
                        for m in message:
                            response = await handle_server_message(m, player_name, websocket)
                            if response:
                                await send_packet(websocket, response)
                    else:
                        response = await handle_server_message(message, player_name, websocket)
                        if response:
                            await send_packet(websocket, response)
                            
                except Exception as e:
                    log(f"Error: {e}", "error")

            iteration += 1
            if iteration % 1000 == 1:
                if DEBUG:
                    print(f"Polling for location_check.txt in {len(L4D2_PATHS)} paths: {L4D2_PATHS}")
            if iteration % 100 == 0:
                if DEBUG:
                    print(f"Heartbeat: Connected=True, Completed Campaigns={len(completed_campaigns)}, Goal Progress={len(completed_campaigns)}/{goal_campaigns}, Goal Completed={goal_completed}")

            # Check for location triggers from mod
            for l4d2_path in L4D2_PATHS:
                location_file = os.path.join(l4d2_path, "left4dead2", "addons", "sourcemod", "data", "archipelago", "mod_data", "location_check.txt")
                if os.path.exists(location_file):
                    try:
                        with open(location_file, 'r') as f:
                            location_id = int(f.read().strip())
                        os.remove(location_file)
                        await send_location_check(websocket, location_id)

                        # Check if this is a finale location (contains "Finale" in name)
                        # If so, mark the campaign completed (once) and check goal
                        location_name = get_location_name_from_id(location_id)
                        if location_name and "Finale" in location_name:
                            campaign = extract_campaign_from_location_name(location_name)
                            if campaign and campaign not in completed_campaigns:
                                completed_campaigns.add(campaign)
                                log(f"Finale completed: {campaign} ({len(completed_campaigns)}/{goal_campaigns})", "success")
                            await check_goal_completion(websocket, player_name)

                    except Exception as e:
                        log(f"Location check error: {e}", "error")

            # Also check for manual location checks from debug script
            debug_location_file = "location_check.txt"
            if os.path.exists(debug_location_file):
                try:
                    with open(debug_location_file, 'r') as f:
                        location_id = int(f.read().strip())
                    os.remove(debug_location_file)
                    await send_location_check(websocket, location_id)

                    # Check if this is a finale location (contains "Finale" in name)
                    # If so, mark the campaign completed (once) and check goal
                    location_name = get_location_name_from_id(location_id)
                    if location_name and "Finale" in location_name:
                        campaign = extract_campaign_from_location_name(location_name)
                        if campaign and campaign not in completed_campaigns:
                            completed_campaigns.add(campaign)
                            log(f"Finale completed: {campaign} ({len(completed_campaigns)}/{goal_campaigns})", "success")
                        await check_goal_completion(websocket, player_name)

                except Exception as e:
                    log(f"Debug location check error: {e}", "error")

            await asyncio.sleep(0.1)

        except Exception as e:
            print(f"Loop error: {e}")
            break

async def connect_to_archipelago(server, slot_name, password=None):
    # Try different URI formats for website compatibility
    if "archipelago.gg" in server:
        uri = f"wss://{server}"
    else:
        uri = f"ws://{server}"
    
    print(f"Trying to connect to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {server}")
            
            # Try exact official client format
            connect_packet = [
                {
                    "cmd": "Connect",
                    "password": password,
                    "game": "Left 4 Dead 2",
                    "name": slot_name,
                    "uuid": "",
                    "version": {"major": 0, "minor": 6, "build": 3, "class": "Version"},
                    "items_handling": 0b111,
                    "tags": ["AP"]
                }
            ]
            
            await send_packet(websocket, connect_packet)
            print("Waiting for authentication...")
            await main_loop(websocket, slot_name)

    except Exception as e:
        print(f"Connection failed: {e}")

# ===== ENTRY POINT =====
if __name__ == "__main__":
    use_gui = "--no-gui" not in sys.argv
    if use_gui:
        mod_data_path = get_resource_path("mod_data")
        if not os.path.exists(mod_data_path):
            os.makedirs(mod_data_path)
        gui = L4D2CompanionGUI()
        if len(sys.argv) > 1:
            gui.slot_entry.insert(0, sys.argv[1])
        if len(sys.argv) > 2:
            gui.host_entry.delete(0, tk.END)
            gui.host_entry.insert(0, sys.argv[2])
        if len(sys.argv) > 3:
            gui.password_entry.insert(0, sys.argv[3])
        gui_instance = gui
        gui.log_message(f"Found L4D2 installations: {L4D2_PATHS}", "info")
        gui.mainloop()
    else:
        mod_data_path = get_resource_path("mod_data")
        if not os.path.exists(mod_data_path):
            os.makedirs(mod_data_path)

        # Get slot name
        if len(sys.argv) > 1:
            player_name = sys.argv[1]
        else:
            player_name = input("Enter your slot name: ")
        
        # Starting items will be initialized when connected to server
        
        # Get server address from user
        if len(sys.argv) > 2:
            server_address = sys.argv[2]
        else:
            server_address = input("Enter server address (e.g. archipelago.gg:38281): ")
        print(f"Connecting as: {player_name} to {server_address}")

        update_status(player_name, False)

        try:
            asyncio.run(connect_to_archipelago(server_address, player_name))
        except Exception as e:
            print(f"Script crashed: {e}")
            traceback.print_exc()
        finally:
            input("Press Enter to exit...")
