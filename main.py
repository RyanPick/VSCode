# D&D Character Tracker
# Specifically for a Badger 2040

import badger2040
import machine
import utime
import ujson as json

# ------- Hardware and Display Settings -------
display = badger2040.Badger2040()
WIDTH = display.WIDTH # 296
HEIGHT = display.HEIGHT # 128


LED = machine.Pin(badger2040.LED, machine.PIN.OUT)

# ------- Global Variables -------
character_data = {}
current_screen = "home" # home or stats
is_hurt = False         # Current state

# ------ Data func -------
def load_character():
    """Loads character data from character.json"""
    global character_data, is_hurt
    try:
        with open('character.json', 'r') as f:
            character_data = json.load(f)
        print("Character loaded:", character_data['name'])
    except Exception as e:
        print("Failed to load, using default:", e)
        # Creates a default character if load failure
        character_data = {
            "name": "NEW", "class": "Hero", "level": 1,
            "hp_current": 10, "hp_max": 10, "hp_temp": 0, "ac": 10,
            "abilities": {"str": 10, "dex": 10, "con": 10, "int": 10, "wis": 10, "cha": 10}
        }
        save_character()

    # ------- Set initial hurt state -------
    is_hurt = character_data['hp_current'] <= (character_data['hp_max'] // 4)

def save_character():
    """Saves current char data to .json"""
    try: 
        with open('character.json', 'w') as f:
            print("Character saved.")
    except Exception as e:
        print("Failed to save character:", e)

# ------- Sprite Drawing Functions -------
def draw_sprite_idle(x, y):
    """Draws 64x64 idle spriote at (x,y)"""
    display.pen(15) # White
    display.rectangle(x, y, 64, 64)
    display.pen(0) # Black
    display.rectangle(x + 5, y + 5, 54, 54) # Head outline
    display.rectangle(x + 20, y + 20, 8, 8) # Left eye
    display.rectangle(x + 36, y + 20, 8, 8) # Right eye
    display.rectangle(x + 20, y + 40, 24, 6) # mouf