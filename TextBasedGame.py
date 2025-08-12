# Miniece Ragin

from typing import Dict, List


def show_instructions() -> None:
    """
    Print the game title, objective, and the available commands.
    """
    print("HELLBREAK — A Text Adventure")
    print("Collect all 6 items before you reach the Gates, or be defeated by The One.")
    print("Move commands: go North, go South, go East, go West")
    print("Add to Inventory: get 'item name'")
    print("-" * 30)


def show_status(current_room: str, inventory: List[str], rooms: Dict[str, dict]) -> None:
    """
    Display the player's current status:
      - Current room
      - Inventory contents
      - Item present in the room (if any)
    """
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    # Show an item if the room has one
    item_in_room = rooms[current_room].get("item")
    if item_in_room:
        print(f"You see a {item_in_room}")
    print("-" * 30)


def normalize_input(raw: str) -> str:
    """
    Normalize player input for easier parsing while preserving item names after 'get '.
    """
    return raw.strip()


def main() -> None:
    """
    Orchestrates the game loop:
      - Holds the map/rooms dictionary
      - Tracks inventory and current room
      - Parses and validates player commands
      - Ends when the player wins or loses
    """
    # ----------------------------
    # WORLD SETUP
    # ----------------------------
    rooms: Dict[str, dict] = {
        #Starting area (no item).
        "Your Room": {
            "South": "Apothecary"
        },
        "Apothecary": {
            "North": "Your Room",
            "West": "Grand Hallway",
            "item": "Potions"
        },
        "Grand Hallway": {
            "North": "Weaponry",
            "East": "Apothecary",
            "West": "Gates",
            "South": "Mess Hall",
            "item": "Letter"
        },
        "Mess Hall": {
            "North": "Grand Hallway",
            "East": "Armory",
            "item": "Locket"
        },
        "Armory": {
            "West": "Mess Hall",
            "item": "Clothing"
        },
        # Villain room (no item). Entering here with < 6 items = loss; with all 6 = win.
        "Gates": {
            "East": "Grand Hallway"
        },
        "Weaponry": {
            "East": "Grand Lair",
            "South": "Grand Hallway",
            "item": "Scythe"
        },
        "Grand Lair": {
            "West": "Weaponry",
            "item": "Key"
        },
    }

    # Items required to win = count of rooms that define an 'item'
    required_items = {info["item"] for info in rooms.values() if "item" in info}
    total_to_collect = len(required_items)

    # ----------------------------
    # GAME STATE
    # ----------------------------
    current_room: str = "Your Room"
    inventory: List[str] = []

    # ----------------------------
    # INTRO
    # ----------------------------
    show_instructions()

    # ----------------------------
    # MAIN GAME LOOP
    # ----------------------------
    while True:
        show_status(current_room, inventory, rooms)

        player_input = normalize_input(input("Enter your move: "))

        # Allow graceful exit for testers
        if player_input.lower() in {"quit", "exit"}:
            print("Thanks for playing. Goodbye!")
            break

        # ----------------------------
        # COMMAND PARSING
        # ----------------------------
        # Movement: "go North/South/East/West"
        if player_input.lower().startswith("go "):
            direction = player_input[3:].strip().capitalize()  # normalize to 'North' etc.
            if direction not in {"North", "South", "East", "West"}:
                print("Invalid direction. Use: North, South, East, or West.")
                continue

            # Validate move exists from current_room
            next_room = rooms[current_room].get(direction)
            if not next_room:
                print("You can't go that way.")
                continue

            current_room = next_room

            # Check for win/lose if we stepped into the villain room
            if current_room == "Gates":
                if len(inventory) == total_to_collect:
                    print("Congratulations! You have collected all items and defeated The One!")
                    print("Thanks for playing the game. Hope you enjoyed it.")
                else:
                    print("NOM NOM...GAME OVER!")
                    print("You faced The One without everything you needed.")
                    print("Thanks for playing the game. Hope you enjoyed it.")
                break

            continue

        # Item pickup: "get Item Name"
        if player_input.lower().startswith("get "):
            requested_item = player_input[4:].strip()
            room_item = rooms[current_room].get("item")

            if not room_item:
                print("There is no item to get here.")
                continue

            # Validate the typed item matches what's in the room (case-insensitive)
            if requested_item.lower() != room_item.lower():
                print(f"That item isn't here. You see a {room_item}.")
                continue

            # Prevent duplicates
            if room_item in inventory:
                print(f"You already picked up the {room_item}.")
                continue

            # Success: add to inventory, remove from room
            inventory.append(room_item)
            del rooms[current_room]["item"]
            print(f"{room_item} added to your inventory!")

            # Optional: check if player now has all items (they still must reach Gates to win)
            if len(inventory) == total_to_collect:
                print("You have gathered everything you need. Find the Gates!")

            continue

        # If we reach here, the command format didn't match any expected pattern
        print("Invalid command. Try: 'go North' or \"get Item Name\".")


# Run the game when executed directly
if __name__ == "__main__":
    main()
