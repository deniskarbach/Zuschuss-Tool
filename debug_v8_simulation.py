
import re

def run_simulation():
    print("--- V8 LOGIC SIMULATION (RHEIN-LAHN PREFIX ISSUE) ---")

    # HYPOTHESIS: 
    # Code Line 6: setup_lk_name = "Landkreis Rhein-Lahn-Kreis"
    # TN_LISTE Data: "Rhein-Lahn-Kreis" (without prefix)
    
    target_lk_code = "Landkreis Rhein-Lahn-Kreis"
    tn_data_lk = "Rhein-Lahn-Kreis"
    
    print(f"Code Expects: '{target_lk_code}'")
    print(f"Data Contains: '{tn_data_lk}'")
    
    # Logic from Line 104:
    # is_local; ARRAYFORMULA(REGEXMATCH(c_tags; "(^|;)" & target_lk & "(;|$)"));
    
    pattern = f"(^|;){re.escape(target_lk_code)}(;|$)"
    
    match = bool(re.search(pattern, tn_data_lk))
    print(f"Match Result: {match}")
    
    if not match:
        print("FAIL: The prefix 'Landkreis' in the code causes the mismatch.")
        print("FIX: Change Line 6 to 'Rhein-Lahn-Kreis' OR allow partial match.")

run_simulation()
