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

## 4. COL_DEF: Output-Mapping

### 4.1 Feste Schlüssel

| Schlüssel | TN_LISTE Index | Typ |
|-----------|----------------|-----|
| `Name` | 13 | Direkt |
| `Vorname` | 14 | Direkt |
| `Geburtsdatum` | 15 | Direkt |
| `Jahr` | 15 | Formel: `YEAR()` |
| `Straße` | 16 | Direkt |
| `PLZ` | 17 | Direkt |
| `Ort` | 18 | Direkt |
| `Geschlecht` | 19 | Direkt |
| `Alter` | 40 | Direkt |
| `Landkreis` | 41 | Direkt |
| `Bundesland` | 42 | Direkt |
| `Funktion` | 2 | Direkt/LABEL_MAP |
| `Juleica` | 3 | Direkt |
| `Behinderung` | 4 | Direkt |
| `Anwesenheit` | 6 | Direkt |

### 4.2 Kombinierte Schlüssel

| Schlüssel | Formel |
|-----------|--------|
| `Name+Vorname` | `Name & ", " & Vorname` |
| `Vorname+Name` | `Vorname & " " & Name` |
| `PLZ+Ort` | `PLZ & ", " & Ort` |
| `L/M` | `IF(Funktion="LEITUNG"; "L"; "M")` |
| `Unterschrift` | _(leere Spalte)_ |

---

## 5. Master-Formel: Logik-Blöcke

### 5.1 Filter-Kette

```
1. STATUS_FILTER → Nur "Angemeldet"
2. TARGET_GROUPS → Nur erlaubte Funktionen
3. ALTER_CONFIG → Altersgrenzen pro Funktion
4. MIN_ANWESENHEIT → Mindest-Anwesenheit
5. Wohnort-Logik → TG_LOCAL_ONLY + QUOTE_AKTION
```

### 5.2 Quote-Berechnung

```
1. QUOTE_BEZUG → Welche Funktionen zählen
2. Lokale zählen → Landkreis = Ziel-Landkreis
3. MIN_QUOTE + QUOTE_MODUS → Ist erfüllt?
4. QUOTE_AKTION → use_all = TRUE/FALSE
```

### 5.3 Sortierung

```
1. SORT_ORDER parsen
2. LOKAL_FIRST → Lokale vor Auswärtigen
3. ALPHA → Alphabetisch nach Name
```

### 5.4 Ausgabe

```
1. OUTPUT_COLUMNS → Welche Spalten
2. LABEL_MAP → Funktions-Labels ersetzen
3. PROPERTY_MAP → Eigenschaften ersetzen
4. ZONEN_CONFIG → Paginierung
```

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

### Phase 3: COL_DEF erstellen
- [ ] Neues Blatt "COL_DEF"
- [ ] 15 feste Schlüssel
- [ ] 5 kombinierte Schlüssel

### Phase 4: Master-Formel
- [ ] Hilfsfunktionen
- [ ] Filter-Logik
- [ ] Quote-Berechnung
- [ ] Sortierung
- [ ] Ausgabe-Formatierung

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

---

## 8. Zukünftige Erweiterung: Geldberechnung

> **Hinweis:** Diese Funktion ist aktuell NICHT implementiert. Dokumentiert für zukünftige Erweiterungen.

Falls später Zuschussbeträge berechnet werden sollen, können folgende Spalten ergänzt werden:

### Zusätzliche RULES-Spalten

| Spalte | Feld | Typ | Beispiel |
|--------|------|-----|----------|
| Y | FOERDER_TYP_TN | Dropdown | `TAG` / `KOPF` / `PAUSCHAL` |
| Z | FOERDER_TYP_MA | Dropdown | `TAG` / `KOPF` / `PAUSCHAL` |
| AA | SATZ_TN | Zahl | `5` (€ pro Tag/Kopf) |
| AB | SATZ_MA | Zahl | `30` (€ pro Tag/Kopf) |

### Bedeutung

| FOERDER_TYP | Berechnung |
|-------------|------------|
| `TAG` | Anzahl × Tage × Tagessatz |
| `KOPF` | Anzahl × Kopfpauschale |
| `PAUSCHAL` | Fester Betrag |

### Beispiel

| Einstellung | Berechnung |
|-------------|------------|
| FOERDER_TYP_TN=TAG, SATZ_TN=5€ | 20 TN × 3 Tage × 5€ = 300€ |
| FOERDER_TYP_MA=PAUSCHAL, SATZ_MA=50€ | 50€ |
| **Gesamt** | **350€** |

---

## 9. Named Function API: ZUSCHUSS_ENGINE

### 9.1 Konzept

Eine zentrale **Named Function** ersetzt alle regionsspezifischen V6-Formeln. Änderungen an der Logik wirken sofort in allen 20+ Blättern.

```
┌─────────────────────────────────────┐
│         ZUSCHUSS_ENGINE             │
│    (Single Source of Truth)         │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┬──────────────┐
    ▼          ▼          ▼              ▼
  RLK        NRW     Westerwaldkreis   [...]
```

### 9.2 Architektur: Hybride Lösung

**Eine Hauptfunktion** mit internen `LAMBDA`-Modulen:

| Aspekt | Lösung |
|--------|--------|
| Deployment | 1× `ZUSCHUSS_ENGINE` registrieren |
| Modularität | Interne LAMBDAs für Filter, Quote, Sort |
| Debugging | Optional: `ZE_DEBUG` als zweite Funktion |

### 9.3 Funktionssignatur

| Feld | Wert |
|------|------|
| **Name** | `ZUSCHUSS_ENGINE` |
| **Registrierung** | `Daten` → `Benannte Funktionen` → `Neue Funktion hinzufügen` |

#### Parameter

| # | Name | Typ | Pflicht | Beispiel |
|---|------|-----|---------|----------|
| 1 | `tn_range` | Range | ✅ | `TN_LISTE!B3:AP1710` |
| 2 | `setup_key` | Text | ✅ | `SETUP!B18` |
| 3 | `target_lk` | Text | ✅ | `SETUP!B16` |
| 4 | `event_start` | Datum | ✅ | `SETUP!B23` |
| 5 | `event_end` | Datum | ⬜ | `SETUP!H23` |
| 6 | `zone` | Zahl | ⬜ | `1` |
| 7 | `debug` | Bool | ⬜ | `FALSCH` |

### 9.4 Aufruf-Beispiele

```excel
/* Minimal */
=ZUSCHUSS_ENGINE(TN_LISTE!B3:AP1710; SETUP!B18; SETUP!B16; SETUP!B23)

/* Mit Paginierung (Zone 2) */
=ZUSCHUSS_ENGINE(TN_LISTE!B3:AP1710; SETUP!B18; SETUP!B16; SETUP!B23; SETUP!H23; 2)

/* Debug-Modus */
=ZUSCHUSS_ENGINE(TN_LISTE!B3:AP1710; SETUP!B18; SETUP!B16; SETUP!B23; ; ; WAHR)
```

### 9.5 Interne Module (als LAMBDA)

```excel
=LET(
  /* ═══ INTERNE MODULE ═══ */
  _load_rules; LAMBDA(key; 
    SVERWEIS(key; CACHE_RULES!A:X; SEQUENZ(1;24;1); 0)
  );
  
  _filter_base; LAMBDA(data; rules;
    LET(
      status_filter; INDEX(rules; 22);
      target_groups; INDEX(rules; 13);
      FILTER(data; 
        (INDEX(data;;1) = status_filter) *
        (ISTFEHLER(SUCHEN(INDEX(data;;2); target_groups)) = FALSCH)
      )
    )
  );
  
  _calc_quote; LAMBDA(data; rules; target_lk;
    LET(
      quote_bezug; INDEX(rules; 15);
      min_quote; INDEX(rules; 10);
      quote_modus; INDEX(rules; 11);
      relevant; FILTER(data; ISTFEHLER(SUCHEN(INDEX(data;;2); quote_bezug)) = FALSCH);
      lokale; SUMMENPRODUKT((INDEX(relevant;;41) = target_lk) * 1);
      gesamt; ZEILEN(relevant);
      quote_pct; WENN(gesamt = 0; 0; lokale / gesamt * 100);
      is_fulfilled; WENN(quote_modus = "MEHRHEIT"; lokale > gesamt - lokale; quote_pct >= min_quote);
      HSTACK(quote_pct; is_fulfilled)
    )
  );
  
  _filter_wohnort; LAMBDA(data; rules; target_lk; use_all;
    LET(
      tg_local_only; INDEX(rules; 14);
      FILTER(data;
        (use_all = WAHR) +
        (ISTFEHLER(SUCHEN(INDEX(data;;2); tg_local_only))) +
        (INDEX(data;;41) = target_lk)
      )
    )
  );
  
  _sort; LAMBDA(data; rules; target_lk;
    LET(
      sort_order; INDEX(rules; 19);
      is_lokal; MAP(INDEX(data;;41); LAMBDA(lk; WENN(lk = target_lk; 0; 1)));
      WENN(ISTFEHLER(SUCHEN("LOKAL_FIRST"; sort_order));
        SORT(data; 13; 1);
        SORT(HSTACK(is_lokal; data); 1; 1; 14; 1)
      )
    )
  );

  /* ═══ REGELN LADEN ═══ */
  rules; _load_rules(setup_key);
  quote_aktion; INDEX(rules; 12);
  
  /* ═══ FILTER-KETTE ═══ */
  step1; _filter_base(tn_range; rules);
  quote_result; _calc_quote(step1; rules; target_lk);
  use_all; ODER(quote_aktion = "ALLE_IMMER"; 
               UND(quote_aktion = "ALLE_WENN_ERFUELLT"; INDEX(quote_result; 2)));
  step2; _filter_wohnort(step1; rules; target_lk; use_all);
  step3; _sort(step2; rules; target_lk);
  
  /* ═══ OUTPUT ═══ */
  WENN(debug;
    "Key: " & setup_key & " | Quote: " & RUNDEN(INDEX(quote_result;1);1) & "% | UseAll: " & use_all;
    step3
  )
)
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

### 9.7 Migration V6 → V7

| Schritt | Aktion |
|---------|--------|
| 1 | Named Function registrieren |
| 2 | CACHE_RULES auf 24 Spalten erweitern |
| 3 | Alte V6-Formeln durch `=ZUSCHUSS_ENGINE(...)` ersetzen |

### 9.8 Umsetzungs-Checkliste (Ergänzung zu Phase 4)

- [ ] Named Function `ZUSCHUSS_ENGINE` registrieren
- [ ] Optional: `ZE_DEBUG` für Entwicklung
- [ ] Alle Zielblätter auf neuen Aufruf umstellen
- [ ] V6-Formeln archivieren

