import os, sys, time, random, msvcrt, math, winsound, json

# ===== Colors / Helpers =====
RESET = "\033[0m"
FG = "\033[38;5;{}m"

def color(txt, code):
    return f"{FG.format(code)}{txt}{RESET}"

GREEN = 46  # General green
GRAY = 240
RED = 196  # Damage, errors
YELLOW = 226  # Warnings, biomes
CYAN = 51  # Stats, info
MAGENTA = 201
WHITE = 255  # Snow
LIME = 118   # Grass
BLUE = 27    # Stats text
HEALTH_GREEN = 82  # Health
DAMAGE_RED = 160  # Damage
DIAMOND_BLUE = 39  # Diamond tier
BROWN = 130  # Wood armor color
GOLD_COLOR = 220  # Gold armor color

# ===== Sound Effects =====
def play_sound(event_type):
    if os.name != "nt":
        return
    if event_type == "move":
        winsound.Beep(440, 100)
    elif event_type == "pickup":
        winsound.Beep(880, 150)
    elif event_type == "combat":
        winsound.Beep(220, 200)
    elif event_type == "equip":
        winsound.Beep(660, 120)
    elif event_type == "use_item":
        winsound.Beep(770, 130)
    elif event_type == "shop":
        winsound.Beep(990, 140)
    elif event_type == "break":
        winsound.Beep(200, 300)
    elif event_type == "drop":
        winsound.Beep(300, 100)
    elif event_type == "open":
        winsound.Beep(500, 80)
    elif event_type == "victory":
        winsound.Beep(800, 300)
    elif event_type == "flee":
        winsound.Beep(1000, 50)
    elif event_type == "cross":
        winsound.Beep(1000, 200)
    elif event_type == "travel":
        winsound.Beep(600, 200)
    elif event_type == "transfer":
        winsound.Beep(700, 100)
    elif event_type == "death":
        winsound.Beep(100, 500)
    elif event_type == "enemy_flee":
        winsound.Beep(400, 100)
    elif event_type == "damage_player":
        winsound.Beep(150, 200)
    elif event_type == "damage_enemy":
        winsound.Beep(250, 200)
    elif event_type == "heal":
        winsound.Beep(550, 150)
    elif event_type == "open_chest":
        winsound.Beep(450, 120)
    elif event_type == "open_inventory":
        winsound.Beep(500, 100)
    elif event_type == "scroll":
        winsound.Beep(300, 50)

# ===== Item =====
class Item:
    SYMBOLS = {
        # Treasures
        "Crystal": "♦",
        "Gem": "◈",
        "Gold": "¤",
        "Sapphire": "▽",

        # Swords
        "Wood Sword": "†",
        "Silver Sword": "†",
        "Bronze Sword": "†",
        "Gold Sword": "†",
        "Diamond Sword": "†",
        "Broken Wood Sword": "†̷",
        "Broken Silver Sword": "†̷",
        "Broken Bronze Sword": "†̷",
        "Broken Gold Sword": "†̷",
        "Broken Diamond Sword": "†̷",

        # Long Swords
        "Wood Long Sword": "‡",
        "Silver Long Sword": "‡",
        "Bronze Long Sword": "‡",
        "Gold Long Sword": "‡",
        "Diamond Long Sword": "‡",
        "Broken Wood Long Sword": "‡̷",
        "Broken Silver Long Sword": "‡̷",
        "Broken Bronze Long Sword": "‡̷",
        "Broken Gold Long Sword": "‡̷",
        "Broken Diamond Long Sword": "‡̷",

        # Spears
        "Wood Spear": "┣",
        "Silver Spear": "┣",
        "Bronze Spear": "┣",
        "Gold Spear": "┣",
        "Diamond Spear": "┣",
        "Broken Wood Spear": "┣̷",
        "Broken Silver Spear": "┣̷",
        "Broken Bronze Spear": "┣̷",
        "Broken Gold Spear": "┣̷",
        "Broken Diamond Spear": "┣̷",

        # Knives
        "Wood Knife": "⌐",
        "Silver Knife": "⌐",
        "Bronze Knife": "⌐",
        "Gold Knife": "⌐",
        "Diamond Knife": "⌐",
        "Broken Wood Knife": "⌐̷",
        "Broken Silver Knife": "⌐̷",
        "Broken Bronze Knife": "⌐̷",
        "Broken Gold Knife": "⌐̷",
        "Broken Diamond Knife": "⌐̷",

        # Maces
        "Wood Mace": "♣",
        "Silver Mace": "♣",
        "Bronze Mace": "♣",
        "Gold Mace": "♣",
        "Diamond Mace": "♣",
        "Broken Wood Mace": "♣̷",
        "Broken Silver Mace": "♣̷",
        "Broken Bronze Mace": "♣̷",
        "Broken Gold Mace": "♣̷",
        "Broken Diamond Mace": "♣̷",

        # Shovels
        "Wood Shovel": "♠",
        "Silver Shovel": "♠",
        "Bronze Shovel": "♠",
        "Gold Shovel": "♠",
        "Diamond Shovel": "♠",
        "Broken Wood Shovel": "♠̷",
        "Broken Silver Shovel": "♠̷",
        "Broken Bronze Shovel": "♠̷",
        "Broken Gold Shovel": "♠̷",
        "Broken Diamond Shovel": "♠̷",

        # Bows
        "Wood Bow": "⌒",
        "Silver Bow": "⌒",
        "Bronze Bow": "⌒",
        "Gold Bow": "⌒",
        "Diamond Bow": "⌒",
        "Broken Wood Bow": "⌒̷",
        "Broken Silver Bow": "⌒̷",
        "Broken Bronze Bow": "⌒̷",
        "Broken Gold Bow": "⌒̷",
        "Broken Diamond Bow": "⌒̷",

        # CrossBows
        "Wood CrossBow": "╬",
        "Silver CrossBow": "╬",
        "Bronze CrossBow": "╬",
        "Gold CrossBow": "╬",
        "Diamond CrossBow": "╬",
        "Broken Wood CrossBow": "╬̷",
        "Broken Silver CrossBow": "╬̷",
        "Broken Bronze CrossBow": "╬̷",
        "Broken Gold CrossBow": "╬̷",
        "Broken Diamond CrossBow": "╬̷",

        # Arrows
        "Arrow Quill": "➤",

        # Shields
        "Wood Shield": "◙",
        "Silver Shield": "◙",
        "Bronze Shield": "◙",
        "Gold Shield": "◙",
        "Diamond Shield": "◙",
        "Broken Wood Shield": "◙̷",
        "Broken Silver Shield": "◙̷",
        "Broken Bronze Shield": "◙̷",
        "Broken Gold Shield": "◙̷",
        "Broken Diamond Shield": "◙̷",

        # Armor
        "Wood Chest Piece": "☰",
        "Silver Chest Piece": "☰",
        "Bronze Chest Piece": "☰",
        "Gold Chest Piece": "☰",
        "Diamond Chest Piece": "☰",
        "Broken Wood Chest Piece": "☰̷",
        "Broken Silver Chest Piece": "☰̷",
        "Broken Bronze Chest Piece": "☰̷",
        "Broken Gold Chest Piece": "☰̷",
        "Broken Diamond Chest Piece": "☰̷",

        "Wood Helmet": "⍤",
        "Silver Helmet": "⍤",
        "Bronze Helmet": "⍤",
        "Gold Helmet": "⍤",
        "Diamond Helmet": "⍤",
        "Broken Wood Helmet": "⍤̷",
        "Broken Silver Helmet": "⍤̷",
        "Broken Bronze Helmet": "⍤̷",
        "Broken Gold Helmet": "⍤̷",
        "Broken Diamond Helmet": "⍤̷",

        "Wood Pants": "∥",
        "Silver Pants": "∥",
        "Bronze Pants": "∥",
        "Gold Pants": "∥",
        "Diamond Pants": "∥",
        "Broken Wood Pants": "∥̷",
        "Broken Silver Pants": "∥̷",
        "Broken Bronze Pants": "∥̷",
        "Broken Gold Pants": "∥̷",
        "Broken Diamond Pants": "∥̷",

        "Wood Boots": "┗",
        "Silver Boots": "┗",
        "Bronze Boots": "┗",
        "Gold Boots": "┗",
        "Diamond Boots": "┗",
        "Broken Wood Boots": "┗̷",
        "Broken Silver Boots": "┗̷",
        "Broken Bronze Boots": "┗̷",
        "Broken Gold Boots": "┗̷",
        "Broken Diamond Boots": "┗̷",

        # Potions
        "Wood Potion": "⍥",
        "Silver Potion": "⍥",
        "Bronze Potion": "⍥",
        "Gold Potion": "⍥",
        "Diamond Potion": "⍥",

        # Bags
        "Wood Bag": "▣",
        "Silver Bag": "▣",
        "Bronze Bag": "▣",
        "Gold Bag": "▣",
        "Diamond Bag": "▣",

        # Crosses
        "Wood Cross": "✚",
        "Silver Cross": "✚",
        "Bronze Cross": "✚",
        "Gold Cross": "✚",
        "Diamond Cross": "✚",
        "Broken Wood Cross": "✚̷",
        "Broken Silver Cross": "✚̷",
        "Broken Bronze Cross": "✚̷",
        "Broken Gold Cross": "✚̷",
        "Broken Diamond Cross": "✚̷",

        # Stun Rings
        "Wood Stun Ring": "∘",
        "Silver Stun Ring": "∘",
        "Bronze Stun Ring": "∘",
        "Gold Stun Ring": "∘",
        "Diamond Stun Ring": "∘",
        "Broken Wood Stun Ring": "∘̷",
        "Broken Silver Stun Ring": "∘̷",
        "Broken Bronze Stun Ring": "∘̷",
        "Broken Gold Stun Ring": "∘̷",
        "Broken Diamond Stun Ring": "∘̷",

        # Daggers
        "Wood Dagger": "‡",
        "Silver Dagger": "‡",
        "Bronze Dagger": "‡",
        "Gold Dagger": "‡",
        "Diamond Dagger": "‡",
    }

    TIERS = {
        "Wood": {"color": GRAY, "multiplier": 1.0, "rarity": 0, "stun_chance": 0.1},
        "Silver": {"color": CYAN, "multiplier": 1.5, "rarity": 1, "stun_chance": 0.2},
        "Bronze": {"color": YELLOW, "multiplier": 2.0, "rarity": 2, "stun_chance": 0.3},
        "Gold": {"color": RED, "multiplier": 3.0, "rarity": 3, "stun_chance": 0.4},
        "Diamond": {"color": DIAMOND_BLUE, "multiplier": 4.0, "rarity": 4, "stun_chance": 0.5},
    }

    TYPE_META = {
        "Sword": {"type": "weapon", "damage": 5, "durability": 10, "weapon_type": "Sword"},
        "Long Sword": {"type": "weapon", "damage": 7, "durability": 15, "weapon_type": "Long Sword"},
        "Spear": {"type": "weapon", "damage": 5, "durability": 10, "weapon_type": "Spear", "empale_chance_base": 0.05},
        "Knife": {"type": "weapon", "damage": 3, "durability": 10, "weapon_type": "Knife", "stun_chance_base": 0.1},
        "Mace": {"type": "weapon", "damage": 6, "durability": 10, "weapon_type": "Mace", "stun_chance_base": 0.1},
        "Shovel": {"type": "weapon", "damage": 7, "durability": 10, "weapon_type": "Shovel"},
        "Bow": {"type": "bow", "damage": 10, "durability": 30},
        "CrossBow": {"type": "bow", "damage": 15, "durability": 40},
        "Shield": {"type": "shield", "durability": 5},
        "Chest Piece": {"type": "armor", "chestpiece": True, "durability": 20},
        "Helmet": {"type": "armor", "helmet": True, "durability": 15},
        "Pants": {"type": "armor", "pants": True, "durability": 18},
        "Boots": {"type": "armor", "boots": True, "durability": 12},
        "Potion": {"type": "consumable"},
        "Bag": {"type": "bag"},
        "Cross": {"type": "cross", "uses": 1},
        "Stun Ring": {"type": "ring", "uses": 5},
        "Arrow Quill": {"type": "quill", "arrows": 10},
        "Crystal": {"type": "crystal"},
        "Gem": {"type": "gem"},
        "Sapphire": {"type": "sapphire"},
        "Dagger": {"type": "dagger", "damage": 12, "uses": 5},
    }

    def __init__(self, name, char=None, color=None, meta=None):
        self.name = name
        tier = next((t for t in self.TIERS if t in name), "Wood")
        self.char = char if char else self.SYMBOLS.get(name, "*")
        self.color = color if color else self.TIERS[tier]["color"]
        self.meta = meta or {}
        self.meta["tier"] = tier
        item_type = name.split()[-1] if "Long" not in name else ' '.join(name.split()[-2:])
        type_meta = self.TYPE_META.get(item_type, {})
        self.meta.update({k: v for k, v in type_meta.items() if k not in self.meta})
        mult = self.TIERS[tier]["multiplier"]
        if "damage" in self.meta:
            self.meta["damage"] = int(self.meta["damage"] * mult)
        if "durability" in self.meta:
            self.meta["durability"] = int(self.meta["durability"] * mult)
        if "uses" in self.meta:
            self.meta["uses"] = int(self.meta["uses"] * mult)
        if "arrows" in self.meta:
            self.meta["arrows"] = int(self.meta["arrows"] * mult)
        if "empale_chance_base" in self.meta:
            self.meta["empale_chance"] = self.meta["empale_chance_base"] * mult
        if "stun_chance_base" in self.meta:
            self.meta["stun_chance"] = self.meta["stun_chance_base"] * mult

    def to_dict(self):
        return {
            'name': self.name,
            'char': self.char,
            'color': self.color,
            'meta': self.meta
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['name'], d['char'], d['color'], d['meta'])

    def render(self):
        return color(self.char, self.color)

    def copy(self):
        return Item(self.name, self.char, self.color, dict(self.meta))

    def get_display_name(self):
        parts = self.name.split()
        if parts[0] == "Broken":
            tier = parts[1]
            item_type = ' '.join(parts[2:])
            rarity_color = self.TIERS.get(tier, {"color": GRAY})["color"]
            return f"Broken {item_type} ({color(tier.lower(), rarity_color)})"
        elif parts[-1] in ["Quill", "Crystal", "Gem", "Sapphire"]:
            return self.name
        else:
            tier = parts[0]
            item_type = ' '.join(parts[1:])
            rarity_color = self.TIERS.get(tier, {"color": GRAY})["color"]
            return f"{item_type} ({color(tier.lower(), rarity_color)})"

    def get_details(self):
        details = f"Name: {self.get_display_name()}\n"
        details += f"Type: {self.meta.get('type', 'Unknown')}\n"
        tier = self.meta.get('tier', 'Wood')
        details += f"Rarity: {self.TIERS[tier]['rarity']}\n"
        if 'durability' in self.meta:
            details += f"Durability: {self.meta['durability']}\n"
        if 'uses' in self.meta:
            details += f"Uses: {self.meta['uses']}\n"
        if 'arrows' in self.meta:
            details += f"Arrows: {self.meta['arrows']}\n"
        if 'damage' in self.meta:
            details += f"Damage: {self.meta['damage']}\n"
        if 'empale_chance' in self.meta:
            details += f"Empale Chance: {int(self.meta['empale_chance'] * 100)}%\n"
        if 'stun_chance' in self.meta:
            details += f"Stun Chance: {int(self.meta['stun_chance'] * 100)}%\n"
        return details.strip()

# ===== Inventory =====
class Inventory:
    def __init__(self, owner, max_size=20):
        self.owner = owner
        self.max_size = max_size
        self.items = []
        self.selected = 0
        self.collapsed = True

    def to_dict(self):
        return {
            'max_size': self.max_size,
            'items': [it.to_dict() for it in self.items],
            'selected': self.selected,
            'collapsed': self.collapsed
        }

    @classmethod
    def from_dict(cls, d, owner):
        inv = cls(owner, d['max_size'])
        inv.items = [Item.from_dict(it) for it in d['items']]
        inv.selected = d['selected']
        inv.collapsed = d['collapsed']
        return inv

    def add(self, item):
        if len(self.items) < self.max_size:
            self.items.append(item)
            return True
        return False

    def remove_raw(self, idx):
        if 0 <= idx < len(self.items):
            return self.items.pop(idx)
        return None

    def remove_one_by_name(self, name):
        for i, it in enumerate(self.items):
            if it.name == name:
                return self.items.pop(i)
        return None

    def is_full(self):
        return len(self.items) >= self.max_size

    def toggle_collapse(self):
        self.collapsed = not self.collapsed
        self.selected = max(0, min(self.selected, len(self.get_display_groups()) - 1))

    def get_display_groups(self):
        order = []
        counts = {}
        for it in self.items:
            if it.name not in counts:
                order.append(it.name)
                counts[it.name] = 0
            counts[it.name] += 1
        groups = []
        for name in order:
            count = counts[name]
            it = next(i for i in self.items if i.name == name)
            display = f"{it.char} {it.get_display_name()}" + (f" (x{count})" if count > 1 else "")
            groups.append((display, count, name))
        return groups

    def get_display_items(self):
        counts = {}
        displays = []
        for it in self.items:
            name = it.name
            counts[name] = counts.get(name, 0) + 1
            display = f"{it.char} {it.get_display_name()} ({counts[name]})"
            displays.append(display)
        return displays

    def get_selected_item(self):
        if self.collapsed:
            groups = self.get_display_groups()
            if self.selected < len(groups):
                _, _, name = groups[self.selected]
                for it in self.items:
                    if it.name == name:
                        return it
        else:
            if 0 <= self.selected < len(self.items):
                return self.items[self.selected]
        return None

    def render_ui(self, title="Inventory"):
        os.system("cls" if os.name == "nt" else "clear")
        owner = "Player" if self.owner and hasattr(self.owner, "char") else "Chest"
        print(color(f"== {title} ({len(self.items)}/{self.max_size}) ==", GREEN))
        if not self.items:
            print("  (empty)")
            return
        if self.collapsed:
            groups = self.get_display_groups()
            for i, (txt, count, name) in enumerate(groups):
                pointer = "►" if i == self.selected else "  "
                equipped = ""
                if hasattr(self.owner, "is_equipped") and any(it is self.owner.weapon or it is self.owner.armor or it is self.owner.shield or it is self.owner.bow or it is self.owner.quiver or it is self.owner.bag or it is self.owner.cross or it is self.owner.ring or it is self.owner.helmet or it is self.owner.pants or it is self.owner.boots or it is self.owner.dagger for it in self.items if it.name == name):
                    equipped = " [EQUIPPED]"
                print(f"{pointer} {txt}{equipped}")
        else:
            displays = self.get_display_items()
            for i, display in enumerate(displays):
                pointer = "►" if i == self.selected else "  "
                equipped = ""
                it = self.items[i]
                if hasattr(self.owner, "is_equipped") and self.owner.is_equipped(it):
                    equipped = f" [EQUIPPED]"
                print(f"{pointer} {display}{equipped}")

        selected_item = self.get_selected_item()
        if selected_item:
            print("\nItem Details:")
            print(selected_item.get_details())

    def equip_toggle_selected(self):
        if not self.items:
            return
        if self.collapsed:
            groups = self.get_display_groups()
            if self.selected >= len(groups): return
            _, _, name = groups[self.selected]
            for i, it in enumerate(self.items):
                if it.name == name:
                    return self._toggle_equip_by_index(i)
        else:
            if 0 <= self.selected < len(self.items):
                return self._toggle_equip_by_index(self.selected)

    def _toggle_equip_by_index(self, idx):
        it = self.items[idx]
        player = self.owner
        if not hasattr(player, "equip"):
            return
        if player.is_equipped(it):
            player.unequip(it)
            play_sound("equip")
            return "unequipped"
        if it.meta.get("type") in ("weapon", "bow", "armor", "shield", "quill", "bag", "cross", "ring", "dagger"):
            player.equip(it)
            play_sound("equip")
            return "equipped"
        return None

    def use_selected(self):
        if not self.items:
            return None
        if self.collapsed:
            groups = self.get_display_groups()
            if self.selected >= len(groups): return None
            _, _, name = groups[self.selected]
            for i, it in enumerate(self.items):
                if it.name == name:
                    return self._use_by_index(i)
        else:
            if 0 <= self.selected < len(self.items):
                return self._use_by_index(self.selected)
        return None

    def _use_by_index(self, idx):
        it = self.items[idx]
        player = self.owner
        if not hasattr(player, "consume_item"):
            return None
        if it.meta.get("type") == "consumable" and "Potion" in it.name:
            player.consume_item(it)
            self.remove_raw(idx)
            play_sound("use_item")
            return "used_potion"
        elif it.meta.get("type") == "crystal":
            player.consume_item(it)
            self.remove_raw(idx)
            play_sound("use_item")
            return "used_crystal"
        elif it.meta.get("type") == "gem":
            player.consume_item(it)
            self.remove_raw(idx)
            play_sound("use_item")
            return "used_gem"
        elif it.meta.get("type") == "sapphire":
            player.consume_item(it)
            self.remove_raw(idx)
            play_sound("use_item")
            return "used_sapphire"
        return None

    def drop_selected_one(self, drop_callback):
        if not self.items:
            return False
        if self.collapsed:
            groups = self.get_display_groups()
            if self.selected >= len(groups): return False
            _, _, name = groups[self.selected]
            itm = self.remove_one_by_name(name)
        else:
            if 0 <= self.selected < len(self.items):
                itm = self.remove_raw(self.selected)
            else:
                itm = None
        if itm:
            if hasattr(self.owner, "is_equipped") and self.owner.is_equipped(itm):
                self.items.append(itm)
                return False
            drop_callback(itm)
            play_sound("drop")
            return True
        return False

    def transfer_selected(self, target_inventory):
        if not self.items or target_inventory.is_full():
            return False
        if self.collapsed:
            groups = self.get_display_groups()
            if self.selected >= len(groups): return False
            _, _, name = groups[self.selected]
            itm = self.remove_one_by_name(name)
        else:
            if 0 <= self.selected < len(self.items):
                itm = self.remove_raw(self.selected)
            else:
                itm = None
        if itm:
            if hasattr(self.owner, "is_equipped") and self.owner.is_equipped(itm):
                self.items.append(itm)
                return False
            target_inventory.add(itm)
            play_sound("transfer")
            return True
        return False

# ===== Player =====
class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.char = '☺'
        self.inventory = Inventory(self, max_size=20)
        self.max_hp = 25
        self.hp = self.max_hp
        self.damage_mult = 1.0
        self.base_damage_mult = 1.0
        self.person_defense = 0.0
        self.stun_resist = 0.0
        self.dodge_chance = 0.0
        self.stun_duration = 0
        self.weapon = None
        self.bow = None
        self.armor = None
        self.helmet = None
        self.pants = None
        self.boots = None
        self.shield = None
        self.quiver = None
        self.bag = None
        self.cross = None
        self.ring = None
        self.dagger = None
        self.in_battle = False
        self.gold = 0
        self.coins_earned = 0
        self.coins_spent = 0
        self.sapphires_used = 0
        self.gems_used = 0
        self.crystals_used = 0
        self.items_broken = 0
        self.items_repaired = 0
        self.monsters_killed = 0
        self.times_fled = 0
        self.skill_points = 0
        self.skills = {
            "Blunt Weapon": 0,
            "Short Blade": 0,
            "Long Blade": 0,
            "Polearm": 0,
            "Archery": 0,
            "Agility": 0,
            "Endurance": 0,
            "Strength": 0,
        }
        self.dead = False

    def to_dict(self):
        eq = {
            'weapon': self.weapon.to_dict() if self.weapon else None,
            'bow': self.bow.to_dict() if self.bow else None,
            'armor': self.armor.to_dict() if self.armor else None,
            'helmet': self.helmet.to_dict() if self.helmet else None,
            'pants': self.pants.to_dict() if self.pants else None,
            'boots': self.boots.to_dict() if self.boots else None,
            'shield': self.shield.to_dict() if self.shield else None,
            'quiver': self.quiver.to_dict() if self.quiver else None,
            'bag': self.bag.to_dict() if self.bag else None,
            'cross': self.cross.to_dict() if self.cross else None,
            'ring': self.ring.to_dict() if self.ring else None,
            'dagger': self.dagger.to_dict() if self.dagger else None,
        }
        return {
            'x': self.x,
            'y': self.y,
            'max_hp': self.max_hp,
            'hp': self.hp,
            'damage_mult': self.damage_mult,
            'base_damage_mult': self.base_damage_mult,
            'person_defense': self.person_defense,
            'stun_resist': self.stun_resist,
            'dodge_chance': self.dodge_chance,
            'gold': self.gold,
            'coins_earned': self.coins_earned,
            'coins_spent': self.coins_spent,
            'sapphires_used': self.sapphires_used,
            'gems_used': self.gems_used,
            'crystals_used': self.crystals_used,
            'items_broken': self.items_broken,
            'items_repaired': self.items_repaired,
            'monsters_killed': self.monsters_killed,
            'times_fled': self.times_fled,
            'skill_points': self.skill_points,
            'skills': self.skills,
            'inventory': self.inventory.to_dict(),
            'equipped': eq,
            'dead': self.dead
        }

    @classmethod
    def from_dict(cls, d):
        p = cls(d['x'], d['y'])
        p.max_hp = d['max_hp']
        p.hp = d['hp']
        p.damage_mult = d['damage_mult']
        p.base_damage_mult = d['base_damage_mult']
        p.person_defense = d['person_defense']
        p.stun_resist = d['stun_resist']
        p.dodge_chance = d['dodge_chance']
        p.gold = d['gold']
        p.coins_earned = d['coins_earned']
        p.coins_spent = d['coins_spent']
        p.sapphires_used = d['sapphires_used']
        p.gems_used = d['gems_used']
        p.crystals_used = d['crystals_used']
        p.items_broken = d['items_broken']
        p.items_repaired = d['items_repaired']
        p.monsters_killed = d['monsters_killed']
        p.times_fled = d['times_fled']
        p.skill_points = d['skill_points']
        p.skills = d['skills']
        p.inventory = Inventory.from_dict(d['inventory'], p)
        eq = d['equipped']
        if eq['weapon']: p.weapon = Item.from_dict(eq['weapon'])
        if eq['bow']: p.bow = Item.from_dict(eq['bow'])
        if eq['armor']: p.armor = Item.from_dict(eq['armor'])
        if eq['helmet']: p.helmet = Item.from_dict(eq['helmet'])
        if eq['pants']: p.pants = Item.from_dict(eq['pants'])
        if eq['boots']: p.boots = Item.from_dict(eq['boots'])
        if eq['shield']: p.shield = Item.from_dict(eq['shield'])
        if eq['quiver']: p.quiver = Item.from_dict(eq['quiver'])
        if eq['bag']: p.bag = Item.from_dict(eq['bag'])
        if eq['cross']: p.cross = Item.from_dict(eq['cross'])
        if eq['ring']: p.ring = Item.from_dict(eq['ring'])
        if eq['dagger']: p.dagger = Item.from_dict(eq['dagger'])
        p.dead = d['dead']

        # Remap equipped to inventory items to maintain object identity
        equipped_slots = ['weapon', 'bow', 'armor', 'helmet', 'pants', 'boots', 'shield', 'quiver', 'bag', 'cross', 'ring', 'dagger']
        for slot in equipped_slots:
            equipped = getattr(p, slot)
            if equipped:
                found = False
                for inv_item in p.inventory.items:
                    if inv_item.name == equipped.name and inv_item.meta == equipped.meta and inv_item.char == equipped.char and inv_item.color == equipped.color:
                        setattr(p, slot, inv_item)
                        found = True
                        break
                if not found:
                    p.inventory.add(equipped)

        return p

    def upgrade_skill(self, skill_name):
        if self.skill_points > 0 and self.skills[skill_name] < 99:
            self.skills[skill_name] += 1
            self.skill_points -= 1
            if skill_name == "Strength":
                self.base_damage_mult += 0.01
            elif skill_name == "Endurance":
                self.person_defense += 0.005
            elif skill_name == "Agility":
                self.dodge_chance += 0.005

    def render(self):
        armor_pieces = [self.helmet, self.armor, self.pants, self.boots]
        tiers = [p.meta.get('tier') for p in armor_pieces if p]
        if len(tiers) == 4 and all(t == tiers[0] for t in tiers):
            tier = tiers[0]
            color_map = {
                "Wood": BROWN,
                "Silver": CYAN,
                "Bronze": YELLOW,
                "Gold": GOLD_COLOR,
                "Diamond": DIAMOND_BLUE,
            }
            return color(self.char, color_map.get(tier, GREEN))
        else:
            return color(self.char, GREEN)

    def is_equipped(self, item):
        return item is self.weapon or item is self.bow or item is self.armor or item is self.shield or item is self.quiver or item is self.bag or item is self.cross or item is self.ring or item is self.helmet or item is self.pants or item is self.boots or item is self.dagger

    def equip(self, item):
        t = item.meta.get("type")
        tier_mult = Item.TIERS[item.meta.get("tier", "Wood")]["multiplier"]
        if t == "weapon":
            self.weapon = item
        elif t == "bow":
            self.bow = item
        elif t == "armor":
            if "helmet" in item.meta:
                self.helmet = item
                self.stun_resist = 0.1 * tier_mult
                if "durability" not in item.meta:
                    item.meta["durability"] = 15 * tier_mult
            elif "chestpiece" in item.meta:
                self.armor = item
                if "durability" not in item.meta:
                    item.meta["durability"] = 20 * tier_mult
            elif "pants" in item.meta:
                self.pants = item
                if "durability" not in item.meta:
                    item.meta["durability"] = 18 * tier_mult
            elif "boots" in item.meta:
                self.boots = item
                self.dodge_chance = 0.05 * tier_mult
                if "durability" not in item.meta:
                    item.meta["durability"] = 12 * tier_mult
        elif t == "shield":
            self.shield = item
            if "durability" not in item.meta:
                item.meta["durability"] = 5 * tier_mult
        elif t == "quill":
            self.quiver = item
        elif t == "bag":
            self.bag = item
            self.inventory.max_size = 20 + int(5 * tier_mult)
        elif t == "cross":
            self.cross = item
        elif t == "ring":
            self.ring = item
        elif t == "dagger":
            self.dagger = item
            if "damage" not in item.meta:
                item.meta["damage"] = 12 * tier_mult
            if "uses" not in item.meta:
                item.meta["uses"] = 5 * tier_mult

    def unequip(self, item):
        if item is self.weapon:
            self.weapon = None
        elif item is self.bow:
            self.bow = None
        elif item is self.armor:
            self.armor = None
        elif item is self.helmet:
            self.helmet = None
            self.stun_resist = 0.0
        elif item is self.pants:
            self.pants = None
        elif item is self.boots:
            self.boots = None
            self.dodge_chance = 0.0
        elif item is self.shield:
            self.shield = None
        elif item is self.quiver:
            self.quiver = None
        elif item is self.bag:
            self.bag = None
            self.inventory.max_size = 20
        elif item is self.cross:
            self.cross = None
        elif item is self.ring:
            self.ring = None
        elif item is self.dagger:
            self.dagger = None

    def compute_armor_reduction(self):
        red = 0.0
        for piece, base_red in [(self.helmet, 0.05), (self.armor, 0.10), (self.pants, 0.08), (self.boots, 0.06)]:
            if piece:
                tier_mult = Item.TIERS[piece.meta.get("tier", "Wood")]["multiplier"]
                red += base_red * tier_mult
        red += 0.005 * self.skills["Endurance"]
        return min(0.99, red)

    def compute_outgoing_damage(self, action):
        base_unarmed = 2
        dmg = base_unarmed
        post = None
        skill_bonus = 0
        if action == "Punch":
            dmg = base_unarmed * self.base_damage_mult
        elif action == "Attack" and self.weapon and self.weapon.meta.get("type") == "weapon":
            tier_mult = Item.TIERS[self.weapon.meta.get("tier", "Wood")]["multiplier"]
            dmg = self.weapon.meta.get("damage", 5) * tier_mult
            wt = self.weapon.meta.get("weapon_type")
            if wt in ["Sword", "Long Sword"]:
                skill_bonus = self.skills["Long Blade"]
            elif wt == "Spear":
                skill_bonus = self.skills["Polearm"]
            elif wt in ["Knife"]:
                skill_bonus = self.skills["Short Blade"]
            elif wt in ["Mace", "Shovel"]:
                skill_bonus = self.skills["Blunt Weapon"]
            dmg += skill_bonus
            def post_weapon():
                if "durability" in self.weapon.meta:
                    self.weapon.meta["durability"] -= 1
                    if self.weapon.meta["durability"] <= 0:
                        broken_name = f"Broken {self.weapon.name}"
                        broken = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": self.weapon.meta["tier"]})
                        old_weapon = self.weapon
                        self.weapon = None
                        self.items_broken += 1
                        play_sound("break")
                        return ("weapon_broken", old_weapon, broken)
                return None
            post = post_weapon
        elif action == "Throw Spear" and self.weapon and self.weapon.meta.get("weapon_type") == "Spear":
            tier_mult = Item.TIERS[self.weapon.meta.get("tier", "Wood")]["multiplier"]
            dmg = self.weapon.meta.get("damage", 5) * tier_mult * 2  # Double damage for throw
            skill_bonus = self.skills["Polearm"]
            dmg += skill_bonus
            def post_throw():
                if "durability" in self.weapon.meta:
                    self.weapon.meta["durability"] -= 2  # Extra durability cost
                    if self.weapon.meta["durability"] <= 0:
                        broken_name = f"Broken {self.weapon.name}"
                        broken = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": self.weapon.meta["tier"]})
                        old_weapon = self.weapon
                        self.weapon = None
                        self.items_broken += 1
                        play_sound("break")
                        return ("weapon_broken", old_weapon, broken)
                return None
            post = post_throw
        elif action == "Shoot Bow" and self.bow and self.bow.meta.get("type") == "bow" and self.quiver and self.quiver.meta.get("arrows", 0) > 0:
            tier_mult = Item.TIERS[self.bow.meta.get("tier", "Wood")]["multiplier"]
            dmg = self.bow.meta.get("damage", 10) * tier_mult
            skill_bonus = self.skills["Archery"]
            dmg += skill_bonus
            def post_bow():
                self.quiver.meta["arrows"] -= 1
                result = None
                if self.quiver.meta["arrows"] <= 0:
                    old_quill = self.quiver
                    self.quiver = None
                    result = ("quill_empty", old_quill)
                if "durability" in self.bow.meta:
                    self.bow.meta["durability"] -= 1
                    if self.bow.meta["durability"] <= 0:
                        broken_name = f"Broken {self.bow.name}"
                        broken = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": self.bow.meta["tier"]})
                        old_bow = self.bow
                        self.bow = None
                        self.items_broken += 1
                        play_sound("break")
                        if result:
                            return ("quill_empty_and_bow_broken", old_quill, old_bow, broken)
                        return ("bow_broken", old_bow, broken)
                return result
            post = post_bow
        elif action == "Throw Dagger" and self.dagger and self.dagger.meta.get("uses", 0) > 0:
            tier_mult = Item.TIERS[self.dagger.meta.get("tier", "Wood")]["multiplier"]
            dmg = self.dagger.meta.get("damage", 12) * tier_mult
            skill_bonus = self.skills["Short Blade"]
            dmg += skill_bonus
            def post_dagger():
                self.dagger.meta["uses"] -= 1
                if self.dagger.meta["uses"] <= 0:
                    old_dagger = self.dagger
                    self.dagger = None
                    return ("dagger_depleted", old_dagger)
                return None
            post = post_dagger
        else:
            dmg = 1
            post = None
        dmg = int(math.ceil(dmg * self.damage_mult))
        return dmg, post

    def take_damage(self, dmg, shield_raised=False, dodge_attempt=False):
        shield_broken_item = None
        armor_broken_items = []
        blocked = False
        dodged = False
        stun_chance = Item.TIERS[self.shield.meta.get("tier", "Wood")]["stun_chance"] if self.shield and shield_raised else 0.0
        stunned = False
        effective_dodge_chance = self.dodge_chance
        if dodge_attempt:
            effective_dodge_chance += 0.4  # Base dodge boost for action, plus boots
            effective_dodge_chance = min(0.95, effective_dodge_chance)  # Max 95% to have slight fail chance
        if random.random() < effective_dodge_chance:
            dodged = True
            return 0, blocked, shield_broken_item, stunned, armor_broken_items, dodged
        if shield_raised and self.shield and self.shield.meta.get("durability", 0) > 0:
            self.shield.meta["durability"] -= 1
            blocked = True
            if random.random() < stun_chance:
                stunned = True
            if self.shield.meta["durability"] <= 0:
                old_shield = self.shield
                broken_name = f"Broken {old_shield.name}"
                shield_broken_item = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": old_shield.meta["tier"]})
                self.shield = None
                self.items_broken += 1
                play_sound("break")
            return 0, blocked, shield_broken_item, stunned, armor_broken_items, dodged
        dmg_after_person = dmg * (1 - self.person_defense)
        armor_red = self.compute_armor_reduction()
        actual = int(math.ceil(dmg_after_person * (1 - armor_red)))
        self.hp -= actual
        for piece in [self.helmet, self.armor, self.pants, self.boots]:
            if piece:
                piece.meta["durability"] -= 1
                if piece.meta["durability"] <= 0:
                    old_piece = piece
                    broken_name = f"Broken {old_piece.name}"
                    broken = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": old_piece.meta["tier"]})
                    if old_piece is self.helmet:
                        self.helmet = None
                        self.stun_resist = 0.0
                    elif old_piece is self.armor:
                        self.armor = None
                    elif old_piece is self.pants:
                        self.pants = None
                    elif old_piece is self.boots:
                        self.boots = None
                        self.dodge_chance = 0.0
                    armor_broken_items.append(broken)
                    self.items_broken += 1
                    play_sound("break")
        return actual, blocked, shield_broken_item, stunned, armor_broken_items, dodged

    def consume_item(self, item):
        tier_mult = Item.TIERS[item.meta.get("tier", "Wood")]["multiplier"]
        if "Potion" in item.name:
            heal = 10 * tier_mult
            self.hp = min(self.max_hp, self.hp + heal)
            play_sound("heal")
        elif item.meta.get("type") == "crystal":
            if self.base_damage_mult < 2.0:
                self.base_damage_mult += 0.01
            self.crystals_used += 1
        elif item.meta.get("type") == "gem":
            self.max_hp += 1
            self.hp += 1
            self.gems_used += 1
            play_sound("heal")
        elif item.meta.get("type") == "sapphire":
            self.person_defense = min(1.0, self.person_defense + 0.01)
            self.sapphires_used += 1

    def reset_on_respawn(self):
        self.max_hp = 25
        self.hp = 25
        self.damage_mult = 1.0
        self.base_damage_mult = 1.0
        self.person_defense = 0.0
        self.stun_resist = 0.0
        self.dodge_chance = 0.0
        self.gold = 0
        self.coins_earned = 0
        self.coins_spent = 0
        self.sapphires_used = 0
        self.gems_used = 0
        self.crystals_used = 0
        self.items_broken = 0
        self.items_repaired = 0
        self.monsters_killed = 0
        self.times_fled = 0
        self.skill_points = 0
        self.skills = {k: 0 for k in self.skills}
        self.dead = False

# ===== Chest =====
class Chest:
    TIERS = {
        "Wood": {"color": GRAY, "max_size": 5, "rarity": 0},
        "Silver": {"color": CYAN, "max_size": 7, "rarity": 1},
        "Bronze": {"color": YELLOW, "max_size": 9, "rarity": 2},
        "Gold": {"color": RED, "max_size": 12, "rarity": 3},
        "Diamond": {"color": DIAMOND_BLUE, "max_size": 15, "rarity": 4},
    }

    def __init__(self, x, y, tier="Wood"):
        self.x, self.y = x, y
        self.tier = tier
        self.char_closed = '☐'
        self.char_open = '☒'
        self.color = self.TIERS[tier]["color"]
        self.inventory = Inventory(self, max_size=self.TIERS[tier]["max_size"])
        self.opened = False
        self.is_mimic = random.random() < 0.1  # 10% chance to be a mimic

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'tier': self.tier,
            'opened': self.opened,
            'is_mimic': self.is_mimic,
            'inventory': self.inventory.to_dict()
        }

    @classmethod
    def from_dict(cls, d):
        c = cls(d['x'], d['y'], d['tier'])
        c.opened = d['opened']
        c.is_mimic = d['is_mimic']
        c.inventory = Inventory.from_dict(d['inventory'], c)
        return c

    def render(self):
        return color(self.char_open if self.opened else self.char_closed, self.color)

# ===== Shop =====
class Shop:
    TIERS = {
        "Wood": {"color": GRAY, "rarity": 0},
        "Silver": {"color": CYAN, "rarity": 1},
        "Bronze": {"color": YELLOW, "rarity": 2},
        "Gold": {"color": RED, "rarity": 3},
        "Diamond": {"color": DIAMOND_BLUE, "rarity": 4},
    }

    def __init__(self, x, y, map_id, tier="Wood"):
        self.x, self.y = x, y
        self.map_id = tuple(map_id)
        self.tier = tier
        self.char = 'S'
        self.color = self.TIERS[tier]["color"]
        self.inventory = Inventory(self, max_size=10)
        self.prices = {}

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'map_id': self.map_id,
            'tier': self.tier,
            'items_with_prices': [(it.to_dict(), self.prices.get(id(it), 10)) for it in self.inventory.items]
        }

    @classmethod
    def from_dict(cls, d):
        s = cls(d['x'], d['y'], d['map_id'], d['tier'])
        s.map_id = tuple(d['map_id'])
        s.inventory = Inventory(s, max_size=10)
        for it_d, price in d['items_with_prices']:
            it = Item.from_dict(it_d)
            s.inventory.add(it)
            s.prices[id(it)] = price
        return s

    def render(self):
        return color(self.char, self.color)

    def add_item(self, item, price):
        if price > 10:
            price = 10
        self.inventory.add(item)
        self.prices[id(item)] = price

    def buy_item(self, player, item_idx, to_inventory=False):
        if item_idx >= len(self.inventory.items):
            return False, "Invalid item"
        item = self.inventory.items[item_idx]
        price = self.prices.get(id(item), 10)
        if player.gold < price:
            return False, "Not enough gold"
        player.gold -= price
        player.coins_spent += price
        itm = self.inventory.remove_raw(item_idx)
        if itm:
            del self.prices[id(itm)]
            if to_inventory:
                if player.inventory.add(itm):
                    play_sound("shop")
                    return True, "Item transferred to inventory"
                else:
                    self.inventory.add(itm)
                    return False, "Inventory full"
            else:
                play_sound("shop")
                return True, itm
        return False, "Purchase failed"

# ===== RepairYard =====
class RepairYard:
    TIERS = {
        "Wood": {"color": GRAY, "rarity": 0},
        "Silver": {"color": CYAN, "rarity": 1},
        "Bronze": {"color": YELLOW, "rarity": 2},
        "Gold": {"color": RED, "rarity": 3},
        "Diamond": {"color": DIAMOND_BLUE, "rarity": 4},
    }

    def __init__(self, x, y, map_id, tier="Wood"):
        self.x, self.y = x, y
        self.map_id = tuple(map_id)
        self.tier = tier
        self.char = 'R'
        self.color = self.TIERS[tier]["color"]

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'map_id': self.map_id,
            'tier': self.tier
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['x'], d['y'], tuple(d['map_id']), d['tier'])

    def render(self):
        return color(self.char, self.color)

# ===== CrushYard =====
class CrushYard:
    TIERS = {
        "Wood": {"color": GRAY, "rarity": 0},
        "Silver": {"color": CYAN, "rarity": 1},
        "Bronze": {"color": YELLOW, "rarity": 2},
        "Gold": {"color": RED, "rarity": 3},
        "Diamond": {"color": DIAMOND_BLUE, "rarity": 4},
    }

    def __init__(self, x, y, map_id, tier="Wood"):
        self.x, self.y = x, y
        self.map_id = tuple(map_id)
        self.tier = tier
        self.char = 'C'
        self.color = self.TIERS[tier]["color"]

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'map_id': self.map_id,
            'tier': self.tier
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['x'], d['y'], tuple(d['map_id']), d['tier'])

    def render(self):
        return color(self.char, self.color)

# ===== Enemy =====
class Enemy:
    def __init__(self, x, y, name="Goblin", hp=10, damage=3, spawn_map=(0,0), enemy_type="melee", is_demon=False, has_shield=False, arrows=0, stun_chance=0.0, hit_chance=1.0, shield_charges=5):
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.map_id = tuple(spawn_map)
        self.char = {'Goblin': 'g', 'Phantom': 'P', 'Skeleton': 'S', 'Troll': 'T', 'Wraith': 'W', 'Orc': 'O', 'Spider': 'X', 'Drake': 'D', 'Defender': 'V', 'Dust Devil': 'U', 'Ice Witch': 'I', 'Golem': 'G', 'Wolf': 'w', 'Bandit': 'b', 'Slime': 'l', 'Miner Ghost': 'm', 'Rock Elemental': 'r', 'Yeti': 'y', 'Frost Giant': 'f', 'Snow Leopard': 'p', 'Scorpion': 'c', 'Mummy': 'u', 'Sand Serpent': 'n', 'Mirage Spirit': 'q', 'Desert Raider': 'd', 'Mimic': 'M'}[name]
        self.name = name
        self.hp = hp * (2 if is_demon else 1)
        self.max_hp = hp * (2 if is_demon else 1)
        self.damage = damage * (1.5 if is_demon else 1)
        self.enemy_type = enemy_type
        self.is_demon = is_demon
        self.has_shield = has_shield
        self.shield_charges = shield_charges if has_shield else 0
        self.shield_tier = "Wood" if has_shield else None
        self.agro_range = 5
        self.move_cooldown = 3 if enemy_type == "melee" else 2
        self._tick = 0
        self.in_combat = False
        self.arrows = arrows if arrows else (5 if enemy_type == "ranged" else 0)
        self.pursuing = False
        self.stun_duration = 0
        self.stun_chance = stun_chance
        self.hit_chance = hit_chance if enemy_type == "ranged" else 1.0

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'spawn_x': self.spawn_x,
            'spawn_y': self.spawn_y,
            'map_id': self.map_id,
            'name': self.name,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'damage': self.damage,
            'enemy_type': self.enemy_type,
            'is_demon': self.is_demon,
            'has_shield': self.has_shield,
            'shield_charges': self.shield_charges,
            'agro_range': self.agro_range,
            'move_cooldown': self.move_cooldown,
            '_tick': self._tick,
            'arrows': self.arrows,
            'pursuing': self.pursuing,
            'stun_duration': self.stun_duration,
            'stun_chance': self.stun_chance,
            'hit_chance': self.hit_chance
        }

    @classmethod
    def from_dict(cls, d):
        base_hp = d['max_hp'] / (2 if d['is_demon'] else 1)
        base_damage = d['damage'] / (1.5 if d['is_demon'] else 1)
        e = cls(d['x'], d['y'], d['name'], base_hp, base_damage, d['map_id'], d['enemy_type'], d['is_demon'], d['has_shield'], d['arrows'], d['stun_chance'], d['hit_chance'], d['shield_charges'])
        e.map_id = tuple(d['map_id'])
        e.hp = d['hp']
        e._tick = d['_tick']
        e.pursuing = d['pursuing']
        e.stun_duration = d['stun_duration']
        return e

    def render(self):
        col = MAGENTA if not self.is_demon else RED
        return color(self.char, col)

    def tick_move(self, world, player, wm):
        if self.stun_duration > 0:
            self.stun_duration -= 1
            return
        self._tick += 1
        if self._tick < self.move_cooldown:
            return
        self._tick = 0
        dist = abs(player.x - self.x) + abs(player.y - self.y)
        if dist <= self.agro_range and self.map_id == wm.current_map and not self.in_combat:
            self.pursuing = True
            dx = 0 if player.x == self.x else (1 if player.x > self.x else -1)
            dy = 0 if player.y == self.y else (1 if player.y > self.y else -1)
            self._attempt_move(dx, dy, world, wm)
        elif self.pursuing and dist > self.agro_range and not self.in_combat:
            self.pursuing = False
            dx = 0 if self.x == self.spawn_x else (-1 if self.x > self.spawn_x else 1)
            dy = 0 if self.y == self.spawn_y else (-1 if self.y > self.spawn_y else 1)
            self._attempt_move(dx, dy, world, wm)
        elif not self.pursuing and not self.in_combat:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            nx = self.x + dx
            ny = self.y + dy
            if abs(nx - self.spawn_x) <= 1 and abs(ny - self.spawn_y) <= 1:
                self._attempt_move(dx, dy, world, wm)

    def _attempt_move(self, dx, dy, world, wm):
        global dirty
        nx = self.x + dx
        ny = self.y + dy
        W, H = world.w, world.h
        if nx < 0:
            self.x = W-1
            wm.move_enemy_to_map(self, (wm.map_x-1, wm.map_y))
            dirty = True
            return
        if nx >= W:
            self.x = 0
            wm.move_enemy_to_map(self, (wm.map_x+1, wm.map_y))
            dirty = True
            return
        if ny < 0:
            self.y = H-1
            wm.move_enemy_to_map(self, (wm.map_x, wm.map_y-1))
            dirty = True
            return
        if ny >= H:
            self.y = 0
            wm.move_enemy_to_map(self, (wm.map_x, wm.map_y+1))
            dirty = True
            return
        chest = next((c for c in world.chests if c.x==nx and c.y==ny), None)
        shop = next((s for s in world.shops if s.x==nx and s.y==ny), None)
        if chest or shop:
            return
        self.x = nx
        self.y = ny
        dirty = True

    def take_damage(self, dmg, player, use_cross=False):
        if self.is_demon and use_cross and player.cross and player.cross.meta.get("uses", 0) > 0:
            self.hp = self.hp // 2
            player.cross.meta["uses"] -= 1
            print(f"\nYou used {player.cross.name}, halving {self.name}'s HP!")
            if player.cross.meta["uses"] <= 0:
                broken_name = f"Broken {player.cross.name}"
                broken = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": player.cross.meta["tier"]})
                player.cross = None
                return dmg, False, broken
            return dmg, False, None
        if self.has_shield and self.shield_charges > 0 and random.random() < 0.5:
            self.shield_charges -= 1
            print(f"\n{self.name} blocks with their shield!")
            if self.shield_charges <= 0:
                play_sound("break")
            return 0, True, None
        if random.random() > self.hit_chance:
            return 0, True, None
        actual = min(self.hp, dmg)
        self.hp -= actual
        if self.enemy_type == "ranged":
            self.arrows -= 1
        return actual, False, None

# ===== Biomes =====
BIOMES = {
    "grass": {"color": LIME, "enemy_weights": {"Goblin": 1.5, "Spider": 1.5, "Skeleton": 1.0, "Wolf": 1.4, "Bandit": 1.3, "Slime": 1.2}, "item_chance": 1.2},
    "stone": {"color": GRAY, "enemy_weights": {"Orc": 1.5, "Troll": 1.5, "Defender": 1.2, "Golem": 1.4, "Miner Ghost": 1.3, "Rock Elemental": 1.2}, "item_chance": 0.8},
    "snow": {"color": WHITE, "enemy_weights": {"Wraith": 1.5, "Phantom": 1.5, "Drake": 1.2, "Ice Witch": 1.4, "Yeti": 1.3, "Frost Giant": 1.2, "Snow Leopard": 1.1}, "item_chance": 0.9},
    "desert": {"color": YELLOW, "enemy_weights": {"Skeleton": 1.5, "Drake": 1.5, "Spider": 1.2, "Dust Devil": 1.5, "Scorpion": 1.4, "Mummy": 1.3, "Sand Serpent": 1.2, "Mirage Spirit": 1.1, "Desert Raider": 1.0}, "item_chance": 1.0},
}

def get_biome(mx, my):
    dist = max(abs(mx), abs(my))
    if dist < 2:
        return "grass"
    elif dist < 4:
        return random.choice(["grass", "stone"])
    elif dist < 6:
        return random.choice(["stone", "snow"])
    else:
        return random.choice(["snow", "desert"])

# ===== World =====
class World:
    def __init__(self, w, h, map_id=(0,0)):
        self.w, self.h = w, h
        self.items = []
        self.chests = []
        self.shops = []
        self.repair_yards = []
        self.crush_yards = []
        self.enemies = []
        self.map_id = tuple(map_id)
        self.biome = get_biome(map_id[0], map_id[1])
        self.floor_color = BIOMES[self.biome]["color"]

    def to_dict(self):
        return {
            'w': self.w,
            'h': self.h,
            'map_id': self.map_id,
            'biome': self.biome,
            'items': [[x, y, it.to_dict()] for x, y, it in self.items],
            'chests': [c.to_dict() for c in self.chests],
            'shops': [s.to_dict() for s in self.shops],
            'repair_yards': [r.to_dict() for r in self.repair_yards],
            'crush_yards': [c.to_dict() for c in self.crush_yards],
            'enemies': [e.to_dict() for e in self.enemies]
        }

    @classmethod
    def from_dict(cls, d):
        w = cls(d['w'], d['h'], d['map_id'])
        w.map_id = tuple(d['map_id'])
        w.biome = d['biome']
        w.floor_color = BIOMES[w.biome]["color"]
        w.items = [[x, y, Item.from_dict(it)] for x, y, it in d['items']]
        w.chests = [Chest.from_dict(c) for c in d['chests']]
        w.shops = [Shop.from_dict(s) for s in d['shops']]
        w.repair_yards = [RepairYard.from_dict(r) for r in d['repair_yards']]
        w.crush_yards = [CrushYard.from_dict(c) for c in d['crush_yards']]
        w.enemies = [Enemy.from_dict(e) for e in d['enemies']]
        return w

    def add_item(self, x, y, item):
        self.items.append([x, y, item])

    def add_chest(self, chest):
        self.chests.append(chest)

    def add_shop(self, shop):
        self.shops.append(shop)

    def add_repair_yard(self, yard):
        self.repair_yards.append(yard)

    def add_crush_yard(self, yard):
        self.crush_yards.append(yard)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def render(self, player, wm):
        os.system("cls" if os.name == "nt" else "clear")
        print(color(f"Map {self.map_id} ({self.biome.capitalize()})", YELLOW))
        for y in range(self.h):
            row = []
            for x in range(self.w):
                if x == player.x and y == player.y and wm.current_map == self.map_id:
                    row.append(player.render())
                else:
                    chest = next((c for c in self.chests if c.x == x and c.y == y), None)
                    if chest:
                        row.append(chest.render())
                    else:
                        shop = next((s for s in self.shops if s.x == x and s.y == y and s.map_id == self.map_id), None)
                        if shop:
                            row.append(shop.render())
                        else:
                            repair = next((r for r in self.repair_yards if r.x == x and r.y == y and r.map_id == self.map_id), None)
                            if repair:
                                row.append(repair.render())
                            else:
                                crush = next((c for c in self.crush_yards if c.x == x and c.y == y and c.map_id == self.map_id), None)
                                if crush:
                                    row.append(crush.render())
                                else:
                                    en = next((e for e in self.enemies if e.x==x and e.y==y and e.map_id == wm.current_map), None)
                                    if en:
                                        row.append(en.render())
                                    else:
                                        itm = next((i for i in self.items if i[0]==x and i[1]==y), None)
                                        if itm:
                                            row.append(itm[2].render())
                                        else:
                                            row.append(color('.', self.floor_color))
            print(''.join(row))

    def get_item_at(self, x, y):
        for i in self.items:
            if i[0] == x and i[1] == y:
                return i
        return None

    def remove_item(self, entry):
        if entry in self.items:
            self.items.remove(entry)

    def get_chest_near(self, x, y):
        for c in self.chests:
            if abs(c.x - x) <= 2 and abs(c.y - y) <= 2:
                return c
        return None

    def get_shop_near(self, x, y):
        for s in self.shops:
            if abs(s.x - x) <= 1 and abs(s.y - y) <= 1 and s.map_id == self.map_id:
                return s
        return None

    def get_repair_yard_near(self, x, y):
        for r in self.repair_yards:
            if abs(r.x - x) <= 1 and abs(r.y - y) <= 1 and r.map_id == self.map_id:
                return r
        return None

    def get_crush_yard_near(self, x, y):
        for c in self.crush_yards:
            if abs(c.x - x) <= 1 and abs(c.y - y) <= 1 and c.map_id == self.map_id:
                return c
        return None

    def get_enemy_at(self, x, y):
        for e in self.enemies:
            if e.x == x and e.y == y and e.map_id == self.map_id:
                return e
        return None

# ===== World Manager =====
class WorldManager:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.maps = {}
        self.map_x = 0
        self.map_y = 0
        self.current_map = (0,0)

    def to_dict(self):
        return {
            'w': self.w,
            'h': self.h,
            'map_x': self.map_x,
            'map_y': self.map_y,
            'current_map': self.current_map,
            'maps': {str(k): v.to_dict() for k, v in self.maps.items()}
        }
    @classmethod
    def from_dict(cls, d):
        wm = cls(d['w'], d['h'])
        wm.map_x = d['map_x']
        wm.map_y = d['map_y']
        wm.current_map = tuple(d['current_map'])
        for sk in d['maps']:
            k_str = sk[1:-1].split(', ')
            k = tuple(int(num) for num in k_str)
            wm.maps[k] = World.from_dict(d['maps'][sk])
        return wm

    def get_world(self, mx, my):
        key = (mx, my)
        if key not in self.maps:
            world = World(self.w, self.h, key)
            dist = max(abs(mx), abs(my))
            item_count = 3 + min(dist, 5)
            biome_data = BIOMES[world.biome]
            tier_chances = {
                "Wood": max(0.5 - dist * 0.05, 0.1),
                "Silver": min(0.3 + dist * 0.03, 0.4),
                "Bronze": min(0.15 + dist * 0.02, 0.3),
                "Gold": min(0.05 + dist * 0.02, 0.2),
                "Diamond": min(0.05 + dist * 0.02, 0.3)
            }
            item_types = [
                ("Sword", Item.TYPE_META["Sword"]),
                ("Long Sword", Item.TYPE_META["Long Sword"]),
                ("Spear", Item.TYPE_META["Spear"]),
                ("Knife", Item.TYPE_META["Knife"]),
                ("Mace", Item.TYPE_META["Mace"]),
                ("Shovel", Item.TYPE_META["Shovel"]),
                ("Bow", Item.TYPE_META["Bow"]),
                ("CrossBow", Item.TYPE_META["CrossBow"]),
                ("Shield", Item.TYPE_META["Shield"]),
                ("Chest Piece", Item.TYPE_META["Chest Piece"]),
                ("Helmet", Item.TYPE_META["Helmet"]),
                ("Pants", Item.TYPE_META["Pants"]),
                ("Boots", Item.TYPE_META["Boots"]),
                ("Potion", Item.TYPE_META["Potion"]),
                ("Bag", Item.TYPE_META["Bag"]),
                ("Cross", Item.TYPE_META["Cross"]),
                ("Stun Ring", Item.TYPE_META["Stun Ring"]),
                ("Arrow Quill", Item.TYPE_META["Arrow Quill"]),
                ("Crystal", Item.TYPE_META["Crystal"]),
                ("Gem", Item.TYPE_META["Gem"]),
                ("Sapphire", Item.TYPE_META["Sapphire"]),
                ("Dagger", Item.TYPE_META["Dagger"]),
            ]
            for _ in range(item_count):
                if random.random() > biome_data["item_chance"]:
                    continue
                tier = random.choices(list(tier_chances.keys()), weights=list(tier_chances.values()), k=1)[0]
                item_type = random.choice(item_types)
                name = f"{tier} {item_type[0]}" if item_type[0] not in ["Arrow Quill", "Crystal", "Gem", "Sapphire"] else item_type[0]
                meta = item_type[1].copy()
                if tier != "Wood" and item_type[0] not in ["Arrow Quill", "Crystal", "Gem", "Sapphire"]:
                    if "damage" in meta:
                        meta["damage"] = int(meta["damage"] * Item.TIERS[tier]["multiplier"])
                    if "durability" in meta:
                        meta["durability"] = int(meta["durability"] * Item.TIERS[tier]["multiplier"])
                    if "uses" in meta:
                        meta["uses"] = int(meta["uses"] * Item.TIERS[tier]["multiplier"])
                    if "arrows" in meta:
                        meta["arrows"] = int(meta["arrows"] * Item.TIERS[tier]["multiplier"])
                    if "empale_chance_base" in meta:
                        meta["empale_chance"] = meta["empale_chance_base"] * Item.TIERS[tier]["multiplier"]
                    if "stun_chance_base" in meta:
                        meta["stun_chance"] = meta["stun_chance_base"] * Item.TIERS[tier]["multiplier"]
                world.add_item(random.randint(0, self.w-1), random.randint(0, self.h-1), Item(name, meta=meta))
            chest_tier = random.choices(list(Chest.TIERS.keys()), weights=list(tier_chances.values()), k=1)[0]
            chest = Chest(random.randint(0, self.w-1), random.randint(0, self.h-1), tier=chest_tier)
            chest.inventory.add(Item("Gold"))
            if random.random() < 0.5:
                chest.inventory.add(Item(f"{chest_tier} Potion", meta={"type": "consumable"}))
            chest.inventory.add(Item(f"{chest_tier} Chest Piece", meta={"type": "armor", "chestpiece": True}))
            if random.random() < 0.5:
                chest.inventory.add(Item("Crystal", meta={"type": "crystal"}))
            if random.random() < 0.5:
                chest.inventory.add(Item("Gem", meta={"type": "gem"}))
            if random.random() < 0.5:
                chest.inventory.add(Item("Sapphire", meta={"type": "sapphire"}))
            if random.random() < 0.5:
                chest.inventory.add(Item(f"{chest_tier} Dagger", meta={"type": "dagger", "damage": 12 * Item.TIERS[chest_tier]["multiplier"], "uses": 5 * Item.TIERS[chest_tier]["multiplier"]}))
            world.add_chest(chest)
            if dist % 5 == 0 and dist > 0:
                shop_tier = random.choices(list(Shop.TIERS.keys()), weights=list(tier_chances.values()), k=1)[0]
                shop = Shop(random.randint(0, self.w-1), random.randint(0, self.h-1), key, tier=shop_tier)
                shop_items = []
                if shop_tier == "Wood":
                    shop_items.extend([
                        (Item(f"Wood Sword", meta=Item.TYPE_META["Sword"]), random.randint(1, 3)),
                        (Item(f"Wood Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(1, 3)),
                        (Item(f"Wood Spear", meta=Item.TYPE_META["Spear"]), random.randint(1, 3)),
                        (Item(f"Wood Knife", meta=Item.TYPE_META["Knife"]), random.randint(1, 3)),
                        (Item(f"Wood Mace", meta=Item.TYPE_META["Mace"]), random.randint(1, 3)),
                        (Item(f"Wood Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(1, 3)),
                        (Item(f"Wood Bow", meta=Item.TYPE_META["Bow"]), random.randint(2, 5)),
                        (Item(f"Wood CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(2, 5)),
                        (Item(f"Wood Shield", meta=Item.TYPE_META["Shield"]), random.randint(2, 4)),
                        (Item(f"Wood Cross", meta=Item.TYPE_META["Cross"]), random.randint(3, 6)),
                        (Item(f"Wood Stun Ring", meta=Item.TYPE_META["Stun Ring"]), random.randint(3, 6)),
                        (Item(f"Wood Helmet", meta=Item.TYPE_META["Helmet"]), random.randint(2, 4)),
                        (Item(f"Wood Pants", meta=Item.TYPE_META["Pants"]), random.randint(2, 4)),
                        (Item(f"Wood Boots", meta=Item.TYPE_META["Boots"]), random.randint(2, 4)),
                        (Item(f"Wood Dagger", meta={"type": "dagger", "damage": 12, "uses": 5}), random.randint(2, 4)),
                    ])
                    if random.random() < 0.3:
                        shop_items.extend([
                            (Item(f"Silver Sword", meta=Item.TYPE_META["Sword"]), random.randint(4, 7)),
                            (Item(f"Silver Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(4, 7)),
                            (Item(f"Silver Spear", meta=Item.TYPE_META["Spear"]), random.randint(4, 7)),
                            (Item(f"Silver Knife", meta=Item.TYPE_META["Knife"]), random.randint(4, 7)),
                            (Item(f"Silver Mace", meta=Item.TYPE_META["Mace"]), random.randint(4, 7)),
                            (Item(f"Silver Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(4, 7)),
                            (Item(f"Silver Bow", meta=Item.TYPE_META["Bow"]), random.randint(5, 8)),
                            (Item(f"Silver CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(5, 8)),
                            (Item(f"Silver Shield", meta=Item.TYPE_META["Shield"]), random.randint(5, 7)),
                            (Item(f"Silver Dagger", meta={"type": "dagger", "damage": 12*1.5, "uses": 5*1.5}), random.randint(5, 7)),
                        ])
                    if random.random() < 0.1:
                        shop_items.extend([
                            (Item(f"Bronze Sword", meta=Item.TYPE_META["Sword"]), random.randint(6, 9)),
                            (Item(f"Bronze Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(6, 9)),
                            (Item(f"Bronze Spear", meta=Item.TYPE_META["Spear"]), random.randint(6, 9)),
                            (Item(f"Bronze Knife", meta=Item.TYPE_META["Knife"]), random.randint(6, 9)),
                            (Item(f"Bronze Mace", meta=Item.TYPE_META["Mace"]), random.randint(6, 9)),
                            (Item(f"Bronze Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(6, 9)),
                            (Item(f"Bronze Bow", meta=Item.TYPE_META["Bow"]), random.randint(7, 10)),
                            (Item(f"Bronze CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(7, 10)),
                            (Item(f"Bronze Shield", meta=Item.TYPE_META["Shield"]), random.randint(6, 9)),
                            (Item(f"Bronze Dagger", meta={"type": "dagger", "damage": 12*2, "uses": 5*2}), random.randint(6, 9)),
                        ])
                elif shop_tier == "Silver":
                    shop_items.extend([
                        (Item(f"Silver Sword", meta=Item.TYPE_META["Sword"]), random.randint(4, 7)),
                        (Item(f"Silver Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(4, 7)),
                        (Item(f"Silver Spear", meta=Item.TYPE_META["Spear"]), random.randint(4, 7)),
                        (Item(f"Silver Knife", meta=Item.TYPE_META["Knife"]), random.randint(4, 7)),
                        (Item(f"Silver Mace", meta=Item.TYPE_META["Mace"]), random.randint(4, 7)),
                        (Item(f"Silver Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(4, 7)),
                        (Item(f"Silver Bow", meta=Item.TYPE_META["Bow"]), random.randint(5, 8)),
                        (Item(f"Silver CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(5, 8)),
                        (Item(f"Silver Shield", meta=Item.TYPE_META["Shield"]), random.randint(5, 7)),
                        (Item(f"Silver Cross", meta=Item.TYPE_META["Cross"]), random.randint(5, 8)),
                        (Item(f"Silver Stun Ring", meta=Item.TYPE_META["Stun Ring"]), random.randint(5, 8)),
                        (Item(f"Silver Helmet", meta=Item.TYPE_META["Helmet"]), random.randint(5, 7)),
                        (Item(f"Silver Pants", meta=Item.TYPE_META["Pants"]), random.randint(5, 7)),
                        (Item(f"Silver Boots", meta=Item.TYPE_META["Boots"]), random.randint(5, 7)),
                        (Item(f"Silver Dagger", meta={"type": "dagger", "damage": 12*1.5, "uses": 5*1.5}), random.randint(5, 7)),
                    ])
                    if random.random() < 0.4:
                        shop_items.extend([
                            (Item(f"Bronze Sword", meta=Item.TYPE_META["Sword"]), random.randint(6, 9)),
                            (Item(f"Bronze Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(6, 9)),
                            (Item(f"Bronze Spear", meta=Item.TYPE_META["Spear"]), random.randint(6, 9)),
                            (Item(f"Bronze Knife", meta=Item.TYPE_META["Knife"]), random.randint(6, 9)),
                            (Item(f"Bronze Mace", meta=Item.TYPE_META["Mace"]), random.randint(6, 9)),
                            (Item(f"Bronze Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(6, 9)),
                            (Item(f"Bronze Bow", meta=Item.TYPE_META["Bow"]), random.randint(7, 10)),
                            (Item(f"Bronze CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(7, 10)),
                            (Item(f"Bronze Shield", meta=Item.TYPE_META["Shield"]), random.randint(6, 9)),
                            (Item(f"Bronze Dagger", meta={"type": "dagger", "damage": 12*2, "uses": 5*2}), random.randint(6, 9)),
                        ])
                    if random.random() < 0.05:
                        shop_items.extend([
                            (Item(f"Gold Sword", meta=Item.TYPE_META["Sword"]), random.randint(8, 10)),
                            (Item(f"Gold Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(8, 10)),
                            (Item(f"Gold Spear", meta=Item.TYPE_META["Spear"]), random.randint(8, 10)),
                            (Item(f"Gold Knife", meta=Item.TYPE_META["Knife"]), random.randint(8, 10)),
                            (Item(f"Gold Mace", meta=Item.TYPE_META["Mace"]), random.randint(8, 10)),
                            (Item(f"Gold Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(8, 10)),
                            (Item(f"Gold Bow", meta=Item.TYPE_META["Bow"]), random.randint(9, 10)),
                            (Item(f"Gold CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(9, 10)),
                            (Item(f"Gold Shield", meta=Item.TYPE_META["Shield"]), random.randint(8, 10)),
                            (Item(f"Gold Dagger", meta={"type": "dagger", "damage": 12*3, "uses": 5*3}), random.randint(8, 10)),
                        ])
                elif shop_tier == "Bronze":
                    shop_items.extend([
                        (Item(f"Bronze Sword", meta=Item.TYPE_META["Sword"]), random.randint(6, 9)),
                        (Item(f"Bronze Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(6, 9)),
                        (Item(f"Bronze Spear", meta=Item.TYPE_META["Spear"]), random.randint(6, 9)),
                        (Item(f"Bronze Knife", meta=Item.TYPE_META["Knife"]), random.randint(6, 9)),
                        (Item(f"Bronze Mace", meta=Item.TYPE_META["Mace"]), random.randint(6, 9)),
                        (Item(f"Bronze Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(6, 9)),
                        (Item(f"Bronze Bow", meta=Item.TYPE_META["Bow"]), random.randint(7, 10)),
                        (Item(f"Bronze CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(7, 10)),
                        (Item(f"Bronze Shield", meta=Item.TYPE_META["Shield"]), random.randint(6, 9)),
                        (Item(f"Bronze Cross", meta=Item.TYPE_META["Cross"]), random.randint(7, 10)),
                        (Item(f"Bronze Stun Ring", meta=Item.TYPE_META["Stun Ring"]), random.randint(7, 10)),
                        (Item(f"Bronze Helmet", meta=Item.TYPE_META["Helmet"]), random.randint(6, 9)),
                        (Item(f"Bronze Pants", meta=Item.TYPE_META["Pants"]), random.randint(6, 9)),
                        (Item(f"Bronze Boots", meta=Item.TYPE_META["Boots"]), random.randint(6, 9)),
                        (Item(f"Bronze Dagger", meta={"type": "dagger", "damage": 12*2, "uses": 5*2}), random.randint(6, 9)),
                    ])
                    if random.random() < 0.3:
                        shop_items.extend([
                            (Item(f"Gold Sword", meta=Item.TYPE_META["Sword"]), random.randint(8, 10)),
                            (Item(f"Gold Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(8, 10)),
                            (Item(f"Gold Spear", meta=Item.TYPE_META["Spear"]), random.randint(8, 10)),
                            (Item(f"Gold Knife", meta=Item.TYPE_META["Knife"]), random.randint(8, 10)),
                            (Item(f"Gold Mace", meta=Item.TYPE_META["Mace"]), random.randint(8, 10)),
                            (Item(f"Gold Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(8, 10)),
                            (Item(f"Gold Bow", meta=Item.TYPE_META["Bow"]), random.randint(9, 10)),
                            (Item(f"Gold CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(9, 10)),
                            (Item(f"Gold Shield", meta=Item.TYPE_META["Shield"]), random.randint(8, 10)),
                            (Item(f"Gold Dagger", meta={"type": "dagger", "damage": 12*3, "uses": 5*3}), random.randint(8, 10)),
                        ])
                    if random.random() < 0.1:
                        shop_items.extend([
                            (Item(f"Diamond Sword", meta=Item.TYPE_META["Sword"]), random.randint(10, 15)),
                            (Item(f"Diamond Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(10, 15)),
                            (Item(f"Diamond Spear", meta=Item.TYPE_META["Spear"]), random.randint(10, 15)),
                            (Item(f"Diamond Knife", meta=Item.TYPE_META["Knife"]), random.randint(10, 15)),
                            (Item(f"Diamond Mace", meta=Item.TYPE_META["Mace"]), random.randint(10, 15)),
                            (Item(f"Diamond Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(10, 15)),
                            (Item(f"Diamond Bow", meta=Item.TYPE_META["Bow"]), random.randint(11, 15)),
                            (Item(f"Diamond CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(11, 15)),
                            (Item(f"Diamond Shield", meta=Item.TYPE_META["Shield"]), random.randint(10, 15)),
                            (Item(f"Diamond Dagger", meta={"type": "dagger", "damage": 12*4, "uses": 5*4}), random.randint(10, 15)),
                        ])
                elif shop_tier == "Gold":
                    shop_items.extend([
                        (Item(f"Gold Sword", meta=Item.TYPE_META["Sword"]), random.randint(8, 10)),
                        (Item(f"Gold Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(8, 10)),
                        (Item(f"Gold Spear", meta=Item.TYPE_META["Spear"]), random.randint(8, 10)),
                        (Item(f"Gold Knife", meta=Item.TYPE_META["Knife"]), random.randint(8, 10)),
                        (Item(f"Gold Mace", meta=Item.TYPE_META["Mace"]), random.randint(8, 10)),
                        (Item(f"Gold Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(8, 10)),
                        (Item(f"Gold Bow", meta=Item.TYPE_META["Bow"]), random.randint(9, 10)),
                        (Item(f"Gold CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(9, 10)),
                        (Item(f"Gold Shield", meta=Item.TYPE_META["Shield"]), random.randint(8, 10)),
                        (Item(f"Gold Cross", meta=Item.TYPE_META["Cross"]), random.randint(8, 10)),
                        (Item(f"Gold Stun Ring", meta=Item.TYPE_META["Stun Ring"]), random.randint(8, 10)),
                        (Item(f"Gold Helmet", meta=Item.TYPE_META["Helmet"]), random.randint(8, 10)),
                        (Item(f"Gold Pants", meta=Item.TYPE_META["Pants"]), random.randint(8, 10)),
                        (Item(f"Gold Boots", meta=Item.TYPE_META["Boots"]), random.randint(8, 10)),
                        (Item(f"Gold Dagger", meta={"type": "dagger", "damage": 12*3, "uses": 5*3}), random.randint(8, 10)),
                    ])
                    if random.random() < 0.3:
                        shop_items.extend([
                            (Item(f"Diamond Sword", meta=Item.TYPE_META["Sword"]), random.randint(10, 15)),
                            (Item(f"Diamond Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(10, 15)),
                            (Item(f"Diamond Spear", meta=Item.TYPE_META["Spear"]), random.randint(10, 15)),
                            (Item(f"Diamond Knife", meta=Item.TYPE_META["Knife"]), random.randint(10, 15)),
                            (Item(f"Diamond Mace", meta=Item.TYPE_META["Mace"]), random.randint(10, 15)),
                            (Item(f"Diamond Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(10, 15)),
                            (Item(f"Diamond Bow", meta=Item.TYPE_META["Bow"]), random.randint(11, 15)),
                            (Item(f"Diamond CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(11, 15)),
                            (Item(f"Diamond Shield", meta=Item.TYPE_META["Shield"]), random.randint(10, 15)),
                            (Item(f"Diamond Dagger", meta={"type": "dagger", "damage": 12*4, "uses": 5*4}), random.randint(10, 15)),
                        ])
                elif shop_tier == "Diamond":
                    shop_items.extend([
                        (Item(f"Diamond Sword", meta=Item.TYPE_META["Sword"]), random.randint(10, 15)),
                        (Item(f"Diamond Long Sword", meta=Item.TYPE_META["Long Sword"]), random.randint(10, 15)),
                        (Item(f"Diamond Spear", meta=Item.TYPE_META["Spear"]), random.randint(10, 15)),
                        (Item(f"Diamond Knife", meta=Item.TYPE_META["Knife"]), random.randint(10, 15)),
                        (Item(f"Diamond Mace", meta=Item.TYPE_META["Mace"]), random.randint(10, 15)),
                        (Item(f"Diamond Shovel", meta=Item.TYPE_META["Shovel"]), random.randint(10, 15)),
                        (Item(f"Diamond Bow", meta=Item.TYPE_META["Bow"]), random.randint(11, 15)),
                        (Item(f"Diamond CrossBow", meta=Item.TYPE_META["CrossBow"]), random.randint(11, 15)),
                        (Item(f"Diamond Shield", meta=Item.TYPE_META["Shield"]), random.randint(10, 15)),
                        (Item(f"Diamond Cross", meta=Item.TYPE_META["Cross"]), random.randint(10, 15)),
                        (Item(f"Diamond Stun Ring", meta=Item.TYPE_META["Stun Ring"]), random.randint(10, 15)),
                        (Item(f"Diamond Helmet", meta=Item.TYPE_META["Helmet"]), random.randint(10, 15)),
                        (Item(f"Diamond Pants", meta=Item.TYPE_META["Pants"]), random.randint(10, 15)),
                        (Item(f"Diamond Boots", meta=Item.TYPE_META["Boots"]), random.randint(10, 15)),
                        (Item(f"Diamond Dagger", meta={"type": "dagger", "damage": 12*4, "uses": 5*4}), random.randint(10, 15)),
                    ])
                shop_items.extend([
                    (Item("Arrow Quill", meta=Item.TYPE_META["Arrow Quill"]), random.randint(1, 2)),
                    (Item("Crystal", meta=Item.TYPE_META["Crystal"]), random.randint(2, 4)),
                    (Item("Gem", meta=Item.TYPE_META["Gem"]), random.randint(2, 4)),
                    (Item("Sapphire", meta=Item.TYPE_META["Sapphire"]), random.randint(2, 4)),
                ])
                for item, price in shop_items:
                    if random.random() < 0.7:
                        shop.add_item(item, price)
                world.add_shop(shop)
            if dist % 3 == 0 and dist > 0:
                yard_tier = random.choices(list(tier_chances.keys()), weights=list(tier_chances.values()), k=1)[0]
                if random.random() < 0.5:
                    repair = RepairYard(random.randint(0, self.w-1), random.randint(0, self.h-1), (mx, my), tier=yard_tier)
                    world.add_repair_yard(repair)
                else:
                    crush = CrushYard(random.randint(0, self.w-1), random.randint(0, self.h-1), (mx, my), tier=yard_tier)
                    world.add_crush_yard(crush)
            enemy_count = 1 + dist
            biome_enemy_defs = {
                "grass": [
                    ("Goblin", {"hp": 10, "damage": 3, "type": "melee", "stun_chance": 0.0}),
                    ("Spider", {"hp": 12, "damage": 4, "type": "melee", "stun_chance": 0.0}),
                    ("Skeleton", {"hp": 8, "damage": 4, "type": "ranged", "stun_chance": 0.0}),
                    ("Wolf", {"hp": 12, "damage": 4, "type": "melee", "stun_chance": 0.0}),
                    ("Bandit", {"hp": 15, "damage": 5, "type": "melee", "stun_chance": 0.1}),
                    ("Slime", {"hp": 10, "damage": 3, "type": "melee", "stun_chance": 0.05}),
                ],
                "stone": [
                    ("Orc", {"hp": 25, "damage": 7, "type": "melee", "stun_chance": 0.1}),
                    ("Troll", {"hp": 20, "damage": 6, "type": "melee", "demon": dist >= 5, "stun_chance": 0.2}),
                    ("Defender", {"hp": 20, "damage": 5, "type": "melee", "shield": True, "stun_chance": 0.0}),
                    ("Golem", {"hp": 25, "damage": 6, "type": "melee", "shield": True, "shield_charges": 3, "stun_chance": 0.0}),
                    ("Miner Ghost", {"hp": 14, "damage": 4, "type": "ranged", "stun_chance": 0.1}),
                    ("Rock Elemental", {"hp": 28, "damage": 7, "type": "melee", "shield": True, "stun_chance": 0.15}),
                ],
                "snow": [
                    ("Wraith", {"hp": 15, "damage": 5, "type": "ranged", "demon": dist >= 4, "stun_chance": 0.05}),
                    ("Phantom", {"hp": 40, "damage": 10, "type": "melee", "demon": dist >= 3, "stun_chance": 0.1}),
                    ("Drake", {"hp": 30, "damage": 8, "type": "ranged", "demon": dist >= 6, "stun_chance": 0.15}),
                    ("Ice Witch", {"hp": 18, "damage": 5, "type": "melee", "stun_chance": 0.3}),
                    ("Yeti", {"hp": 22, "damage": 6, "type": "melee", "stun_chance": 0.2}),
                    ("Frost Giant", {"hp": 35, "damage": 9, "type": "melee", "demon": dist >= 5, "stun_chance": 0.25}),
                    ("Snow Leopard", {"hp": 16, "damage": 5, "type": "melee", "stun_chance": 0.1}),
                ],
                "desert": [
                    ("Skeleton", {"hp": 8, "damage": 4, "type": "ranged", "stun_chance": 0.0}),
                    ("Drake", {"hp": 30, "damage": 8, "type": "ranged", "demon": dist >= 6, "stun_chance": 0.15}),
                    ("Spider", {"hp": 12, "damage": 4, "type": "melee", "stun_chance": 0.0}),
                    ("Dust Devil", {"hp": 15, "damage": 5, "type": "ranged", "arrows": 10, "hit_chance": 0.3, "stun_chance": 0.05}),
                    ("Scorpion", {"hp": 13, "damage": 4, "type": "melee", "stun_chance": 0.2}),
                    ("Mummy", {"hp": 17, "damage": 5, "type": "melee", "stun_chance": 0.15}),
                    ("Sand Serpent", {"hp": 20, "damage": 6, "type": "ranged", "stun_chance": 0.1}),
                    ("Mirage Spirit", {"hp": 14, "damage": 4, "type": "ranged", "hit_chance": 0.6, "stun_chance": 0.05}),
                    ("Desert Raider", {"hp": 18, "damage": 5, "type": "melee", "stun_chance": 0.1}),
                ],
            }
            enemy_defs = biome_enemy_defs.get(world.biome, [])
            weights = [biome_data.get("enemy_weights", {}).get(name, 1.0) for name, props in enemy_defs]
            for _ in range(enemy_count):
                x = random.randint(0, self.w-1)
                y = random.randint(0, self.h-1)
                enemy_def = random.choices(enemy_defs, weights=weights, k=1)[0]
                name, props = enemy_def
                shield_charges = props.get("shield_charges", 5)
                e = Enemy(x, y, name=name, hp=props["hp"] + dist * 3, damage=props["damage"] + dist, spawn_map=(mx, my), enemy_type=props["type"], is_demon=props.get("demon", False), has_shield=props.get("shield", False), arrows=props.get("arrows", 0), stun_chance=props.get("stun_chance", 0.0), hit_chance=props.get("hit_chance", 1.0), shield_charges=shield_charges)
                world.add_enemy(e)
            self.maps[(mx, my)] = world
        return self.maps[key]

    def move_enemy_to_map(self, enemy, new_map):
        new_map = tuple(new_map)
        old = self.maps.get(enemy.map_id)
        if old and enemy in old.enemies:
            old.enemies.remove(enemy)
        enemy.map_id = new_map
        nw = self.get_world(new_map[0], new_map[1])
        nw.enemies.append(enemy)

# ===== Save/Load =====
def save_game(world_name, wm, player):
    os.makedirs('saves', exist_ok=True)
    path = f"saves/{world_name}.json"
    data = {
        'wm': wm.to_dict(),
        'player': player.to_dict()
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_game(world_name):
    path = f"saves/{world_name}.json"
    if not os.path.exists(path):
        return None, None
    with open(path, 'r') as f:
        data = json.load(f)
    wm = WorldManager.from_dict(data['wm'])
    player = Player.from_dict(data['player'])
    return wm, player

# ===== Input =====
def get_key():
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\xe0' or key == b'\x00':
            key2 = msvcrt.getch()
            try:
                return {"H":"w","P":"s","K":"a","M":"d"}.get(key2.decode("utf-8"), None)
            except:
                return None
        try:
            return key.decode("utf-8").lower()
        except:
            return None
    return None

# ===== Combat =====
def render_combat(selected_action, actions, action_symbols, player, enemy, turn, flee_allowed_after):
    os.system("cls" if os.name == "nt" else "clear")
    print(color(f"Battle: You vs {enemy.name}{' (Demon)' if enemy.is_demon else ''}", RED))
    print(f"Your HP: {color(str(player.hp), HEALTH_GREEN)}/{color(str(player.max_hp), HEALTH_GREEN)}   Enemy HP: {color(str(enemy.hp), HEALTH_GREEN)}/{color(str(enemy.max_hp), HEALTH_GREEN)}")
    print(f"Enemy Type: {enemy.enemy_type}{' (Arrows: ' + str(enemy.arrows) + ')' if enemy.enemy_type == 'ranged' else ''}")
    if enemy.has_shield:
        print(f"Enemy Shield Charges: {enemy.shield_charges}")
    print("\nSelect Action (use W/S to navigate, Q to select):")
    for i, action in enumerate(actions):
        pointer = "►" if i == selected_action else "  "
        display_action = f"{action_symbols.get(action, '')} {action}"
        if action == "Flee" and turn < flee_allowed_after:
            print(f"{pointer} {display_action} (Available after {flee_allowed_after} turns)")
        else:
            print(f"{pointer} {display_action}")

def fight(player, enemy, world, wm):
    player.in_battle = True
    enemy.in_combat = True
    turn = 0
    flee_allowed_after = 3
    selected_action = 0
    action_symbols = {
        "Punch": "➲",
        "Attack": "⚔",
        "Throw": "➳",
        "Shoot Bow": "➼",
        "Throw Dagger": "‡",
        "Shield": "⍌",
        "Dodge": "↯",
        "Use Cross": "✝",
        "Use Ring": "∘",
        "Use Potion": "⍥",
        "Flee": "➩",
    }
    actions = ["Punch"]
    if player.weapon and player.weapon.meta.get("type") == "weapon":
        actions.append("Attack")
        if player.weapon.meta.get("weapon_type") == "Spear":
            actions.append("Throw")
    if player.bow and player.bow.meta.get("type") == "bow" and player.quiver and player.quiver.meta.get("arrows", 0) > 0:
        actions.append("Shoot Bow")
    if player.dagger and player.dagger.meta.get("uses", 0) > 0:
        actions.append("Throw Dagger")
    actions.append("Shield")
    actions.append("Dodge")
    if enemy.is_demon and player.cross and player.cross.meta.get("uses", 0) > 0:
        actions.append("Use Cross")
    if player.ring and player.ring.meta.get("uses", 0) > 0:
        actions.append("Use Ring")
    actions.extend(["Use Potion", "Flee"])

    while player.hp > 0 and enemy.hp > 0:
        turn += 1
        shield_raised = False
        dodge_attempt = False
        if player.stun_duration > 0:
            print(color("\nYou are stunned and skip your turn!", DAMAGE_RED))
            player.stun_duration -= 1
            time.sleep(0.6)
        else:
            render_combat(selected_action, actions, action_symbols, player, enemy, turn, flee_allowed_after)
            action = None
            while not action:
                k = get_key()
                if not k:
                    time.sleep(0.05)
                    continue
                if k == 'w':
                    selected_action = max(0, selected_action - 1)
                    render_combat(selected_action, actions, action_symbols, player, enemy, turn, flee_allowed_after)
                elif k == 's':
                    selected_action = min(len(actions) - 1, selected_action + 1)
                    render_combat(selected_action, actions, action_symbols, player, enemy, turn, flee_allowed_after)
                elif k == 'q':
                    action = actions[selected_action]

            thrown_weapon = None
            if action in ["Punch", "Attack", "Shoot Bow", "Throw Dagger", "Throw"]:
                if action == "Throw":
                    action = "Throw Spear"
                dmg, post = player.compute_outgoing_damage(action)
                empaled = False
                stunned = False
                stun_duration = 0
                broke_shield = False
                if action in ["Attack", "Throw Spear"] and player.weapon:
                    weapon_type = player.weapon.meta.get("weapon_type")
                    tier = player.weapon.meta.get("tier")
                    empale_bonus = 0.005 * player.skills["Polearm"] if weapon_type == "Spear" else 0
                    skill_map = {"Knife": "Short Blade", "Mace": "Blunt Weapon"}
                    skill_name = skill_map.get(weapon_type)
                    stun_bonus = 0.005 * player.skills[skill_name] if skill_name and skill_name in player.skills else 0
                    if weapon_type == "Spear" and random.random() < player.weapon.meta.get("empale_chance", 0) + empale_bonus:
                        dmg = enemy.hp
                        empaled = True
                    elif weapon_type == "Knife" and random.random() < player.weapon.meta.get("stun_chance", 0) + stun_bonus:
                        stunned = True
                        stun_duration = 1
                    elif weapon_type == "Mace" and random.random() < Item.TIERS[tier]["stun_chance"] + stun_bonus:
                        stunned = True
                        if tier == "Wood":
                            stun_duration = 1
                        elif tier in ["Silver", "Bronze"]:
                            stun_duration = 2
                        elif tier in ["Gold", "Diamond"]:
                            stun_duration = 3
                    elif weapon_type == "Shovel" and enemy.has_shield:
                        enemy.has_shield = False
                        enemy.shield_charges = 0
                        broke_shield = True
                actual, blocked, broken_item = enemy.take_damage(dmg, player)
                if actual > 0 and empaled:
                    print(color(f"\nYou empaled {enemy.name} for instant kill!", CYAN))
                else:
                    print(color(f"\nYou {action_symbols.get(action, '')} {action.lower()} for {color(str(dmg), DAMAGE_RED)} dmg -> {color(str(actual), DAMAGE_RED)} effective{' (missed)' if blocked else ''}.", CYAN))
                if actual > 0:
                    play_sound("damage_enemy")
                    if stunned:
                        enemy.stun_duration = stun_duration
                        print(color(f"\n{enemy.name} is stunned for {stun_duration} turns!", CYAN))
                    if broke_shield:
                        print(color(f"\nYou broke {enemy.name}'s shield!", CYAN))
                else:
                    play_sound("combat")
                if broken_item:
                    world.add_item(player.x, player.y, broken_item)
                if post:
                    res = post()
                    if res:
                        if isinstance(res, tuple):
                            if "bow_broken" in res[0] or "weapon_broken" in res[0]:
                                old = res[1]
                                broken = res[-1]
                                world.add_item(player.x, player.y, broken)
                            if "dagger_depleted" in res[0]:
                                pass
                if action == "Throw Spear" and player.weapon:
                    thrown_weapon = player.weapon
                    player.weapon = None
                time.sleep(0.6)
            elif action == "Shield":
                if player.shield and player.shield.meta.get("durability", 0) > 0:
                    print(color(f"\nYou raise your {action_symbols.get('Shield')} shield!", CYAN))
                    shield_raised = True
                    time.sleep(0.6)
                else:
                    print(color("\nNo shield or shield has no durability!", YELLOW))
                    time.sleep(0.6)
                    continue
            elif action == "Dodge":
                print(color(f"\nYou prepare to {action_symbols.get('Dodge')} dodge!", CYAN))
                dodge_attempt = True
                time.sleep(0.6)
            elif action == "Use Cross":
                actual, blocked, broken_item = enemy.take_damage(0, player, use_cross=True)
                if broken_item:
                    world.add_item(player.x, player.y, broken_item)
                play_sound("cross")
                time.sleep(0.6)
            elif action == "Use Ring":
                if player.ring and player.ring.meta.get("uses", 0) > 0:
                    enemy.stun_duration = 1
                    print(color(f"\nYou used {player.ring.name}, stunning {enemy.name}!", CYAN))
                    player.ring.meta["uses"] -= 1
                    if player.ring.meta["uses"] <= 0:
                        broken_name = f"Broken {player.ring.name}"
                        broken = Item(broken_name, char=Item.SYMBOLS.get(broken_name, "*"), color=GRAY, meta={"tier": player.ring.meta["tier"]})
                        player.ring = None
                        world.add_item(player.x, player.y, broken)
                        player.items_broken += 1
                        play_sound("break")
                    time.sleep(0.6)
                else:
                    print(color("\nNo ring or no uses left!", YELLOW))
                    time.sleep(0.6)
                    continue
            elif action == "Use Potion":
                pot_index = next((i for i, it in enumerate(player.inventory.items) if "Potion" in it.name), None)
                if pot_index is not None:
                    player.inventory.items.pop(pot_index)
                    player.hp = min(player.max_hp, player.hp + 10)
                    print(color(f"\nYou used a {action_symbols.get('Use Potion')} potion and healed 10 hp.", CYAN))
                    play_sound("use_item")
                    time.sleep(0.6)
                else:
                    print(color("\nNo potion!", YELLOW))
                    time.sleep(0.6)
                    continue
            elif action == "Flee":
                if turn < flee_allowed_after:
                    print(color("\nYou cannot flee yet!", YELLOW))
                    time.sleep(0.8)
                    continue
                else:
                    if random.random() < 0.7 or (enemy.enemy_type == "ranged" and enemy.arrows <= 0):
                        player.inventory.items = []
                        if player.weapon:
                            player.weapon = None
                        if player.bow:
                            player.bow = None
                        if player.armor:
                            player.armor = None
                        if player.helmet:
                            player.helmet = None
                        if player.pants:
                            player.pants = None
                        if player.boots:
                            player.boots = None
                        if player.shield:
                            player.shield = None
                        if player.quiver:
                            player.quiver = None
                        if player.bag:
                            player.bag = None
                        if player.cross:
                            player.cross = None
                        if player.ring:
                            player.ring = None
                        if player.dagger:
                            player.dagger = None
                        print(color(f"\nYou {action_symbols.get('Flee')} fled! You lost all your items but kept your upgrades.", CYAN))
                        play_sound("flee")
                        time.sleep(1)
                        player.in_battle = False
                        enemy.in_combat = False
                        return "player_flee"
                    else:
                        print(color("\nFlee failed!", YELLOW))
                        time.sleep(0.6)

        if enemy.hp <= 0:
            break

        if enemy.stun_duration > 0:
            print(color(f"\n{enemy.name} is stunned and skips their turn!", CYAN))
            enemy.stun_duration -= 1
            time.sleep(0.6)
        else:
            print(color(f"\n{enemy.name} attacks!", DAMAGE_RED))
            time.sleep(0.4)
            actual, blocked, shield_broken_item, stunned, armor_broken_items, dodged = player.take_damage(enemy.damage, shield_raised, dodge_attempt)
            if stunned:
                enemy.stun_duration = 1
                print(color(f"Your {action_symbols.get('Shield')} shield stuns the {enemy.name}!", CYAN))
            if dodged:
                print(color(f"You dodged the attack!", CYAN))
            elif blocked or shield_raised:
                print(color("Your shield blocked the attack!", CYAN))
                if shield_broken_item:
                    world.add_item(player.x, player.y, shield_broken_item)
            else:
                print(color(f"You take {color(str(actual), DAMAGE_RED)} damage.", CYAN))
                if actual > 0:
                    play_sound("damage_player")
                    effective_stun = max(0, enemy.stun_chance - player.stun_resist)
                    if random.random() < effective_stun:
                        player.stun_duration = 1
                        print(color(f"You are stunned by {enemy.name}!", DAMAGE_RED))
            for broken in armor_broken_items:
                world.add_item(player.x, player.y, broken)
            play_sound("combat")
            time.sleep(0.6)

        if thrown_weapon:
            player.equip(thrown_weapon)
            print(color("\nYour spear returns!", CYAN))
            time.sleep(0.3)

    player.in_battle = False
    enemy.in_combat = False
    if player.hp <= 0:
        player.dead = True
        print(color("You died...", DAMAGE_RED))
        play_sound("death")
        time.sleep(1.0)
        return "player_dead"
    elif enemy.hp <= 0:
        print(color(f"You defeated the {enemy.name}!", GREEN))
        play_sound("victory")
        drop_amount = 2 + random.randint(0, 2) if not enemy.is_demon else 3 + random.randint(0, 3)
        for _ in range(drop_amount):
            world.add_item(player.x, player.y, Item("Gold"))
        if random.random() < 0.3:
            world.add_item(player.x, player.y, Item("Crystal", meta={"type": "crystal"}))
        if random.random() < 0.3:
            world.add_item(player.x, player.y, Item("Gem", meta={"type": "gem"}))
        if random.random() < 0.3:
            world.add_item(player.x, player.y, Item("Sapphire", meta={"type": "sapphire"}))
        player.hp = max(1, player.hp)
        player.skill_points += 1
        time.sleep(1.0)
        return "player_win"
    return "unknown"

# ===== Shop Interface =====
def render_shop(selected, player, shop):
    os.system("cls" if os.name == "nt" else "clear")
    print(color(f"== {shop.tier} Shop at {shop.map_id} ({len(shop.inventory.items)} items) ==", shop.color))
    print(color(f"Your Gold: {player.gold}", BLUE))
    if not shop.inventory.items:
        print("  (empty)")
    else:
        displays = shop.inventory.get_display_items()
        for i, display in enumerate(displays):
            pointer = "►" if i == selected else "  "
            price = shop.prices.get(id(shop.inventory.items[i]), 10)
            print(f"{pointer} {display} - {price} Gold")
    selected_item = shop.inventory.get_selected_item()
    if selected_item:
        print("\nItem Details:")
        print(selected_item.get_details())
    print("\nW/S to select, T to buy and drop, Y to buy to inventory, E to exit")

def shop_interface(player, shop, world):
    selected = 0
    render_shop(selected, player, shop)
    while True:
        k = get_key()
        if not k:
            time.sleep(0.05)
            continue
        if k == 'w':
            selected = max(0, selected - 1)
            play_sound("scroll")
            render_shop(selected, player, shop)
        elif k == 's':
            selected = min(len(shop.inventory.items) - 1, selected + 1) if shop.inventory.items else 0
            play_sound("scroll")
            render_shop(selected, player, shop)
        elif k == 't':
            success, msg = shop.buy_item(player, selected, to_inventory=False)
            if success and isinstance(msg, Item):
                world.add_item(player.x, player.y, msg)
                print(color(f"\nBought and dropped {msg.name}!", CYAN))
            else:
                print(color(f"\n{msg}", YELLOW))
            time.sleep(0.6)
            render_shop(selected, player, shop)
        elif k == 'y':
            success, msg = shop.buy_item(player, selected, to_inventory=True)
            print(color(f"\n{msg}", CYAN if success else YELLOW))
            time.sleep(0.6)
            render_shop(selected, player, shop)
        elif k == 'e':
            break

# ===== Repair Interface =====
def calc_repair_cost(item):
    parts = item.name.split()
    if parts[0] != "Broken":
        return 0
    tier = parts[1]
    rarity = Item.TIERS.get(tier, {"rarity": 0})["rarity"]
    return (rarity + 1) * 5

def repair_item(item):
    parts = item.name.split()
    if parts[0] != "Broken":
        return None
    tier = parts[1]
    itype = ' '.join(parts[2:])
    if itype == "Dagger":
        return None
    original_name = f"{tier} {itype}"
    meta_base = Item.TYPE_META.get(itype, {})
    meta = meta_base.copy()
    mult = Item.TIERS[tier]["multiplier"]
    if "damage" in meta:
        meta["damage"] = int(meta["damage"] * mult)
    if "durability" in meta:
        meta["durability"] = int(meta["durability"] * mult)
    if "uses" in meta:
        meta["uses"] = int(meta["uses"] * mult)
    if "arrows" in meta:
        meta["arrows"] = int(meta["arrows"] * mult)
    if "empale_chance_base" in meta:
        meta["empale_chance"] = meta["empale_chance_base"] * mult
    if "stun_chance_base" in meta:
        meta["stun_chance"] = meta["stun_chance_base"] * mult
    return Item(original_name, char=Item.SYMBOLS.get(original_name, "*"), color=Item.TIERS[tier]["color"], meta=meta)

def render_repair(selected, player, yard):
    os.system("cls" if os.name == "nt" else "clear")
    print(color(f"== {yard.tier} Repair Yard at {yard.map_id} ==", yard.color))
    print(color(f"Your Gold: {player.gold}", BLUE))
    broken_items = [it for it in player.inventory.items if "Broken" in it.name and "Dagger" not in it.name]
    if not broken_items:
        print("  (no broken items)")
    else:
        for i, it in enumerate(broken_items):
            pointer = "►" if i == selected else "  "
            cost = calc_repair_cost(it)
            print(f"{pointer} {it.char} {it.get_display_name()} - Repair Cost: {cost} Gold")
    if broken_items and selected < len(broken_items):
        print("\nItem Details:")
        print(broken_items[selected].get_details())
    print("\nW/S to select, Q to repair, E to exit")

def repair_interface(player, yard, world):
    selected = 0
    render_repair(selected, player, yard)
    while True:
        k = get_key()
        if not k:
            time.sleep(0.05)
            continue
        broken_items = [it for it in player.inventory.items if "Broken" in it.name and "Dagger" not in it.name]
        if k == 'w':
            selected = max(0, selected - 1)
            play_sound("scroll")
            render_repair(selected, player, yard)
        elif k == 's':
            selected = min(len(broken_items) - 1, selected + 1) if broken_items else 0
            play_sound("scroll")
            render_repair(selected, player, yard)
        elif k == 'q':
            if broken_items and selected < len(broken_items):
                item = broken_items[selected]
                cost = calc_repair_cost(item)
                if player.gold >= cost:
                    player.gold -= cost
                    player.inventory.items.remove(item)
                    repaired = repair_item(item)
                    if repaired:
                        if not player.inventory.add(repaired):
                            world.add_item(player.x, player.y, repaired)
                        print(color(f"\nRepaired {repaired.name}!", CYAN))
                        player.items_repaired += 1
                    else:
                        print(color("\nRepair failed!", YELLOW))
                else:
                    print(color("\nNot enough gold!", YELLOW))
                time.sleep(0.6)
                render_repair(selected, player, yard)
        elif k == 'e':
            break

# ===== Crush Interface =====
def calc_crush_rewards(item):
    tier = item.meta.get("tier", "Wood")
    rarity = Item.TIERS.get(tier, {"rarity": 0})["rarity"]
    rewards = []
    gold_num = (rarity + 1) * 2
    rewards.append(("Gold", gold_num))
    if random.random() < 0.3 * (rarity + 1):
        rewards.append(("Crystal", 1))
    if random.random() < 0.2 * (rarity + 1):
        rewards.append(("Gem", 1))
    if random.random() < 0.1 * (rarity + 1):
        rewards.append(("Sapphire", 1))
    return rewards

def render_crush(selected, player, yard, item_rewards):
    os.system("cls" if os.name == "nt" else "clear")
    print(color(f"== {yard.tier} Crush Yard at {yard.map_id} ==", yard.color))
    print(color(f"Your Gold: {player.gold}", BLUE))
    items = player.inventory.items
    if not items:
        print("  (empty)")
    else:
        for i, it in enumerate(items):
            pointer = "►" if i == selected else "  "
            rewards = item_rewards.get(id(it), [])
            reward_str = ', '.join([f"{num} {name}" for name, num in rewards])
            print(f"{pointer} {it.char} {it.get_display_name()} - Rewards: {reward_str}")
    if items and selected < len(items):
        print("\nItem Details:")
        print(items[selected].get_details())
    print("\nW/S to select, Q to crush, E to exit")

def crush_interface(player, yard, world):
    item_rewards = {}
    for it in player.inventory.items:
        item_rewards[id(it)] = calc_crush_rewards(it)
    selected = 0
    render_crush(selected, player, yard, item_rewards)
    while True:
        k = get_key()
        if not k:
            time.sleep(0.05)
            continue
        items = player.inventory.items
        if k == 'w':
            selected = max(0, selected - 1)
            play_sound("scroll")
            render_crush(selected, player, yard, item_rewards)
        elif k == 's':
            selected = min(len(items) - 1, selected + 1) if items else 0
            play_sound("scroll")
            render_crush(selected, player, yard, item_rewards)
        elif k == 'q':
            if items and selected < len(items):
                item = items[selected]
                if player.is_equipped(item):
                    print(color("\nCannot crush equipped item!", YELLOW))
                    time.sleep(0.6)
                    continue
                rewards = item_rewards[id(item)]
                player.inventory.items.remove(item)
                del item_rewards[id(item)]
                for rname, num in rewards:
                    for _ in range(num):
                        ritem = Item(rname, meta=Item.TYPE_META.get(rname, {}))
                        if not player.inventory.add(ritem):
                            world.add_item(player.x + random.randint(-1,1), player.y + random.randint(-1,1), ritem)
                        else:
                            item_rewards[id(ritem)] = calc_crush_rewards(ritem)
                print(color(f"\nCrushed {item.name}! Received rewards.", CYAN))
                time.sleep(0.6)
                selected = max(0, min(selected, len(player.inventory.items) - 1))
                render_crush(selected, player, yard, item_rewards)
        elif k == 'e':
            break

# ===== Skill Tree Interface =====
SKILL_DESCRIPTIONS = {
    "Blunt Weapon": "Increases damage and stun chance for maces and shovels. Decreases enemy hit chance.",
    "Short Blade": "Increases damage and stun chance for knives and daggers. Decreases enemy hit chance.",
    "Long Blade": "Increases damage for swords and long swords. Decreases enemy hit chance.",
    "Polearm": "Increases damage and empale chance for spears. Decreases enemy hit chance.",
    "Archery": "Increases damage for bows and crossbows. Decreases enemy hit chance.",
    "Agility": "Increases dodge chance overall and when dodging.",
    "Endurance": "Increases buffs to armor and player defense.",
    "Strength": "Increases damage multiplier for all attacks.",
}

def render_skill_tree(selected, player):
    os.system("cls" if os.name == "nt" else "clear")
    print(color("== Skill Tree ==", GREEN))
    print(color(f"Available Points: {player.skill_points}", BLUE))
    skill_list = list(player.skills.keys())
    for i, skill in enumerate(skill_list):
        pointer = "►" if i == selected else "  "
        level = player.skills[skill]
        print(f"{pointer} {skill}: {level}/99")
    if skill_list:
        selected_skill = skill_list[selected]
        print("\nDescription:")
        print(SKILL_DESCRIPTIONS.get(selected_skill, "No description available."))
    print("\nW/S to select, Q to upgrade (if points available), E to exit")

def skill_tree_interface(player):
    selected = 0
    render_skill_tree(selected, player)
    skill_list = list(player.skills.keys())
    while True:
        k = get_key()
        if not k:
            time.sleep(0.05)
            continue
        if k == 'w':
            selected = max(0, selected - 1)
            play_sound("scroll")
            render_skill_tree(selected, player)
        elif k == 's':
            selected = min(len(skill_list) - 1, selected + 1)
            play_sound("scroll")
            render_skill_tree(selected, player)
        elif k == 'q':
            if player.skill_points > 0:
                selected_skill = skill_list[selected]
                player.upgrade_skill(selected_skill)
                print(color(f"\nUpgraded {selected_skill} to {player.skills[selected_skill]}!", CYAN))
                time.sleep(0.6)
                render_skill_tree(selected, player)
            else:
                print(color("\nNo skill points available!", YELLOW))
                time.sleep(0.6)
        elif k == 'e':
            break

# ===== Game Loop =====
def game_loop(wm, player, world_name):
    global dirty
    dirty = True
    map_x = wm.map_x
    map_y = wm.map_y
    world = wm.get_world(map_x, map_y)
    in_inventory = False
    in_shop = False
    in_repair = False
    in_crush = False
    in_skill_tree = False
    current_inventory = player.inventory
    if player.dead:
        print(color("You died last time. Respawning...", YELLOW))
        time.sleep(1)
        chest = Chest(player.x, player.y, tier="Wood")
        equipped_slots = ['weapon', 'bow', 'armor', 'helmet', 'pants', 'boots', 'shield', 'quiver', 'bag', 'cross', 'ring', 'dagger']
        for slot in equipped_slots:
            eq = getattr(player, slot)
            if eq:
                player.unequip(eq)
                chest.inventory.add(eq)
        for it in list(player.inventory.items):
            chest.inventory.add(it)
            player.inventory.items.remove(it)
        world.add_chest(chest)
        player.reset_on_respawn()
        map_x = 0
        map_y = 0
        world = wm.get_world(0, 0)
        player.x = wm.w // 2
        player.y = wm.h // 2
        dirty = True
    while True:
        wm.map_x, wm.map_y = map_x, map_y
        wm.current_map = (map_x, map_y)
        for e in list(world.enemies):
            e.tick_move(world, player, wm)
            if e.map_id == wm.current_map and e.x == player.x and e.y == player.y:
                res = fight(player, e, world, wm)
                if res == "player_win":
                    if e in world.enemies:
                        world.enemies.remove(e)
                    player.monsters_killed += 1
                    dirty = True
                elif res == "player_dead":
                    os.system("cls" if os.name == "nt" else "clear")
                    print(color("You died...", DAMAGE_RED))
                    options = ["Respawn", "Menu"]
                    selected = 0
                    while True:
                        render_menu(options, selected, "Death Menu", "\nW/S to navigate, Q to select")
                        k = get_key()
                        if not k:
                            time.sleep(0.05)
                            continue
                        if k == 'w':
                            selected = max(0, selected - 1)
                        elif k == 's':
                            selected = min(1, selected + 1)
                        elif k == 'q':
                            if selected == 0:
                                # Respawn
                                chest = Chest(player.x, player.y, tier="Wood")
                                equipped_slots = ['weapon', 'bow', 'armor', 'helmet', 'pants', 'boots', 'shield', 'quiver', 'bag', 'cross', 'ring', 'dagger']
                                for slot in equipped_slots:
                                    eq = getattr(player, slot)
                                    if eq:
                                        player.unequip(eq)
                                        chest.inventory.add(eq)
                                for it in list(player.inventory.items):
                                    chest.inventory.add(it)
                                    player.inventory.items.remove(it)
                                world.add_chest(chest)
                                player.reset_on_respawn()
                                map_x = 0
                                map_y = 0
                                world = wm.get_world(0, 0)
                                player.x = wm.w // 2
                                player.y = wm.h // 2
                                dirty = True
                                break
                            elif selected == 1:
                                save_game(world_name, wm, player)
                                return
                elif res == "player_flee":
                    player.times_fled += 1
                    dirs = [(-1, 0, wm.w-1, player.y), (1, 0, 0, player.y), (0, -1, player.x, wm.h-1), (0, 1, player.x, 0)]
                    dx, dy, nx, ny = random.choice(dirs)
                    map_x += dx
                    map_y += dy
                    world = wm.get_world(map_x, map_y)
                    player.x = nx
                    player.y = ny
                    dirty = True
                elif res == "enemy_flee":
                    dirty = True

        if not in_inventory and not in_shop and not in_repair and not in_crush and not in_skill_tree:
            if dirty:
                world.render(player, wm)
                print("\nPlayer Status:")
                print(color(f"HP: {color(str(player.hp), HEALTH_GREEN)}/{color(str(player.max_hp), HEALTH_GREEN)}", BLUE))
                print(color(f"Gold: {player.gold}", BLUE))
                print(color(f"Weapon: {player.weapon.get_display_name() if player.weapon else 'None'}", BLUE))
                print(color(f"Bow: {player.bow.get_display_name() if player.bow else 'None'}", BLUE))
                print(color(f"Shield: {player.shield.get_display_name() if player.shield else 'None'} (Durability: {player.shield.meta.get('durability', 0) if player.shield else 0})", BLUE))
                print(color(f"Helmet: {player.helmet.get_display_name() if player.helmet else 'None'} (Durability: {player.helmet.meta.get('durability', 0) if player.helmet else 0})", BLUE))
                print(color(f"Armor: {player.armor.get_display_name() if player.armor else 'None'} (Durability: {player.armor.meta.get('durability', 0) if player.armor else 0})", BLUE))
                print(color(f"Pants: {player.pants.get_display_name() if player.pants else 'None'} (Durability: {player.pants.meta.get('durability', 0) if player.pants else 0})", BLUE))
                print(color(f"Boots: {player.boots.get_display_name() if player.boots else 'None'} (Durability: {player.boots.meta.get('durability', 0) if player.boots else 0})", BLUE))
                print(color(f"Quiver: {player.quiver.get_display_name() if player.quiver else 'None'} (Arrows: {player.quiver.meta.get('arrows', 0) if player.quiver else 0})", BLUE))
                print(color(f"Bag: {player.bag.get_display_name() if player.bag else 'None'} (Inventory Size: {player.inventory.max_size})", BLUE))
                print(color(f"Cross: {player.cross.get_display_name() if player.cross else 'None'} (Uses: {player.cross.meta.get('uses', 0) if player.cross else 0})", BLUE))
                print(color(f"Ring: {player.ring.get_display_name() if player.ring else 'None'} (Uses: {player.ring.meta.get('uses', 0) if player.ring else 0})", BLUE))
                print(color(f"Dagger: {player.dagger.get_display_name() if player.dagger else 'None'} (Uses: {player.dagger.meta.get('uses', 0) if player.dagger else 0})", BLUE))
                print(color(f"Damage Multiplier: {player.base_damage_mult:.2f}x", BLUE))
                print(color(f"Person Defense: {int(player.person_defense * 100)}%", BLUE))
                print(color(f"Stun Resist: {int(player.stun_resist * 100)}%", BLUE))
                print(color(f"Dodge Chance: {int(player.dodge_chance * 100)}%", BLUE))
                print("\nUse WASD to move, E for inventory, Y for chest transfer, T for skill tree, E near shop/repair/crush to interact.")
                print("Stand on item to pick up. Move past edges to new map. Z to save, M to menu.")
                dirty = False
        elif in_inventory:
            if dirty:
                title = f"{current_inventory.owner.tier} Chest" if current_inventory is not player.inventory else "Player Inventory"
                current_inventory.render_ui(title)
                print("\nW/S to select, T to drop, Y to transfer (if near chest), R to toggle collapse, F to equip/unequip, Q to use item, E to exit.")
                dirty = False
        elif in_shop:
            shop_interface(player, current_inventory, world)
            in_shop = False
            dirty = True
        elif in_repair:
            repair_interface(player, current_inventory, world)
            in_repair = False
            dirty = True
        elif in_crush:
            crush_interface(player, current_inventory, world)
            in_crush = False
            dirty = True
        elif in_skill_tree:
            skill_tree_interface(player)
            in_skill_tree = False
            dirty = True

        key = get_key()
        if not key:
            time.sleep(0.08)
            continue

        if not in_inventory and not in_shop and not in_repair and not in_crush and not in_skill_tree:
            old_x, old_y = player.x, player.y
            if key == 'w': player.y -= 1
            if key == 's': player.y += 1
            if key == 'a': player.x -= 1
            if key == 'd': player.x += 1

            if (player.x != old_x or player.y != old_y):
                play_sound("move")
                dirty = True

            old_map_x, old_map_y = map_x, map_y
            if player.x < 0:
                map_x -= 1
                world = wm.get_world(map_x, map_y)
                player.x = wm.w-1
                if (map_x, map_y) != (old_map_x, old_map_y):
                    play_sound("travel")
                    dirty = True
            if player.x >= wm.w:
                map_x += 1
                world = wm.get_world(map_x, map_y)
                player.x = 0
                if (map_x, map_y) != (old_map_x, old_map_y):
                    play_sound("travel")
                    dirty = True
            if player.y < 0:
                map_y -= 1
                world = wm.get_world(map_x, map_y)
                player.y = wm.h-1
                if (map_x, map_y) != (old_map_x, old_map_y):
                    play_sound("travel")
                    dirty = True
            if player.y >= wm.h:
                map_y += 1
                world = wm.get_world(map_x, map_y)
                player.y = 0
                if (map_x, map_y) != (old_map_x, old_map_y):
                    play_sound("travel")
                    dirty = True

            itm = world.get_item_at(player.x, player.y)
            if itm:
                if itm[2].name == "Gold":
                    player.gold += 1
                    player.coins_earned += 1
                    world.remove_item(itm)
                    play_sound("pickup")
                    dirty = True
                elif player.inventory.add(itm[2]):
                    world.remove_item(itm)
                    play_sound("pickup")
                    dirty = True

            if key == 'e':
                near_shop = world.get_shop_near(player.x, player.y)
                near_repair = world.get_repair_yard_near(player.x, player.y)
                near_crush = world.get_crush_yard_near(player.x, player.y)
                if near_shop:
                    in_shop = True
                    current_inventory = near_shop
                    play_sound("open")
                elif near_repair:
                    in_repair = True
                    current_inventory = near_repair
                    play_sound("open")
                elif near_crush:
                    in_crush = True
                    current_inventory = near_crush
                    play_sound("open")
                else:
                    in_inventory = True
                    current_inventory = player.inventory
                    play_sound("open_inventory")
                    dirty = True
            elif key == 'y':
                near_chest = world.get_chest_near(player.x, player.y)
                if near_chest:
                    if not near_chest.opened and near_chest.is_mimic:
                        mimic_rarity = Chest.TIERS[near_chest.tier]["rarity"]
                        mimic = Enemy(near_chest.x, near_chest.y, name="Mimic", hp=20 * (1 + mimic_rarity), damage=5 * (1 + mimic_rarity), enemy_type="melee", has_shield=(mimic_rarity >= 3))
                        res = fight(player, mimic, world, wm)
                        if res == "player_win":
                            near_chest.is_mimic = False
                            near_chest.opened = True
                            in_inventory = True
                            current_inventory = near_chest.inventory
                            play_sound("open_chest")
                            dirty = True
                        elif res == "player_dead":
                            os.system("cls" if os.name == "nt" else "clear")
                            print(color("Game Stats:", YELLOW))
                            print(f"Coins Earned: {player.coins_earned}")
                            print(f"Coins Spent: {player.coins_spent}")
                            print(f"Sapphires Used: {player.sapphires_used}")
                            print(f"Gems Used: {player.gems_used}")
                            print(f"Crystals Used: {player.crystals_used}")
                            print(f"Items Broken: {player.items_broken}")
                            print(f"Items Repaired: {player.items_repaired}")
                            print(f"Monsters Killed: {player.monsters_killed}")
                            print(f"Times Fled: {player.times_fled}")
                            input("Press enter to continue...")
                            return
                        else:
                            continue
                    else:
                        near_chest.opened = True
                        in_inventory = True
                        current_inventory = near_chest.inventory
                        play_sound("open_chest")
                        dirty = True
            elif key == 't':
                in_skill_tree = True
                play_sound("open")
                dirty = True
            elif key == 'z':
                save_game(world_name, wm, player)
                print(color("Game saved!", GREEN))
                time.sleep(0.5)
                dirty = True
            elif key == 'm':
                save_game(world_name, wm, player)
                print(color("Returning to menu...", GREEN))
                time.sleep(0.5)
                return

        elif in_inventory:
            inv = current_inventory
            if key == 'e':
                in_inventory = False
                dirty = True
            elif key == 't':
                def drop_cb(item):
                    dx, dy = random.randint(-1,1), random.randint(-1,1)
                    world.add_item(player.x+dx, player.y+dy, item)
                if inv.drop_selected_one(drop_cb):
                    dirty = True
            elif key == 'y':
                near_chest = world.get_chest_near(player.x, player.y)
                if near_chest:
                    target = near_chest.inventory if inv is player.inventory else player.inventory
                    if inv.transfer_selected(target):
                        print(color("\nItem transferred!", CYAN))
                    else:
                        print(color("\nTransfer failed (inventory full or item equipped)!", YELLOW))
                    time.sleep(0.6)
                    dirty = True
            elif key == 'w':
                play_sound("scroll")
                if inv.collapsed:
                    inv.selected = max(0, inv.selected-1)
                else:
                    inv.selected = max(0, inv.selected-1)
                dirty = True
            elif key == 's':
                play_sound("scroll")
                if inv.collapsed:
                    inv.selected = min(len(inv.get_display_groups())-1, inv.selected+1) if inv.get_display_groups() else 0
                else:
                    inv.selected = min(len(inv.items)-1, inv.selected+1) if inv.items else 0
                dirty = True
            elif key == 'r':
                inv.toggle_collapse()
                inv.selected = 0
                dirty = True
            elif key == 'f':
                inv.equip_toggle_selected()
                time.sleep(0.2)
                dirty = True
            elif key == 'q':
                inv.use_selected()
                time.sleep(0.2)
                dirty = True

# ===== Menu =====
def render_menu(options, selected, title="Main Menu", instructions="\nW/S to navigate, Q to select"):
    os.system("cls" if os.name == "nt" else "clear")
    print(color(title, GREEN))
    for i, opt in enumerate(options):
        pointer = "►" if i == selected else "  "
        print(f"{pointer} {opt}")
    print(instructions)

def main_menu():
    options = ["Continue Adventure", "New Adventure"]
    selected = 0
    while True:
        render_menu(options, selected)
        k = get_key()
        if not k: time.sleep(0.05); continue
        if k == 'w': selected = max(0, selected-1)
        elif k == 's': selected = min(1, selected+1)
        elif k == 'q':
            if selected == 0:
                saves = [f[:-5] for f in os.listdir('saves') if f.endswith('.json')] if os.path.exists('saves') else []
                if not saves:
                    print(color("\nNo saved worlds!", YELLOW))
                    time.sleep(1)
                    continue
                sel_world = 0
                while True:
                    render_menu(saves, sel_world, "Select World", "\nW/S navigate, Q select, T rename, X delete, E back")
                    k = get_key()
                    if not k: time.sleep(0.05); continue
                    if k == 'w': sel_world = max(0, sel_world-1)
                    elif k == 's': sel_world = min(len(saves)-1, sel_world+1)
                    elif k == 'q':
                        world_name = saves[sel_world]
                        wm, player = load_game(world_name)
                        if wm and player:
                            game_loop(wm, player, world_name)
                        break
                    elif k == 't':
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Enter new name: ")
                        new_name = input().strip()
                        if new_name and not os.path.exists(f"saves/{new_name}.json"):
                            os.rename(f"saves/{saves[sel_world]}.json", f"saves/{new_name}.json")
                            saves[sel_world] = new_name
                        else:
                            print("Invalid or existing name!")
                            time.sleep(1)
                    elif k == 'x':
                        os.system("cls" if os.name == "nt" else "clear")
                        confirm = input("Delete? (y/n): ")
                        if confirm.lower() == 'y':
                            os.remove(f"saves/{saves[sel_world]}.json")
                            del saves[sel_world]
                            sel_world = max(0, sel_world-1)
                    elif k == 'e':
                        break
            elif selected == 1:
                os.system("cls" if os.name == "nt" else "clear")
                print("Enter world name: ")
                world_name = input().strip()
                if not world_name or os.path.exists(f"saves/{world_name}.json"):
                    print("Invalid or existing name!")
                    time.sleep(1)
                    continue
                W, H = 20, 10
                wm = WorldManager(W, H)
                wm.map_x, wm.map_y = 0, 0
                wm.current_map = (0, 0)
                wm.get_world(0, 0)
                player = Player(W//2, H//2)
                player.inventory.add(Item("Wood Sword", meta={"type":"weapon","damage":5,"durability":10}))
                player.inventory.add(Item("Wood Bow", meta={"type":"bow","damage":10,"durability":30}))
                player.inventory.add(Item("Arrow Quill", meta={"type":"quill","arrows":10}))
                player.inventory.add(Item("Wood Shield", meta={"type":"shield","durability":5}))
                player.inventory.add(Item("Wood Potion", meta={"type":"consumable"}))
                player.inventory.add(Item("Wood Cross", meta={"type":"cross","uses":1}))
                player.inventory.add(Item("Wood Dagger", meta={"type":"dagger","damage":12,"uses":5}))
                game_loop(wm, player, world_name)

if __name__ == "__main__":
    main_menu()