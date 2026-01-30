import datetime
from dataclasses import dataclass
from typing import List, Optional

# --- DATENSTRUKTUREN ---

@dataclass
class Rules:
    min_anwesenheit: int = 0
    min_tage: int = 0
    min_anzahl: int = 0
    min_anzahl_bezug: str = "TN"
    
    min_alter_tn: int = 0       
    min_alter_tn_soft: int = 0  
    max_alter_tn: int = 0
    min_alter_ma: int = 0
    min_alter_leitung: int = 0
    
    min_quote: float = 0.0
    quote_mode: str = "PROZENT" 
    quote_bezug: List[str] = None # NEU: Wer zählt zur Quote? z.B. ["TN"]
    quote_action: str = "KEINE_QUOTE" 
    
    target_groups: List[str] = None 
    gruppen_nur_lokal: List[str] = None 

    setup_start: datetime.date = datetime.date(2026, 1, 1)
    setup_end: datetime.date = datetime.date(2026, 1, 5) 
    setup_landkreis: str = "Landkreis Rhein-Lahn-Kreis"

@dataclass
class Person:
    vorname: str
    nachname: str
    geburtsdatum: Optional[datetime.date]
    funktion: str # "TN", "MA", "LEITUNG"
    status: str   # "Angemeldet", "Storniert"
    wohnort_landkreis: str
    anwesenheit_tage: int

class V8Validator:
    def __init__(self, rules: Rules):
        self.rules = rules
        self.measure_duration = (rules.setup_end - rules.setup_start).days + 1
        # Default Quote Bezug falls leer: Alles was Target Group ist
        if not self.rules.quote_bezug:
             self.rules.quote_bezug = self.rules.target_groups

    # ... (calculate_age, get_effective_min_age_tn, validate_person bleiben gleich) ...
    def calculate_age(self, geburtsdatum: datetime.date) -> int:
        if not geburtsdatum:
            return 0
        end_date = self.rules.setup_end
        age = end_date.year - geburtsdatum.year - ((end_date.month, end_date.day) < (geburtsdatum.month, geburtsdatum.day))
        return age

    def get_effective_min_age_tn(self) -> int:
        soft = self.rules.min_alter_tn_soft
        hard = self.rules.min_alter_tn
        if soft > 0 and soft < hard:
            return soft
        return hard

    def validate_person(self, p: Person) -> list[str]:
        reasons = []
        if "Angemeldet" not in p.status:
            reasons.append(f"Status: {p.status}")
            return reasons 
        if self.rules.target_groups and p.funktion not in self.rules.target_groups:
            reasons.append(f"Funktion '{p.funktion}' nicht in Zielgruppe")
            return reasons
        age = self.calculate_age(p.geburtsdatum)
        if not p.geburtsdatum:
             reasons.append("Geburtsdatum fehlt")
        else:
            if p.funktion == "TN":
                eff_min = self.get_effective_min_age_tn()
                if age < eff_min:
                    reasons.append(f"Zu jung (TN): {age} < {eff_min}")
                if self.rules.max_alter_tn > 0 and age > self.rules.max_alter_tn:
                    reasons.append(f"Zu alt (TN): {age} > {self.rules.max_alter_tn}")
            elif p.funktion == "LEITUNG":
                min_l = self.rules.min_alter_leitung if self.rules.min_alter_leitung > 0 else self.rules.min_alter_ma
                if age < min_l:
                    reasons.append(f"Zu jung (LEITUNG): {age} < {min_l}")
            elif "MA" in p.funktion:
                if age < self.rules.min_alter_ma:
                    reasons.append(f"Zu jung (MA): {age} < {self.rules.min_alter_ma}")
        if self.rules.min_anwesenheit > 0 and p.anwesenheit_tage < self.rules.min_anwesenheit:
             reasons.append(f"Zu wenig Tage: {p.anwesenheit_tage} < {self.rules.min_anwesenheit}")
        is_local = p.wohnort_landkreis == self.rules.setup_landkreis
        if self.rules.gruppen_nur_lokal and p.funktion in self.rules.gruppen_nur_lokal:
            if not is_local:
                reasons.append(f"Muss Lokal sein ({p.funktion})")
        return reasons 

    def validate_group(self, persons: List[Person]) -> dict:
        valid_candidates = []
        for p in persons:
            rejections = self.validate_person(p)
            if not rejections:
                valid_candidates.append(p)
        
        global_errors = []
        if self.rules.min_tage > 0 and self.measure_duration < self.rules.min_tage:
            global_errors.append(f"Maßnahme zu kurz ({self.measure_duration} < {self.rules.min_tage})")
            return {"accepted": [], "global_errors": global_errors}

        # Phase 3: Quote (Mit Quote Bezug!)
        # Filter Kandidaten, die für die Quote relevant sind
        quote_relevant_candidates = [p for p in valid_candidates if p.funktion in self.rules.quote_bezug]
        
        cnt_base = len(quote_relevant_candidates)
        cnt_local = sum(1 for p in quote_relevant_candidates if p.wohnort_landkreis == self.rules.setup_landkreis)
        
        # Quote berechnen (Nur auf Basis der relevanten!)
        quote_ok = False
        quote_pct = 0
        if cnt_base > 0:
            quote_pct = cnt_local / cnt_base
            if self.rules.quote_mode == "MEHRHEIT":
                cnt_extern = cnt_base - cnt_local
                quote_ok = cnt_local > cnt_extern
            else: # PROZENT
                quote_ok = quote_pct >= self.rules.min_quote
        else:
            quote_ok = True 

        force_local_filter = False
        if self.rules.quote_action == "STRIKT_LOKAL":
            force_local_filter = True
        elif self.rules.quote_action == "SOLIDARISCH" and not quote_ok:
            force_local_filter = True
        
        final_list = []
        for p in valid_candidates:
            is_local = p.wohnort_landkreis == self.rules.setup_landkreis
            # Filter greift: Wenn externe gefiltert werden müssen...
            if force_local_filter and not is_local:
                # ...aber nur, wenn die Person auch zur Quote gehört? NEIN!
                # V8 Logik checken: force_local_filter entfernt ALLE externen, egal ob Bezug oder nicht.
                # (Sicherheitshalber: meist werden auch externe Referenten entfernt bei Solidarisch)
                continue 
            final_list.append(p)

        # Phase 4: Mindestanzahl
        cnt_check = 0
        for p in final_list:
            # Check MIN_ANZAHL_BEZUG (ist in der alten Implementation fixed auf TN/ALLE, hier vereinfacht)
            if self.rules.min_anzahl_bezug == "ALLE" or p.funktion == "TN":
                cnt_check += 1
        
        if self.rules.min_anzahl > 0 and cnt_check < self.rules.min_anzahl:
             global_errors.append(f"Zu wenige Teilnehmer ({cnt_check} < {self.rules.min_anzahl})")
             return {"accepted": [], "global_errors": global_errors}

        return {"accepted": final_list, "global_errors": [], "quote_info": f"{cnt_local}/{cnt_base} ({quote_pct:.0%})"}

def run_advanced_scenarios():
    print("--- START V8 ADVANCED LOGIC SIMULATOR ---")
    
    # Test-Personen
    # Sophie (TN, Lokal), Max (TN, Extern), Chef (MA, Extern), Boss (Leitung, Lokal)
    pool = [
        Person("Sophie", "Lokal", datetime.date(2010, 1, 1), "TN", "Angemeldet", "Landkreis Rhein-Lahn-Kreis", 5),
        Person("Max", "Extern", datetime.date(2010, 1, 1), "TN", "Angemeldet", "Berlin", 5),
        Person("Chef", "MA_Extern", datetime.date(1990, 1, 1), "MA", "Angemeldet", "Berlin", 5),
        Person("Boss", "Leitung", datetime.date(1980, 1, 1), "LEITUNG", "Angemeldet", "Landkreis Rhein-Lahn-Kreis", 5)
    ]
    
    # A) TARGET GROUPS: Nur TN erlaubt. MA müssen raus.
    print("\n🔹 SZENARIO A: Target Groups = ['TN'] (MA Chef muss raus)")
    rules_a = Rules(target_groups=["TN"], setup_end=datetime.date(2026,2,1))
    res_a = V8Validator(rules_a).validate_group(pool)
    accepted = [p.vorname for p in res_a['accepted']]
    if "Chef" not in accepted and "Boss" not in accepted and "Sophie" in accepted:
        print("   ✅ Korrekt: Nur TN sind drin.")
    else:
        print(f"   ❌ FEHLER: {accepted}")

    # B) LOCAL ONLY: TN müssen lokal sein. MA dürfen extern sein.
    print("\n🔹 SZENARIO B: Gruppen Nur Lokal = ['TN'] (Max muss raus, Chef darf bleiben)")
    rules_b = Rules(target_groups=["TN", "MA", "LEITUNG"], gruppen_nur_lokal=["TN"], setup_end=datetime.date(2026,2,1))
    res_b = V8Validator(rules_b).validate_group(pool)
    accepted = [p.vorname for p in res_b['accepted']]
    if "Max" not in accepted and "Chef" in accepted:
        print("   ✅ Korrekt: Externer Max gefiltert, Externer Chef erlaubt.")
    else:
         print(f"   ❌ FEHLER: {accepted}")

    # C) QUOTE BEZUG: Quote zählt nur TN. (Chef Ma_Extern versaut Quote nicht)
    # 1 TN Lokal, 1 TN Extern -> 50%. Min Quote 50%.
    # MA Extern ist dabei. Wenn MA zählen würden, wäre Quote 1/3 = 33% (Fail).
    print("\n🔹 SZENARIO C: Quote Bezug = ['TN'] (MA ignoriert)")
    rules_c = Rules(
        target_groups=["TN", "MA"], 
        min_quote=0.5, quote_mode="PROZENT", quote_bezug=["TN"], quote_action="SOLIDARISCH",
        setup_end=datetime.date(2026,2,1)
    )
    res_c = V8Validator(rules_c).validate_group(pool)
    accepted = [p.vorname for p in res_c['accepted']]
    # Sophie (L), Max (E) -> 50% OK. Chef (E) ist egal. Alle bleiben.
    if "Max" in accepted and "Chef" in accepted:
         print(f"   ✅ Korrekt: Quote 50% erfüllt (nur TN gezählt). Alle Externe bleiben. Info: {res_c.get('quote_info')}")
    else:
         print(f"   ❌ FEHLER: Jemand flog raus. {accepted} Info: {res_c.get('quote_info')}")

    # D) QUOTE AKTION: SOLIDARISCH vs STRIKT bei Fail
    # Quote Fail erzwingen: Min Quote 90%.
    print("\n🔹 SZENARIO D: Quote Fail (90% nötig) -> Solidarisch")
    rules_d = rules_c # Kopie
    rules_d.min_quote = 0.9
    res_d = V8Validator(rules_d).validate_group(pool)
    accepted = [p.vorname for p in res_d['accepted']]
    # Quote Fail -> Externe (Max, Chef) müssen fliegen.
    if "Max" not in accepted and "Chef" not in accepted and "Sophie" in accepted:
         print("   ✅ Korrekt: Solidarisch griff, Externe entfernt.")
    else:
         print(f"   ❌ FEHLER: {accepted}")

    print("\n--- END ADVANCED SIMULATOR ---")

if __name__ == "__main__":
    run_advanced_scenarios()
