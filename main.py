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
