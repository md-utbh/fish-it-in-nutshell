import streamlit as st
import random
import math
import time

# --- SETUP HALAMAN WEB ---
st.set_page_config(page_title="Fish It In Nutshell", page_icon="🎣")

# --- GAME LOGIC ---
L_FACTOR = 0.95
CAST_BASE = 3.0

FISH_POOL = {
    "Common":   {"weight": (1, 4),    "chance": 70},
    "Uncommon": {"weight": (2, 7),    "chance": 20},
    "Rare":     {"weight": (4, 12),   "chance": 8},
    "Epic":     {"weight": (6, 18),   "chance": 1.6},
    "Legendary":{"weight": (10, 30),  "chance": 0.8},
    "Mythic":   {"weight": (20, 50),  "chance": 0.4},
    "Secret":   {"weight": (35, 90),  "chance": 0.2}
}

def scaled_luck(rod_luck, bait_luck):
    total = rod_luck + bait_luck
    return 1.0 + math.log10(1 + total) * L_FACTOR

def calculate_cast_time(speed):
    return CAST_BASE / (1 + math.log10(1 + speed))

def roll_rarity(luck_mult):
    current_weights = {}
    for rarity, data in FISH_POOL.items():
        base_chance = data["chance"]
        if rarity == "Common":
            current_weights[rarity] = base_chance
        else:
            current_weights[rarity] = base_chance * luck_mult
    total_weight = sum(current_weights.values())
    r = random.uniform(0, total_weight)
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
    roll = random.random() * 100
    if roll < 0.03: return ("Titanic", 1.50)
    if roll < 0.10: return ("Huge", 0.80)
    if roll < 0.40: return ("Big", 0.30)
    if roll < 1.00: return ("Shiny", 0.10)
    return None

def check_line_snap(weight, rod_line):
    chance = max(0, (weight - rod_line) * 3)
    return random.random() * 100 < chance

def fish_once(rod, bait):
    luck_mult = scaled_luck(rod["luck"], bait["luck"])
    rarity = roll_rarity(luck_mult)
    base_weight = roll_weight(rarity)
    mutation = roll_mutation()
    final_weight = base_weight
    if mutation:
        final_weight *= (1 + mutation[1])
    snapped = check_line_snap(final_weight, rod["line_str"])
    
    return {
        "rarity": rarity,
        "weight": final_weight,
        "mut": mutation[0] if mutation else None,
        "snapped": snapped
    }

# --- UI INTERFACE STREAMLIT ---
st.title("🎣 Fish It In Nutshell")
st.write('Or just call it "Simulasi RNG dengan Logarithmic Luck Scaling & Physics Weight."')

# Sidebar untuk Setting
st.sidebar.header("⚙️ Equipment Setup")
rod_choice = st.sidebar.selectbox("Pilih Rod", ["Element Rod", "Ghosfinn Rod", "Astral Rod"])
bait_choice = st.sidebar.selectbox("Pilih Bait", ["Singularity Bait", "Floral Bait", "No Bait"])

# Stats Mapping (Sederhana untuk demo)
rods_db = {
    "Element Rod": {"luck": 1111, "speed": 130, "line_str": 90},
    "Ghosfinn Rod": {"luck": 610, "speed": 118, "line_str": 60},
    "Astral Rod": {"luck": 380, "speed": 43, "line_str": 25}
}
baits_db = {
    "Singularity Bait": {"luck": 380},
    "Floral Bait": {"luck": 320},
    "No Bait": {"luck": 0}
}

current_rod = rods_db[rod_choice]
current_bait = baits_db[bait_choice]

st.sidebar.info(f"Total Luck: {current_rod['luck'] + current_bait['luck']}%\nSpeed: {current_rod['speed']}%")

# Main Area
col1, col2 = st.columns(2)

with col1:
    if st.button("🎣 FISH ONCE (Manual)"):
        cast_time = calculate_cast_time(current_rod['speed'])
        with st.spinner(f"Casting line... ({cast_time:.2f}s)"):
            time.sleep(cast_time)
        
        result = fish_once(current_rod, current_bait)
        
        if result['snapped']:
            st.error(f"⚠ LINE SNAPPED! {result['rarity']} ({result['weight']:.1f}kg) too heavy!")
        else:
            mut_text = f"[{result['mut']}] " if result['mut'] else ""
            st.success(f"CAUGHT! {mut_text}{result['rarity']} ({result['weight']:.1f}kg)")

with col2:
    afk_duration = st.slider("Durasi AFK (Detik)", 10, 60, 30)
    if st.button("🤖 START AFK MODE"):
        log_placeholder = st.empty()
        stats = {"Common":0, "Uncommon":0, "Rare":0, "Epic":0, "Legendary":0, "Mythic":0, "Secret":0}
        logs = []
        
        start_time = time.time()
        cast_time = calculate_cast_time(current_rod['speed'])
        
        progress_bar = st.progress(0)
        
        while time.time() - start_time < afk_duration:
            # Simulasi wait time
            time.sleep(cast_time) 
            
            res = fish_once(current_rod, current_bait)
            stats[res['rarity']] += 1
            
            # Update Log
            status = "SNAPPED" if res['snapped'] else "CAUGHT"
            logs.append(f"[{status}] {res['rarity']} - {res['weight']:.1f}kg")
            if len(logs) > 5: logs.pop(0) # Keep last 5
            
            # Tampilkan realtime
            log_text = "\n".join(logs)
            log_placeholder.code(log_text)
            
            # Update progress
            elapsed = time.time() - start_time
            progress_bar.progress(min(elapsed / afk_duration, 1.0))
            
        st.write("--- AFK RESULT ---")
        st.json(stats)
