# Kontext für die nächste Session

## Projekt: Zuschusslisten-Formeln (Google Sheets)

### Was wurde gemacht:

1. **V3.1 Logik-Vereinfachung:**
   - "Auffüllen" wirkt jetzt einheitlich auf TN UND MA
   - Quote = 0 überspringt die Quote-Prüfung komplett

2. **TN_LISTE-Strukturänderung (V4 → V5):**
   - 29 Spalten statt 22 (7 Platzhalter T-Z nach Geschlecht)
   - Spalte G = Anwesenheit, H-L = Reserve, T-Z = Platzhalter
   - Alle Indizes ab Alter um +7 verschoben (gegenüber V4)

3. **V5-Formel Rhein-Lahn-Kreis:**
   - Datei: `RLP/Kreise/V5/Rhein-Lahn-Kreis/rheinlahnkreisV5.md`
   - Angepasst an 29-Spalten-Struktur
   - Debugging-Test steht noch aus

---

## Prompt für die nächste Session:

```
Wir arbeiten an den Zuschusslisten-Formeln für Google Sheets. 

Zuletzt wurde:
- Die TN_LISTE auf 29 Spalten erweitert (7 Platzhalter T-Z nach Geschlecht)
- Die V5-Formel für Rhein-Lahn-Kreis erstellt

Heute stehen an:
1. V5-Debugging mit allen Testszenarien
2. RLP-Landesformel erstellen (rheinlandpfalzV1.md)

Wichtige Dateien:
- RLP/Kreise/V5/Rhein-Lahn-Kreis/rheinlahnkreisV5.md (aktuelle Formel)
- docs/manuals/rules_konfiguration.md (Handbuch)
- TODO_2026-01-19.md (Aufgabenliste)

Dropdown-Werte:
- Behinderung: Ja/Nein/--
- Soziales: Arbeitslos/Einkommensschwach/--

Starte mit dem V5-Debugging.
```

---

## Spalten-Index-Referenz (V5)

| Feld | Index | Spalte |
|------|-------|--------|
| Status | 1 | B |
| Funktion | 2 | C |
| Behinderung | 4 | E |
| Soziales | 5 | F |
| Anwesenheit | 6 | G |
| Nachname | 12 | M |
| Vorname | 13 | N |
| Geburtsdatum | 14 | O |
| PLZ | 16 | Q |
| Wohnort | 17 | R |
| Geschlecht | 18 | S |
| *Platz_1 - Platz_7* | 19-25 | T-Z |
| Alter | 26 | AA |
| Landkreis | 27 | AB |
| Bundesland | 28 | AC |
