import csv
from datetime import datetime

# --- CONFIG MAINZ-BINGEN (User Specific: 42) ---
CONFIG = {
    "setup_start": datetime.strptime("01.02.2026", "%d.%m.%Y"),
    "setup_end": datetime.strptime("14.02.2026", "%d.%m.%Y"),
    "target_lk": "Landkreis Mainz-Bingen",
    
    "min_tage": 1,      # From config (Col H)
    "min_anw": 7,       # From config (Col I) - This is the killer!
    
    # Age Limits (Parsed: 7, 27, 7)
    "min_alter_tn_hard": 7,
    "min_alter_tn_soft": 7,  # Effectively 7
    "max_alter_tn": 27, 
    "min_alter_ma": 16, # Standard? Assuming standard if not in snippets
    "min_alter_leit": 18,
    
    "target_groups": ["TN", "MA", "LEITUNG"], 
    
    # Quota Config
    "min_quote": 1.0, # 100% written in prompt
    "quote_action": "SOLIDARISCH", # "--" usually maps to Default/Solidarisch behavior (filter if fail)
    "quote_mode": "MEHRHEIT", # New param to handle
    "quote_bezug": ["TN"], # Default if empty in user string? "MEHRHEIT" usually ignores empty
    
    "status_ok": ["Angemeldet"],
    "must_be_local": [] 
}

def calculate_age(dob_str, ref_date):
    try:
        dob = datetime.strptime(dob_str, "%d.%m.%Y")
        age = ref_date.year - dob.year - ((ref_date.month, ref_date.day) < (dob.month, dob.day))
        return age
    except:
        return 0

def clean_days(d):
    try:
        return int(d)
    except:
        return 0

csv_file = "tests/V8_stress_test.csv"

candidates = []

print(f"--- STARTING SIMULATION ALTENKIRCHEN (SCENARIO A - FIXED) ---")
print(f"Config: 50% Quote (Base: TN), Solidarisch, TN+MA+LEITUNG")

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Filters (Status, Target Group, Duration, Age, Must-Be-Local)
        if row["Status"] not in CONFIG["status_ok"]:
            continue
        func = row["Funktion"]
        if func not in CONFIG["target_groups"]:
            continue
        days = clean_days(row["Anwesenheit"])
        if days < CONFIG["min_anw"]:
             continue
             
        age = calculate_age(row["Geburtsdatum"], CONFIG["setup_end"])
        age_ok = True
        if func == "TN":
             if age < CONFIG["min_alter_tn_hard"] or (CONFIG["max_alter_tn"] > 0 and age > CONFIG["max_alter_tn"]):
                 age_ok = False
        elif func == "MA":
             if age < CONFIG["min_alter_ma"]:
                 age_ok = False
        elif func == "LEITUNG":
             if age < CONFIG["min_alter_leit"]:
                 age_ok = False
        if not age_ok:
            continue
            
        is_local = (row["Bundesland"] == CONFIG["target_lk"]) or (row["Landkreis"] == CONFIG["target_lk"])
        must_be_local_group = (func in CONFIG["must_be_local"])
        if must_be_local_group and not is_local:
            continue

        row["_is_local"] = is_local
        candidates.append(row)

# --- QUOTA CHECK ---
if not candidates:
    print("No candidates found.")
    exit()

# V8 Logic: Calculate Quota ONLY on 'quote_bezug' groups
# mask_quote_relevant; ARRAYFORMULA(REGEXMATCH(c_func; regex_quote_bezug));
relevant_candidates = [c for c in candidates if c["Funktion"] in CONFIG["quote_bezug"]]

cnt_base = len(relevant_candidates)
cnt_loc = sum(1 for c in relevant_candidates if c["_is_local"])

quote = 0
if cnt_base > 0:
    quote = cnt_loc / cnt_base

print(f"Full Pool: {len(candidates)}")
print(f"Quota Base ({CONFIG['quote_bezug']}): {cnt_base} (Local: {cnt_loc}) -> Quote: {quote:.2%} (Target: {CONFIG['min_quote']:.0%})")

final_list = []

force_filter = False

# V8 Logic for MEHRHEIT:
# quote_ok; IF(quote_mode="MEHRHEIT"; cnt_loc > (cnt_base - cnt_loc); quote_pct >= min_quote);
quote_ok = False
if CONFIG.get("quote_mode") == "MEHRHEIT":
    quote_ok = cnt_loc > (cnt_base - cnt_loc) # More locals than non-locals
else:
    quote_ok = quote >= CONFIG["min_quote"]

print(f"Quote OK: {quote_ok} (Mode: {CONFIG.get('quote_mode', 'PERCENT')})")

if CONFIG["quote_action"] == "STRIKT_LOKAL":
    force_filter = True 
elif CONFIG["quote_action"] == "SOLIDARISCH":
    if not quote_ok:
        force_filter = True

for c in candidates:
    if force_filter and not c["_is_local"]:
        continue
    final_list.append(c)

print(f"Applied Filter: {force_filter}")
print(f"FINAL VALID COUNT: {len(final_list)}")
