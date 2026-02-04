
import re

def run_simulation():
    print("--- V8 DISPLAY MODE FAILURE SIMULATION ---")

    # Scenario: FILTERED works, SHOW_ALL fails.
    # display_mode = "SHOW_ALL"
    
    # Mock Arrays (Length 3)
    c_func = ["TN", "TN", "MA"]
    mask_eligible = [1, 1, 0] # 2 Valid TNs
    mask_base_pool = [1, 1, 1] 
    
    display_mode = "SHOW_ALL"
    
    # 1. Logic
    is_filtered = display_mode == "FILTERED"
    is_show_all = display_mode == "SHOW_ALL"
    
    regex_display_custom = display_mode.replace(";", "|")
    
    # mask_display_custom
    # In Code: REGEXMATCH(c_func, regex_custom)
    # If regex is "SHOW_ALL", does it match "TN"? NO.
    # If regex is "TN", it matches.
    
    def simulate_regex(func, pat):
        try:
            return 1 if re.search(pat, func) else 0
        except:
            return 0 # Error -> False
            
    mask_display_custom = [simulate_regex(f, regex_display_custom) for f in c_func]
    print(f"Mask Custom (Pat: {regex_display_custom}): {mask_display_custom}")
    # Results for SHOW_ALL: [0, 0, 0] (no match against "TN")
    
    # mask_add_on
    # Code: IF(is_show_all; mask_base_pool; mask_base_pool * mask_display_custom)
    mask_add_on = []
    if is_show_all:
        mask_add_on = mask_base_pool # [1, 1, 1]
    else:
        mask_add_on = [b * c for b, c in zip(mask_base_pool, mask_display_custom)]
        
    print(f"Mask AddOn: {mask_add_on}")
    
    # mask_display
    # Code: IF(is_filtered; mask_eligible; mask_eligible + mask_add_on)
    mask_display = []
    if is_filtered:
        mask_display = mask_eligible
    else:
        # Addition
        mask_display = [e + a for e, a in zip(mask_eligible, mask_add_on)]
        
    print(f"Mask Display: {mask_display}")
    # Result: [2, 2, 1] (Indices 0, 1, 2 should be shown)
    
    # Why would Sheets fail?
    # Maybe FILTER rejects values > 1?
    # Code: IFERROR(FILTER(SEQUENCE(...); mask_display); 0);
    # Sheets FILTER usually treats any Non-Zero number as TRUE.
    # But just in case, logic usually normalizes to (val > 0).
    
    print("Everything works in Python logic. Issue might be GSheets specific.")
    print("Hypothesis: Is Regex 'SHOW_ALL' causing an error inside REGEXMATCH if not found?")
    # No, just False.
    
    # Hypothesis 2: display_mode_raw is not string?
    # r_txt uses TRIM(CLEAN(...)) -> Valid string.
    
    # Hypothesis 3: display_mode with space? "SHOW_ALL " -> TRIM catches this.
    
    # Hypothesis 4: c_func has Header Row included? 
    # raw_data starts A2. c_func matches rows.
    
run_simulation()
