# TN_LISTE Struktur V7 (42 Spalten)

**Bereich:** B:AQ | **Index:** 1-42

---

## Meta-Bereich (B:M = Index 1-12)

| Spalte | Index | Feld | Typ | Hinweis |
|--------|-------|------|-----|---------|
| B | 1 | Status | Dropdown | Angemeldet/Abgemeldet/Storniert |
| C | 2 | Funktion | Dropdown | TN/MA/LEITUNG/REF |
| D | 3 | Juleica | Dropdown | Juleica/Nein/-- |
| E | 4 | Behinderung | Dropdown | MmB/BEGLEITPERSON/MmB_BEGLEITPERSON/-- |
| F | 5 | Soziales | Dropdown | Arbeitslos/Einkommensschwach/-- |
| G | 6 | Anwesenheit | Zahl | Anwesenheitstage |
| H | 7 | Reserve_1 | - | |
| I | 8 | Reserve_2 | - | |
| J | 9 | Reserve_3 | - | |
| K | 10 | Reserve_4 | - | |
| L | 11 | Reserve_5 | - | |
| M | 12 | Reserve_6 | - | |

---

## Daten-Bereich (N:AM = Index 13-38)

| Spalte | Index | Feld | Typ |
|--------|-------|------|-----|
| N | 13 | Nachname | Text |
| O | 14 | Vorname | Text |
| P | 15 | Geburtsdatum | Datum |
| Q | 16 | Adresse | Text |
| R | 17 | PLZ | Text |
| S | 18 | Wohnort | Text |
| T | 19 | Geschlecht | Text |
| U-AM | 20-38 | Reserve_7-25 | - |

---

## Auto-Bereich (AN:AQ = Index 39-42)

| Spalte | Index | Feld | Formel |
|--------|-------|------|--------|
| AN | 39 | Reserve_26 | - |
| AO | 40 | Alter | `=DATEDIF(P3;SETUP!$B$23;"Y")` |
| AP | 41 | Landkreis | `=SVERWEIS(R3;PLZDB!...;3;0)` |
| AQ | 42 | Bundesland | `=SVERWEIS(R3;PLZDB!...;4;0)` |

---

## Header-Zeile

Die Header stehen in **Zeile 2** (B2:AQ2).

## Daten-Zonen

| Zone | Bereich | Zeilen |
|------|---------|--------|
| 1 | B3:AQ749 | 3-749 |
| 2 | B754:AQ1454 | 754-1454 |
| 3 | B1459:AQ1710 | 1459-1710 |
