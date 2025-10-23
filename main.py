# ----------------------------------- DEV BRANCH ONLY -----------------------------------
# ----------------------------------- DEV BRANCH ONLY -----------------------------------
# ----------------------------------- DEV BRANCH ONLY -----------------------------------
# ----------------------------------- DEV BRANCH ONLY -----------------------------------
# ----------------------------------- DEV BRANCH ONLY -----------------------------------



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

def draw_sprite_hurt(x, y):
    """Draws the 64x64 'hurt' sprite at (x, y)"""
    display.pen(15) # White background
    display.rectangle(x, y, 64, 64)
    display.pen(0) # Black ink
    display.rectangle(x + 5, y + 5, 54, 54) # Head outline
    # X eyes
    display.line(x + 20, y + 20, x + 28, y + 28)
    display.line(x + 20, y + 28, x + 28, y + 20)
    display.line(x + 36, y + 20, x + 44, y + 28)
    display.line(x + 36, y + 28, x + 44, y + 20)
    display.rectangle(x + 20, y + 45, 24, 6) # (octothorp)sadface
    display.text("Oof", x + 18, y + 5, scale=1) # oof

# ------- Main Draw Func's -------
def draw_home_screen(partial_update=False):
    """Draws the main pet screen. If partial update is True, it only redraws the HP text. If hurt stage changes, it will force a full redraw anyway."""
    global is_hurt

    # Check if sprite needs to change
    new_is_hurt = character_data['hp_current'] <= (character_data['hp_max'] // 4)
    sprite_changed = new_is_hurt != is_hurt
    
    if sprite_changed:
        partial_update = False # Full redraw forced if changed

    is_hurt = new_is_hurt

    if not partial_update:
        # Full redraw
        display.pen(15) # White
        display.clear()
        display.pen(0) # Blk
        
        # Header
        display.text(f"{character_data['name']} L{character_data['level']} {character_data['class']}", 5, 5, scale=2)
        display.line(0, 24, WIDTH, 24)
        
        # Sprite
        if is_hurt:
            draw_sprite_hurt(10, 30)
        else:
            draw_sprite_idle(10, 30)

        # Button Labels
        display.line(0, HEIGHT - 15, WIDTH, HEIGHT - 15)
        display.text("A: HP-", 10, HEIGHT - 10, scale=1)
        display.text("B: HP+", 70, HEIGHT - 10, scale=1)
        display.text("C: Stats", 130, HEIGHT - 10, scale=1)

        # --- (Semi) Partial Update Area ---
    # Always redraw the stats, even on a "partial" update.
    # We clear the area first.
    display.pen(15) # White
    display.rectangle(90, 30, 200, 70) # Clear stat text area
    
    display.pen(0) # Black
    display.text(f"HP: {character_data['hp_current']} / {character_data['hp_max']}", 90, 35, scale=2)
    display.text(f"AC: {character_data['ac']}", 90, 55, scale=2)
    display.text(f"Tmp: {character_data['hp_temp']}", 90, 75, scale=2)
    
    return "full" if not partial_update else "partial"

def draw_stats_screen():
    """Draws the ability score screen. (Full Refresh)"""
    display.pen(15) # White
    display.clear()
    display.pen(0) # Black
    
    display.text("ABILITY SCORES", 5, 5, scale=2)
    display.line(0, 24, WIDTH, 24)
    
    abilities = character_data.get('abilities', {})
    stats = [
        f"STR: {abilities.get('str', 10)}",
        f"DEX: {abilities.get('dex', 10)}",
        f"CON: {abilities.get('con', 10)}",
        f"INT: {abilities.get('int', 10)}",
        f"WIS: {abilities.get('wis', 10)}",
        f"CHA: {abilities.get('cha', 10)}",
    ]
    
    y_pos = 30
    for i in range(0, 6, 2): # Draw in two columns
        display.text(stats[i], 10, y_pos, scale=2)
        if i + 1 < 6:
            display.text(stats[i+1], 150, y_pos, scale=2)
        y_pos += 25

    # Button Label
    display.line(0, HEIGHT - 15, WIDTH, HEIGHT - 15)
    display.text("C: Home", 130, HEIGHT - 10, scale=1)

# --- Main Application Loop ---

def run():
    global current_screen, character_data
    
    print("Initializing D&D Pet (Badger 2040)...")
    LED.on()
    load_character()
    
    # Initial full draw
    draw_home_screen(partial_update=False)
    display.update_speed(badger2040.UPDATE_NORMAL)
    display.update()
    LED.off()

    while True:
        refresh_type = "none"  # "none", "partial", "full"
        
        # --- Button Polling ---
        # The Badger library handles debouncing with display.pressed()
        
        if display.pressed(badger2040.BUTTON_A): # HP -
            if current_screen == "home" and character_data['hp_current'] > 0:
                character_data['hp_current'] -= 1
                print("HP- pressed. HP:", character_data['hp_current'])
                refresh_type = "partial"

        elif display.pressed(badger2040.BUTTON_B): # HP +
            if current_screen == "home" and character_data['hp_current'] < character_data['hp_max']:
                character_data['hp_current'] += 1
                print("HP+ pressed. HP:", character_data['hp_current'])
                refresh_type = "partial"

        elif display.pressed(badger2040.BUTTON_C): # Stats / Home
            current_screen = "stats" if current_screen == "home" else "home"
            print("Menu pressed. Screen:", current_screen)
            refresh_type = "full"
        
        # Badger "UP" and "DOWN" could be used for Temp HP, Spells, etc.
        # elif display.pressed(badger2040.BUTTON_UP):
        #    ...
            
        # --- Drawing Logic ---
        if refresh_type != "none":
            LED.on() # Turn on LED during refresh
            
            if refresh_type == "full":
                # A full screen change
                display.update_speed(badger2040.UPDATE_NORMAL)
                if current_screen == "home":
                    draw_home_screen(partial_update=False)
                else:
                    draw_stats_screen()
                
            elif refresh_type == "partial":
                # Just an HP update
                # draw_home_screen(partial=True) will return "full" if
                # the sprite state changed, forcing a slower update.
                update_mode = draw_home_screen(partial_update=True)
                
                if update_mode == "full":
                    display.update_speed(badger2040.UPDATE_NORMAL)
                else:
                    display.update_speed(badger2040.UPDATE_FAST)
            
            # Commit the changes to the screen
            display.update()
            
            # Save data after any change
            save_character()
            
            LED.off()
            utime.sleep(0.1) # A small pause to prevent rapid button holds
            
        utime.sleep(0.01) # Main loop polling delay

# --- Start the App ---
if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("An error occurred:", e)
        # In case of crash, clear the screen and show error
        display.pen(15)
        display.clear()
        display.pen(0)
        display.text("An error occurred:", 10, 10, scale=2)
        display.text(str(e), 10, 30, scale=1, wordwrap=WIDTH-20)
        display.update()