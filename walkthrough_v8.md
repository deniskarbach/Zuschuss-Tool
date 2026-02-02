# Walkthrough: V8 Formeln Session 2026-02-02

## Zusammenfassung

Diese Session fokussierte auf die Einführung des **Zuschuss-Tags Systems** (Multi-Listen-Zuordnung) und die Implementierung der V8 Formeln für **VG Rüdesheim** und das Land **NRW**.

---

## Erledigte Aufgaben

### 1. Zuschuss-Tags System (Multi-Listen) ✅
- **Problem:** Orte wie Hargesheim gehören zum LK Bad Kreuznach UND zur VG Rüdesheim.
- **Lösung:** Neue Spalte `AS` ("Zuschuss-Tags") in `TN_LISTE`.
- **Logik:** Formeln prüfen per `REGEXMATCH` auf Tags in dieser Spalte.
- **Update:** Alle 36 bestehenden V8 Formeln wurden auf diese Logik umgestellt.

### 2. VG Rüdesheim V8 ✅
- **Layout:** 4 Bereiche (MA, TN1-3) mit insgesamt 59 Zeilen Kapazität.
- **Formeln:** `vgruedesheimV8_MA.txt`, `_TN1.txt`, `_TN2.txt`, `_TN3.txt` erstellt.

### 3. Land NRW V8 ✅
- **Layout:** Basierend auf Photo analysiert (14 + 26 Zeilen).
- **Besonderheit:** Mixed List (TN, MA, LEITUNG, REF in einer Tabelle).
- **Spalten:** Inklusive Spalte H ("Adresse" / Straße).
- **Formeln:** `nrwV8_TN1.txt`, `nrwV8_TN2.txt` erstellt.

---

## Aktualisierte V8 Formel-Liste (42 Dateien)

| Region | Anzahl Formeln | Status |
| :--- | :--- | :--- |
| Rheinland-Pfalz (Land) | 1 | Tag-Logic ✅ |
| Altenkirchen | 1 | Tag-Logic ✅ |
| Alzey-Worms | 3 | Tag-Logic ✅ |
| Bad Kreuznach (Kreis + Stadt) | 5 | Tag-Logic ✅ |
| Bernkastel-Wittlich | 4 | Tag-Logic ✅ |
| Mainz (Stadt) | 4 | Tag-Logic ✅ |
| Mainz-Bingen | 3 | Tag-Logic ✅ |
| Rhein-Hunsrück-Kreis | 4 | Tag-Logic ✅ |
| Rhein-Lahn-Kreis | 1 | Tag-Logic ✅ |
| Trier-Saarburg | 2 | Tag-Logic ✅ |
| Westerwaldkreis | 4 | Tag-Logic ✅ |
| **VG Rüdesheim** | 4 | NEU ✅ |
| **NRW (Land)** | 2 | NEU ✅ |

---

## Technische Details (NRW)

**RULES-Tags:**
- `Nordrhein-Westfalen_Soziale_Bildung` etc.
- `OUTPUT_COLUMNS`: `{Nachname}; {Vorname}; {Funktion}; {Alter}; {PLZ}; {Wohnort}; {Adresse}`
- `LABEL_MAP`: `Funktion:LEITUNG=L;Funktion:MA=M;Funktion:TN=`

---

## Nächste Schritte
- [ ] Verifizierung der NRW-Formeln in Google Sheets (Stichprobe).
- [ ] Dokumentation für den User: Spalte `AS` in `TN_LISTE` mit Tags pflegen.
