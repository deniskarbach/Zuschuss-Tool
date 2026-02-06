import csv
import random
import datetime

# Configuration
TOTAL_PAX = 300
REF_DATE = datetime.date(2026, 7, 1)

# Groups & Target Counts
GROUPS = {
    "Landkreis Mainz-Bingen": 70,       # Massentest
    "Landkreis Altenkirchen": 20,
    "Landkreis Alzey-Worms": 20,
    "Landkreis Bad Kreuznach": 20,
    "Landkreis Bernkastel-Wittlich": 20,
    "Kreisfreie Stadt Mainz": 20,
    "Rhein-Hunsrück-Kreis": 20,
    "Landkreis Rhein-Lahn-Kreis": 20,
    "Landkreis Trier-Saarburg": 20,
    "Westerwaldkreis": 20,
    "Gemeinde Neunkirchen": 15,         # NRW
    "Landkreis Gießen": 15,             # Hessen
    "Berlin, Stadt": 10,                # Auswärtig
    "Stadt München": 5,                 # Auswärtig
    "Stadt Hamburg": 5                  # Auswärtig
}

# State Mapping (Approximate)
STATE_MAP = {
    "Landkreis Mainz-Bingen": "Rheinland-Pfalz",
    "Landkreis Altenkirchen": "Rheinland-Pfalz",
    "Landkreis Alzey-Worms": "Rheinland-Pfalz",
    "Landkreis Bad Kreuznach": "Rheinland-Pfalz",
    "Landkreis Bernkastel-Wittlich": "Rheinland-Pfalz",
    "Kreisfreie Stadt Mainz": "Rheinland-Pfalz",
    "Rhein-Hunsrück-Kreis": "Rheinland-Pfalz",
    "Landkreis Rhein-Lahn-Kreis": "Rheinland-Pfalz",
    "Landkreis Trier-Saarburg": "Rheinland-Pfalz",
    "Westerwaldkreis": "Rheinland-Pfalz",
    "Gemeinde Neunkirchen": "Nordrhein-Westfalen",
    "Landkreis Gießen": "Hessen",
    "Berlin, Stadt": "Berlin",
    "Stadt München": "Bayern",
    "Stadt Hamburg": "Hamburg"
}

# PLZ Mapping (Approximate for the main town)
PLZ_MAP = {
    "Landkreis Mainz-Bingen": "55218",
    "Landkreis Altenkirchen": "57610",
    "Landkreis Alzey-Worms": "55232",
    "Landkreis Bad Kreuznach": "55543",
    "Landkreis Bernkastel-Wittlich": "54516",
    "Kreisfreie Stadt Mainz": "55116",
    "Rhein-Hunsrück-Kreis": "55469",
    "Landkreis Rhein-Lahn-Kreis": "56130",
    "Landkreis Trier-Saarburg": "54439",
    "Westerwaldkreis": "56410",
    "Gemeinde Neunkirchen": "57290",
    "Landkreis Gießen": "35390",
    "Berlin, Stadt": "10115",
    "Stadt München": "80331",
    "Stadt Hamburg": "20095"
}

CITY_MAP = {
    "Landkreis Mainz-Bingen": "Ingelheim am Rhein",
    "Landkreis Altenkirchen": "Altenkirchen",
    "Landkreis Alzey-Worms": "Alzey",
    "Landkreis Bad Kreuznach": "Bad Kreuznach",
    "Landkreis Bernkastel-Wittlich": "Wittlich",
    "Kreisfreie Stadt Mainz": "Mainz",
    "Rhein-Hunsrück-Kreis": "Simmern",
    "Landkreis Rhein-Lahn-Kreis": "Bad Ems",
    "Landkreis Trier-Saarburg": "Saarburg",
    "Westerwaldkreis": "Montabaur",
    "Gemeinde Neunkirchen": "Neunkirchen",
    "Landkreis Gießen": "Gießen",
    "Berlin, Stadt": "Berlin",
    "Stadt München": "München",
    "Stadt Hamburg": "Hamburg"
}

# Setup CSV Header
HEADER = ["Status", "Funktion", "Nachname", "Vorname", "Anwesenheit", "Juleica", "Behinderung", "Soziales", "Geburtsdatum", "Adresse", "PLZ", "Wohnort", "Geschlecht", "Landkreis (Spalte AQ)", "Bundesland"]

data_rows = []

def get_random_date(start_year, end_year):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{day:02d}.{month:02d}.{year}"

cnt_global = 0

for region, count in GROUPS.items():
    for i in range(count):
        cnt_global += 1
        
        # 1. Determine Function
        r_func = random.random()
        if r_func < 0.75:
            func = "TN"
            age_min, age_max = 6, 15
        elif r_func < 0.95:
            func = "MA"
            age_min, age_max = 16, 29
        elif r_func < 0.98:
            func = "LEITUNG"
            age_min, age_max = 25, 50
        else:
            func = "REF"
            age_min, age_max = 30, 60
            
        # 2. Status
        status = "Angemeldet"
        if random.random() < 0.05:
            status = "Storniert"
        elif random.random() < 0.02:
            status = "Abgemeldet"

        # 3. Attributes
        juleica = "--"
        if func in ["MA", "LEITUNG"] and random.random() < 0.5:
            juleica = "JB-12345"
            
        behinderung = "--"
        if random.random() < 0.05:
            behinderung = "G" if random.random() < 0.5 else "B"
            
        soziales = "--"
        if random.random() < 0.1:
            soziales = "Bildungspaket"
            
        anwesenheit = 10 
        if random.random() < 0.05:
            anwesenheit = random.randint(1, 5) # Short stay
            
        # 4. Age Edge Cases
        dob = get_random_date(REF_DATE.year - age_max, REF_DATE.year - age_min)
        if random.random() < 0.02 and func == "TN":
             # Edge Case: Exactly 5 years old (Zu Jung)
             dob = f"01.07.{REF_DATE.year - 5}"
             
        # 5. Names
        last_name = f"Testperson_{region.split(' ')[-1]}_{i+1}"
        first_name = f"{func}_{i+1}"
        
        # 6. Gender
        gender = random.choice(["m", "w", "d"])

        
        final_row = {
            "Status": status,
            "Funktion": func,
            "Nachname": last_name,
            "Vorname": first_name,
            "Anwesenheit": anwesenheit,
            "Juleica": juleica,
            "Behinderung": behinderung,
            "Soziales": soziales,
            "Geburtsdatum": dob,
            "Adresse": f"Musterstr. {cnt_global}",
            "PLZ": PLZ_MAP[region],
            "Wohnort": CITY_MAP[region],
            "Geschlecht": gender,
            "Landkreis": region,
            "Bundesland": STATE_MAP[region]
        }
        data_rows.append(final_row)

# Writing CSV
# We format it to match a likely Copy-Paste structure for Sheets
columns = ["Status", "Funktion", "Nachname", "Vorname", "Anwesenheit", "Juleica", "Behinderung", "Soziales", "Geburtsdatum", "Adresse", "PLZ", "Wohnort", "Geschlecht", "Landkreis", "Bundesland"]

with open("tests/V8_stress_test.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data_rows)

print(f"Generated {len(data_rows)} rows in tests/V8_stress_test.csv")
