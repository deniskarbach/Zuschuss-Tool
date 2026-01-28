# V7 Master-Formel: Finale Spezifikation

**Stand: 2026-01-23** | **Version: 7.0-final**

---

## 1. RULES-Blatt: Vollständige Struktur (A-Y)

### 1.1 Übersicht

| Bereich | Spalten | Inhalt |
|---------|---------|--------|
| **Identifikation** | A-D | KEY, Landkreis, Typ, Kürzel |
| **Basis-Regeln** | E-I | TN-Min, Alter, Tage |
| **Quote-Logik** | J-L | Quote-Wert, Modus, Aktion |
| **Target-Groups** | M-O | Funktionen, Wohnort-Check, Quote-Bezug |
| **Alter-Config** | P | Altersgrenzen für MA/LEITUNG/REF |
| **Ausgabe** | Q-T | Labels, Spalten, Sortierung, Filter |
| **Erweitert** | U-X | Properties, Status, Anwesenheit, Zonen |

### 1.2 Detaillierte Spalten-Definition

| Spalte | Feld | Typ | Werte/Beispiel | Standardwert |
|--------|------|-----|----------------|--------------|
| A | KEY | Text | `RLK_Soziale_Bildung` | - |
| B | LANDKREIS | Text | `Rhein-Lahn-Kreis` | - |
| C | TYP | Dropdown | siehe 1.5 | - |
| D | KUERZEL | Text | `RLK` | - |
| E | MIN_TN | Zahl | `5` | `0` |
| F | MIN_ALTER_TN | Zahl | `6` | `0` |
| G | MAX_ALTER_TN | Zahl | `27` | `999` |
| H | MIN_ALTER_SOFT_TN | Zahl | `5` | `=F` |
| I | MIN_TAGE | Zahl | `3` | `0` |
| J | MIN_QUOTE | Zahl | `51` | `0` |
| K | QUOTE_MODUS | Dropdown | `PROZENT` / `MEHRHEIT` | `MEHRHEIT` |
| **L** | **QUOTE_AKTION** | Dropdown | `NUR_LOKALE` / `ALLE_WENN_ERFUELLT` / `ALLE_IMMER` | `NUR_LOKALE` |
| **M** | TARGET_GROUPS | Dropdown | siehe 1.6 | `TN;MA;LEITUNG;REF` |
| **N** | TG_LOCAL_ONLY | Dropdown | siehe 1.7 | `TN` |
| **O** | QUOTE_BEZUG | Dropdown | siehe 1.8 | `TN` |
| **P** | ALTER_CONFIG | Text | `MA:16-99;LEITUNG:18-99` | _(leer)_ |
| **Q** | LABEL_MAP | Text | `MA=Betreuer:in;JULEICA_PH=J` | _(leer)_ |
| **R** | OUTPUT_COLUMNS | Text | `Name;Vorname;PLZ;Ort;Jahr` | Standard-Set |
| **S** | SORT_ORDER | Dropdown | siehe 1.4 | `LOKAL_FIRST;ALPHA` |
| **T** | FILTER_FUNCTION | Dropdown | siehe 1.9 | `ALL` |
| **U** | PROPERTY_MAP | Text | `MmB=mit Behinderung` | _(leer)_ |
| **V** | STATUS_FILTER | Dropdown | `Angemeldet` / `Alle` | `Angemeldet` |
| **W** | MIN_ANWESENHEIT | Zahl | `2` | `0` |
| **X** | ZONEN_CONFIG | Text | `3-749;754-1454;1459-1710` | Standard |

### 1.3 Dropdowns einrichten

| Spalte | Feld | Optionen |
|--------|------|----------|
| K | QUOTE_MODUS | `PROZENT`, `MEHRHEIT` |
| L | QUOTE_AKTION | `NUR_LOKALE`, `ALLE_WENN_ERFUELLT`, `ALLE_IMMER` |
| N | TG_LOCAL_ONLY | `TN`, `TN;MA`, `TN;MA;LEITUNG`, _(leer)_ |
| S | SORT_ORDER | siehe 1.4 |

### 1.4 SORT_ORDER Optionen

| Option | Bedeutung |
|--------|-----------|
| `ALPHA` | Alphabetisch A-Z |
| `ALPHA_DESC` | Alphabetisch Z-A |
| `LOKAL_FIRST;ALPHA` | Lokale zuerst, dann A-Z |
| `FUNKTION_ALPHA` | Nach Funktion, dann A-Z |
| `FUNKTION;LOKAL_FIRST;ALPHA` | Funktion, dann Lokale, dann A-Z |
| `LANDKREIS_ALPHA` | Nach Landkreis, dann A-Z |
| `BUNDESLAND_ALPHA` | Nach Bundesland, dann A-Z |
| `ALTER` | Nach Alter (jung → alt) |
| `KEINE` | Keine Sortierung |

### 1.5 TYP Optionen (Event-Typen)

| Option |
|--------|
| `Soziale_Bildung` |
| `Schulung_Ehrenamtlicher_Mitarbeitenden` |
| `Politische_Jugendbildung` |

### 1.6 TARGET_GROUPS Optionen

| Option | Bedeutung |
|--------|-----------|
| `TN;MA;LEITUNG;REF` | Alle Gruppen |
| `TN;MA;LEITUNG` | Ohne REF |
| `TN;MA` | Nur TN + MA |
| `TN` | Nur TN |

### 1.7 TG_LOCAL_ONLY Optionen

| Option | Bedeutung |
|--------|-----------|
| `TN` | Nur TN müssen lokal sein |
| `TN;MA` | TN + MA müssen lokal sein |
| `TN;MA;LEITUNG` | Alle außer REF müssen lokal sein |
| _(leer)_ | Niemand muss lokal sein |

### 1.8 QUOTE_BEZUG Optionen

| Option | Bedeutung |
|--------|-----------|
| `TN` | Quote nur für TN |
| `TN;MA` | Quote für TN + MA |
| `TN;MA;LEITUNG` | Quote für alle außer REF |

### 1.9 FILTER_FUNCTION Optionen

| Option | Bedeutung |
|--------|-----------|
| `ALL` | Alle Gruppen ausgeben |
| `TN_ONLY` | Nur TN |
| `STAFF_ONLY` | Nur MA + LEITUNG |
| `REF_ONLY` | Nur REF |

---

## 2. Wohnort-Logik: Entscheidungsbaum

### 2.1 Zwei Fragen

**Frage 1:** Wer braucht einen Wohnort-Check?
→ Antwort in `TG_LOCAL_ONLY`

**Frage 2:** Dürfen Auswärtige trotzdem drauf?
→ Antwort in `QUOTE_AKTION` + `QUOTE_BEZUG`

### 2.2 Entscheidungslogik

```
WENN QUOTE_AKTION = "ALLE_IMMER"
  → Alle (unabhängig von Wohnort)

WENN QUOTE_AKTION = "ALLE_WENN_ERFUELLT" UND Quote erfüllt UND Funktion in QUOTE_BEZUG
  → Alle

SONST
  WENN Funktion in TG_LOCAL_ONLY
    → Nur Lokale
  SONST
    → Alle
```

### 2.3 Beispiele

| Einstellung | Quote | TN-Ergebnis | MA-Ergebnis |
|-------------|-------|-------------|-------------|
| TG_LOCAL_ONLY=TN, QUOTE_AKTION=NUR_LOKALE | - | Nur lokal | Alle |
| TG_LOCAL_ONLY=TN, QUOTE_AKTION=ALLE_WENN_ERFUELLT, QUOTE_BEZUG=TN | ✅ 60% | **Alle** | Alle |
| TG_LOCAL_ONLY=TN, QUOTE_AKTION=ALLE_WENN_ERFUELLT, QUOTE_BEZUG=TN | ❌ 40% | Nur lokal | Alle |
| TG_LOCAL_ONLY=TN;MA, QUOTE_AKTION=ALLE_WENN_ERFUELLT, QUOTE_BEZUG=TN;MA | ✅ 55% | **Alle** | **Alle** |

### 2.4 Konfigurations-Szenarien

**Wie konfiguriere ich...?**

| Gewünschtes Ergebnis | QUOTE_AKTION | TG_LOCAL_ONLY | MIN_QUOTE |
|----------------------|--------------|---------------|-----------|
| **Nur lokale TN, MA global** | `NUR_LOKALE` | `TN` | _(egal)_ |
| **Nur lokale TN + MA** | `NUR_LOKALE` | `TN;MA` | _(egal)_ |
| **Alle TN wenn Quote erfüllt** | `ALLE_WENN_ERFUELLT` | `TN` | `51` |
| **Alle TN + MA wenn Quote erfüllt** | `ALLE_WENN_ERFUELLT` | `TN;MA` | `51` |
| **Immer ALLE (Quote egal, Wohnort egal)** | `ALLE_IMMER` | _(leer oder egal)_ | _(egal)_ |
| **Alle global (kein Wohnort-Check nötig)** | _(egal)_ | _(leer)_ | _(egal)_ |

> **Hinweis:** Wenn `QUOTE_AKTION = ALLE_IMMER` gesetzt ist, werden **alle Personen** auf die Liste genommen, unabhängig von Wohnort und Quote. Die Felder `TG_LOCAL_ONLY` und `MIN_QUOTE` werden dann ignoriert.

---

## 3. TN_LISTE: Spaltenstruktur

### 3.1 Übersicht (42 Spalten)

| Bereich | Spalten | Anzahl | Inhalt |
|---------|---------|--------|--------|
| **Meta** | B:M | 12 | Status, Funktion, Eigenschaften |
| **Daten** | N:AM | 26 | Persönliche Daten |
| **Auto** | AN:AP | 3 | Berechnete Felder |

### 3.2 Meta-Bereich (B:M)

| Spalte | Index | Feld | Typ |
|--------|-------|------|-----|
| B | 1 | Status | Dropdown: Angemeldet/Abgemeldet/Storniert |
| C | 2 | Funktion | Dropdown: TN/MA/LEITUNG/REF |
| D | 3 | Juleica | Dropdown: Ja/Nein/-- |
| E | 4 | Behinderung | Dropdown: MmB/BEGLEITPERSON/-- |
| F | 5 | Soziales | Dropdown: Arbeitslos/Einkommensschwach/-- |
| G | 6 | Anwesenheit | Zahl (Tage) |
| H-M | 7-12 | Reserve | Für Erweiterungen |

### 3.3 Daten-Bereich (N:AM)

| Spalte | Index | Feld |
|--------|-------|------|
| N | 13 | Nachname |
| O | 14 | Vorname |
| P | 15 | Geburtsdatum |
| Q | 16 | Straße + Nr |
| R | 17 | PLZ |
| S | 18 | Wohnort |
| T | 19 | Geschlecht |
| U-AM | 20-39 | Weitere (E-Mail, Telefon, etc.) |

### 3.4 Auto-Bereich (AN:AP)

| Spalte | Index | Feld | Formel |
|--------|-------|------|--------|
| AN | 40 | Alter | `=DATEDIF(P3; SETUP!$B$23; "Y")` |
| AO | 41 | Landkreis | `=SVERWEIS(R3; PLZDB...; 3)` |
| AP | 42 | Bundesland | `=SVERWEIS(R3; PLZDB...; 4)` |

---


---

## 6. Umsetzungs-Checkliste

### Phase 1: RULES erweitern
- [ ] Spalten N-Y anlegen
- [ ] Dropdowns (L, M, O) einrichten
- [ ] LOGIK → QUOTE_AKTION umbenennen
- [ ] Standardwerte eintragen

### Phase 2: TN_LISTE umstrukturieren
- [ ] Backup erstellen
- [ ] Meta-Bereich (B:M) anlegen
- [ ] Daten-Bereich (N:AM) anpassen
- [ ] Auto-Bereich (AN:AP) mit Formeln

### Phase 5: Testen
- [ ] 8 Testszenarien
- [ ] Edge Cases

### Phase 6: Validierung
- [ ] Vollständigkeitsprüfung
- [ ] Dokumentation finalisieren

---

## 7. REF-Schutz

**REF ist immer global.** Sichergestellt durch:
1. Dropdown TG_LOCAL_ONLY enthält REF nicht
2. Formel entfernt REF automatisch falls vorhanden

```excel
tg_local_clean; SUBSTITUTE(tg_local_only; "REF"; "")
```


```

### 9.6 V7-Spalten → Rules-Index

| V7 Spalte | Feld | Index |
|-----------|------|-------|
| J | MIN_QUOTE | 10 |
| K | QUOTE_MODUS | 11 |
| L | QUOTE_AKTION | 12 |
| M | TARGET_GROUPS | 13 |
| N | TG_LOCAL_ONLY | 14 |
| O | QUOTE_BEZUG | 15 |
| S | SORT_ORDER | 19 |
| V | STATUS_FILTER | 22 |


### 9.8 Umsetzungs-Checkliste (Ergänzung zu Phase 4)
- [ ] V6-Formeln archivieren

