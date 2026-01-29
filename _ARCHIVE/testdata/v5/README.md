# Testdaten V5 - Hardcore-Szenario

Diese CSV-Dateien enthalten Testdaten für das "Kipppunkt"-Testszenario der V5-Formel.

## Dateien

| Datei | Zone | Inhalt |
|-------|------|--------|
| `zone1_online.csv` | Z1 (Online) | 5 TN (inkl. 1 Storniert) |
| `zone2_local.csv` | Z2 (Local) | 4 TN + 2 MA |
| `zone3_manuell.csv` | Z3 (Manuell) | 3 TN + 2 MA |

## Import in Google Sheets

1. Öffne `TN_LISTE`
2. Zone 1: Einfügen ab **Zeile 3** (Bereich B3:AC)
3. Zone 2: Einfügen ab **Zeile 754** (Bereich B754:AC)
4. Zone 3: Einfügen ab **Zeile 1459** (Bereich B1459:AC)

**Trennzeichen:** Semikolon (;)

## CACHE_RULES Konfiguration

| Feld | Wert |
|------|------|
| Förderumfang | `TN_K_MA_K` |
| MIN_TN | `8` |
| MIN_ALTER | `7` |
| MAX_ALTER | `27` |
| MIN_ALTER_SOFT | `6` |
| MIN_TAGE | `3` |
| Quote | `51` |
| QUOTE_MODUS | `MEHRHEIT` |
| Logik | `Auffüllen` |

## SETUP Konfiguration

| Feld | Wert |
|------|------|
| Event-Start (B23) | `15.07.2026` |
| Event-Ende (H23) | `17.07.2026` |

## Erwartetes Ergebnis

**12 Personen** in der Ausgabe:
- 5 lokale TN (alphabetisch)
- 3 auswärtige TN (alphabetisch)
- 3 lokale MA (alphabetisch)
- 1 auswärtiger MA

**Ausgeschlossen:**
- Braun, Felix (Storniert)
- Klein, Emma (5 Jahre < MIN_ALTER_SOFT 6)
- Wagner, Paul (28 Jahre > MAX_ALTER 27)
