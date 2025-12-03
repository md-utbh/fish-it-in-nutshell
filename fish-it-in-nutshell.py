import random
import math
import time

# ---------------------
#    GAME CONSTANTS
# ---------------------
L_FACTOR = 0.95
CAST_BASE = 3.0

MUTATION_TABLE = [
    ("Shiny", 0.10),
    ("Big",   0.30),
    ("Huge",  0.80),
    ("Titanic", 1.50),
]

FISH_POOL = {
    "Common":   {"weight": (1, 4),    "chance": 70},
    "Uncommon": {"weight": (2, 7),    "chance": 20},
    "Rare":     {"weight": (4, 12),   "chance": 8},
    "Epic":     {"weight": (6, 18),   "chance": 1.6},
    "Legendary":{"weight": (10, 30),  "chance": 0.8},
    "Mythic":   {"weight": (20, 50),  "chance": 0.4},
    "Secret":    {"weight": (35, 90),  "chance": 0.2}
}

# ---------------------
#   HELPER FUNCTIONS
# ---------------------

def scaled_luck(rod_luck, bait_luck):
    total = rod_luck + bait_luck
    return 1.0 + math.log10(1 + total) * L_FACTOR

def calculate_cast_time(speed):
    return CAST_BASE / (1 + math.log10(1 + speed))

def roll_rarity(luck_mult):
    # 1. Buat pool peluang baru yang sudah dikalikan Luck
    # Item langka bobotnya dikali luck_mult, item Common tetap.
    current_weights = {}
    for rarity, data in FISH_POOL.items():
        base_chance = data["chance"]
        if rarity == "Common":
            current_weights[rarity] = base_chance
        else:
            # Tier tinggi mendapat boost dari luck
            current_weights[rarity] = base_chance * luck_mult
    
    # 2. Hitung total bobot baru
    total_weight = sum(current_weights.values())
    
    # 3. Roll Random Standard
    r = random.uniform(0, total_weight)
    
    # 4. Cek Cumulative
    cumulative = 0
    for rarity, weight in current_weights.items():
        cumulative += weight
        if r <= cumulative:
            return rarity
            
    return "Common"

def roll_weight(rarity):
    lo, hi = FISH_POOL[rarity]["weight"]
    return random.uniform(lo, hi)

def roll_mutation():
    roll = random.random() * 100  # 0–100%
    if roll < 0.03: return ("Titanic", 1.50)
    if roll < 0.10: return ("Huge", 0.80)
    if roll < 0.40: return ("Big", 0.30)
    if roll < 1.00: return ("Shiny", 0.10)
    return None

def check_line_snap(weight, rod_line):
    chance = max(0, (weight - rod_line) * 3)
    return random.random() * 100 < chance

# ---------------------
#    MAIN CATCH LOGIC
# ---------------------

def fish_once(rod, bait, verbose=True):
    luck_mult = scaled_luck(rod["luck"], bait["luck"])
    cast_time = calculate_cast_time(rod["speed"])

    time.sleep(cast_time)  # FIXED — cannot bypass via AFK

    rarity = roll_rarity(luck_mult)
    base_weight = roll_weight(rarity)

    mutation = roll_mutation()
    final_weight = base_weight

    if mutation:
        final_weight *= (1 + mutation[1])  # Weight boost

    snapped = check_line_snap(final_weight, rod["line_str"])

    if verbose:
        print(f"Casted {cast_time:.2f}s → {rarity} ({final_weight:.1f}kg){' + '+mutation[0] if mutation else ''}")
        if snapped:
            print("⚠ Line snapped!")

    return {
        "rarity": rarity,
        "weight": final_weight,
        "mut": mutation[0] if mutation else None,
        "snapped": snapped
    }

# ---------------------
#     AFK MODE FIXED
# ---------------------

def afk_true(rod, bait, seconds=60):
    print(f"AFK TRUE MODE • {seconds} detik tanpa cheat speed…")
    start = time.time()
    results = []

    while time.time() - start < seconds:
        results.append(fish_once(rod, bait, verbose=False))

    return results
