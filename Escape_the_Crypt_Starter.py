# title: ESCAPE THE CRYPT - PYTHON STARTER
# script: python
# TIC-80 / pocketpy - Python, not Lua.
# Arrow keys: move. Z: talk / interact.
# F1: CODE. F2: SPRITES. F3: MAP.
# Search for "MISSION" to find your exercises.

# Each tile ID refers to a drawing in TIC-80.
FLOOR = 0
WALL = 1
TORCH = 2
NPC = 3
KEY = 4
LEVER = 5
DOOR = 6
RIGHT_EXIT = 7
LEFT_EXIT = 8
LEVER_ON = 10
HERO = 256

# Each room uses 30 x 14 tiles in the MAP editor.
# The rooms start at map columns 0, 32 and 64.
ROOMS = [
    ("Antechamber", 0),
    ("Relic Hall", 32),
    ("Exit Chamber", 64),
]

# Variables remember what happens in the game.
room_index = 0
player_x = 2
player_y = 6
has_key = False
lever_on = False
won = False
dialog_lines = None
dialog_index = 0


def tile_at(x, y):
    """Read a tile from the current room."""
    if x < 0 or x >= 30 or y < 0 or y >= 14:
        return WALL
    map_x = ROOMS[room_index][1]
    return mget(map_x + x, y)


def show_dialog(lines):
    """Display a message, one line at a time."""
    global dialog_lines, dialog_index
    dialog_lines = lines
    dialog_index = 0


def move_player(dx, dy):
    """Move one tile; walls and objects are solid."""
    global player_x, player_y, room_index
    next_x = player_x + dx
    next_y = player_y + dy
    tile = tile_at(next_x, next_y)

    if tile in (WALL, NPC, KEY, LEVER, LEVER_ON, DOOR):
        return

    if tile == RIGHT_EXIT and room_index < len(ROOMS) - 1:
        room_index += 1
        player_x = 1
        player_y = next_y
    elif tile == LEFT_EXIT and room_index > 0:
        room_index -= 1
        player_x = 28
        player_y = next_y
    else:
        player_x = next_x
        player_y = next_y


def interact():
    """Examine an NPC or object next to the hero."""
    global has_key, lever_on, won
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for dx, dy in directions:
        x = player_x + dx
        y = player_y + dy
        tile = tile_at(x, y)

        if tile == NPC:
            # MISSION 3: Write your own character dialogues.
            # BONUS: Make them react when has_key is True.
            if room_index == 0:
                show_dialog(["Welcome to the crypt.",
                             "The way out lies ahead..."])
            elif room_index == 1:
                show_dialog(["The relics hide old secrets."])
            else:
                show_dialog(["The final door is nearby."])
            return

        elif tile == KEY:
            # MISSION 4: Make the key collectible.
            # 1. Set has_key = True.
            # 2. Remove the key using mset(..., FLOOR).
            # 3. Show a message describing what happened.
            show_dialog(["A rusty key. Can you pick it up?"])
            return

        elif tile == LEVER:
            # MISSION 5: Activate the lever.
            # 1. Set lever_on = True.
            # 2. Change its tile to LEVER_ON with mset().
            # 3. Tell the player what happened.
            show_dialog(["An ancient lever. It will not budge."])
            return

        elif tile == DOOR:
            # MISSION 6: Escape the crypt!
            # Win only if has_key AND lever_on are both True.
            # Otherwise, explain what the player still needs.
            show_dialog(["The exit door is locked."])
            return

    show_dialog(["There is nothing to examine here."])


def draw_game():
    """Draw the room, character and interface."""
    cls(0)
    if won:
        rect(12, 22, 216, 92, 1)
        rectb(12, 22, 216, 92, 10)
        print("ESCAPE THE CRYPT", 64, 42, 10)
        print("You escaped the crypt!", 55, 65, 15)
        print("Congratulations!", 74, 81, 12)
        return

    map_x = ROOMS[room_index][1]
    map(map_x, 0, 30, 14, 0, 0)

    # MISSION 1: Redraw hero sprite #256 in SPRITES.
    # MISSION 2: Change the rooms in MAP.
    spr(HERO, player_x * 8, player_y * 8, 0)

    rect(0, 112, 240, 24, 0)
    print(ROOMS[room_index][0], 4, 115, 15)
    print("KEY:" + ("YES" if has_key else "NO"), 118, 115, 10)
    print("LEVER:" + ("ON" if lever_on else "OFF"), 174, 115, 11)

    if dialog_lines is not None:
        print(dialog_lines[dialog_index], 4, 125, 12)
    else:
        print("ARROWS: MOVE   Z: TALK / USE", 4, 125, 13)


def TIC():
    """TIC-80 calls this function about 60 times/second."""
    global dialog_lines, dialog_index
    if not won:
        if dialog_lines is not None:
            if btnp(4):
                dialog_index += 1
                if dialog_index >= len(dialog_lines):
                    dialog_lines = None
        else:
            if btnp(4):
                interact()
            if btnp(0, 12, 8):
                move_player(0, -1)
            elif btnp(1, 12, 8):
                move_player(0, 1)
            elif btnp(2, 12, 8):
                move_player(-1, 0)
            elif btnp(3, 12, 8):
                move_player(1, 0)
    draw_game()
