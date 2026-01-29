# RULES Index V7 (24 Spalten)

**Bereich:** A:X | **Lookup via:** VLOOKUP(key; CACHE_RULES!A:X; col; 0)

---

## Spalten-Übersicht

| Spalte | Col | Feld | Typ | Standardwert |
|--------|-----|------|-----|--------------|
| A | 1 | KEY | Text | Pflicht |
| B | 2 | LANDKREIS | Text | Pflicht |
| C | 3 | TYP | Dropdown | Pflicht |
| D | 4 | KUERZEL | Text | - |
| E | 5 | MIN_TN | Zahl | 0 |
| F | 6 | MIN_ALTER_TN | Zahl | 0 |
| G | 7 | MAX_ALTER_TN | Zahl | 999 |
| H | 8 | MIN_ALTER_SOFT_TN | Zahl | =F |
| I | 9 | MIN_TAGE | Zahl | 0 |
| J | 10 | MIN_QUOTE | Zahl | 0 |
| K | 11 | QUOTE_MODUS | Dropdown | MEHRHEIT |
| L | 12 | QUOTE_AKTION | Dropdown | NUR_LOKALE |
| M | 13 | TARGET_GROUPS | Dropdown | TN;MA;LEITUNG;REF |
| N | 14 | TG_LOCAL_ONLY | Dropdown | TN |
| O | 15 | QUOTE_BEZUG | Dropdown | TN |
| P | 16 | ALTER_CONFIG | Text | *(leer)* |
| Q | 17 | LABEL_MAP | Text | *(leer)* |
| R | 18 | OUTPUT_COLUMNS | Text | Standard-Set |
| S | 19 | SORT_ORDER | Dropdown | LOKAL_FIRST;ALPHA |
| T | 20 | FILTER_FUNCTION | Dropdown | ALL |
| U | 21 | PROPERTY_MAP | Text | *(leer)* |
| V | 22 | STATUS_FILTER | Dropdown | Angemeldet |
| W | 23 | MIN_ANWESENHEIT | Zahl | 0 |
| X | 24 | ZONEN_CONFIG | Text | *(leer)* |

---

## Dropdown-Werte

### K: QUOTE_MODUS
- `PROZENT` - Quote als Prozentsatz prüfen
- `MEHRHEIT` - Lokale müssen Mehrheit sein

### L: QUOTE_AKTION
- `NUR_LOKALE` - Nur lokale Teilnehmer
- `ALLE_WENN_ERFUELLT` - Alle, wenn Quote erfüllt
- `ALLE_IMMER` - Immer alle

### M: TARGET_GROUPS
- `TN;MA;LEITUNG;REF` - Alle Gruppen
- `TN;MA;LEITUNG` - Ohne REF
- `TN;MA` - Nur TN + MA
- `TN` - Nur TN

### N: TG_LOCAL_ONLY
- `TN` - Nur TN müssen lokal sein
- `TN;MA` - TN + MA müssen lokal sein
- *(leer)* - Niemand muss lokal sein

### S: SORT_ORDER
- `ALPHA` - Alphabetisch
- `LOKAL_FIRST;ALPHA` - Lokale zuerst
- `FUNKTION_ALPHA` - Nach Funktion
- `KEINE` - Keine Sortierung
