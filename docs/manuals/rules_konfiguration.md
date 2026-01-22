# RULES-Konfiguration: Benutzerhandbuch

Dieses Handbuch erklärt alle Felder im RULES-Tabellenblatt und wie sie zusammenwirken, um die Zuschussliste zu generieren.

---

## Übersicht: Spaltenstruktur

| Spalte | Feld | Typ | Beschreibung |
|--------|------|-----|--------------|
| A | KEY | Text | Eindeutiger Schlüssel (automatisch aus B+C) |
| B | Landkreis | Text | Ziel-Landkreis für die Förderung |
| C | Event-Typ | Text | Art der Veranstaltung |
| D | Kürzel | Text | Kurzbezeichnung |
| **E** | **Förderumfang** | Code | Wer wird gefördert? |
| **F** | **MIN_TN** | Zahl | Mindestanzahl Teilnehmer |
| **G** | **MIN_ALTER** | Zahl | Hartes Mindestalter (TN) |
| **H** | **MAX_ALTER** | Zahl | Höchstalter (TN) |
| **I** | **MIN_ALTER_SOFT** | Zahl | Weiches Mindestalter (Toleranz) |
| **J** | **MIN_TAGE** | Zahl | Mindest-Veranstaltungstage |
| **K** | **Quote (%)** | Zahl | Mindestanteil lokaler TN |
| **L** | **QUOTE_MODUS** | Text | Art der Quote-Berechnung |
| **M** | **Logik** | Text | Förderlogik bei erfüllter Quote |
| N | Hinweise | Text | Optionale Anmerkungen |

---

## Feld-Definitionen

### E: Förderumfang (12 Codes)

Der Förderumfang definiert, **welche Personengruppen** grundsätzlich förderfähig sind.

| Code | TN | MA | REF | Beschreibung |
|------|:--:|:--:|:---:|--------------| 
| `TN_K` | K | — | — | Nur lokale TN |
| `TN_K_MA_K` | K | K | — | Lokale TN + lokale MA |
| `TN_K_MA_P` | K | P | — | Lokale TN + alle MA |
| `TN_P` | P | — | — | Alle TN |
| `TN_P_MA_K` | P | K | — | Alle TN + lokale MA |
| `TN_P_MA_P` | P | P | — | Alle TN + alle MA |
| `MA_K` | — | K | — | Nur lokale MA |
| `MA_P` | — | P | — | Alle MA |
| `TN_K_REF` | K | — | P | Lokale TN + alle REF |
| `TN_K_MA_K_REF` | K | K | P | Lokale TN + MA + alle REF |
| `TN_P_MA_P_REF` | P | P | P | Alle TN + MA + REF |
| `REF` | — | — | P | Nur alle REF |

**Legende:**
- **K** = Nur Personen aus dem Ziel-Landkreis/Bundesland
- **P** = Alle Personen (Pauschal)
- **—** = Diese Rolle ist nicht aktiv

> [!NOTE]
> **REF ist immer pauschal.** Wenn REF aktiv ist (`_REF` Suffix), werden alle Referenten einbezogen.

> **Wichtig:** Bei TN mit "Kreis"-Regel wirken zusätzlich Quote und Logik!


---

### F: MIN_TN (Mindestanzahl Teilnehmer)

Die Mindestanzahl der Teilnehmer, die nach allen Filtern übrig bleiben müssen, damit eine Förderung erfolgt.

| Wert | Bedeutung |
|------|-----------|
| `0` oder leer | Keine Mindestanzahl |
| `5` | Mindestens 5 förderfähige Personen |
| `10` | Mindestens 10 förderfähige Personen |

**Fehlermeldung bei Unterschreitung:**
> ⚠️ Min TN (5) nicht erreicht. Aktuell: 3

---

### G: MIN_ALTER (Hartes Mindestalter)

Das **absolute** Mindestalter für Teilnehmer. Wird im Prüfungen-Dashboard zur Warnung verwendet.

| Wert | Bedeutung |
|------|-----------|
| `0` oder leer | Kein Mindestalter |
| `7` | Mindestalter 7 Jahre |

> **Hinweis:** Dieser Wert dient als Referenz. Der tatsächliche Filter verwendet `MIN_ALTER_SOFT`.

---

### H: MAX_ALTER (Höchstalter)

Das Höchstalter für Teilnehmer.

| Wert | Bedeutung |
|------|-----------|
| `999` oder leer | Kein Höchstalter |
| `27` | Höchstalter 27 Jahre |

> **Wichtig:** Der Altersfilter gilt **nur für TN**, nicht für MA!

---

### I: MIN_ALTER_SOFT (Weiches Mindestalter)

Das **tolerierte** Mindestalter für den Filter. Ermöglicht eine "weiche" Grenze.

| Beispiel | MIN_ALTER | MIN_ALTER_SOFT | Effekt |
|----------|-----------|----------------|--------|
| Strikt | 7 | 7 | Nur ab 7 Jahren |
| Tolerant | 7 | 6 | Ab 6 Jahren (6-Jährige werden mitgezählt) |

**Anwendungsfall:**
Ein Landkreis fördert offiziell ab 7 Jahren, toleriert aber 6-Jährige. Setze:
- MIN_ALTER = 7 (für Dokumentation/Warnungen)
- MIN_ALTER_SOFT = 6 (für den Filter)

> **Wichtig:** MIN_ALTER_SOFT beeinflusst die Quote-Berechnung! Siehe "Wechselwirkungen".

---

### J: MIN_TAGE (Mindest-Veranstaltungstage)

Die Mindestdauer der Veranstaltung in Tagen.

| Wert | Bedeutung |
|------|-----------|
| `0` oder leer | Keine Mindestdauer |
| `3` | Mindestens 3 Tage (inkl. An- und Abreisetag) |

**Berechnung:**
```
Veranstaltungstage = Enddatum - Startdatum + 1
```

**Fehlermeldung bei Unterschreitung:**
> ⚠️ Mindestdauer (3 Tage) nicht erreicht. Aktuell: 2

---

### K: Quote (%)

Der Mindestanteil lokaler Teilnehmer an der Gesamtzahl der TN.

| Wert | Bedeutung |
|------|-----------|
| `0` | **Keine Quote-Prüfung** (immer erfüllt) |
| `51` | Mindestens 51% lokale TN |
| `0.51` | Auch als Dezimalzahl möglich |

> [!TIP]
> Setze **Quote = 0**, um die Quote-Prüfung komplett zu deaktivieren.  
> Dies funktioniert sowohl mit PROZENT als auch mit MEHRHEIT.

> **Wichtig:** Die Quote wird **nach** dem Altersfilter berechnet!

---

### L: QUOTE_MODUS (Art der Quote-Berechnung)

Definiert, **wie** die Quote geprüft wird.

| Wert | Berechnung | Beschreibung |
|------|------------|--------------|
| `PROZENT` | `lokale_TN / gesamt_TN >= Quote` | Prozentualer Anteil |
| `MEHRHEIT` | `lokale_TN > auswärtige_TN` | Absolute Mehrheit |

**Beispiel mit 30 TN (18 lokal, 12 auswärtig):**

| Modus | Prüfung | Ergebnis |
|-------|---------|----------|
| PROZENT (51%) | 18/30 = 60% >= 51% | ✅ Erfüllt |
| MEHRHEIT | 18 > 12 | ✅ Erfüllt |

**Beispiel mit 30 TN (14 lokal, 16 auswärtig):**

| Modus | Prüfung | Ergebnis |
|-------|---------|----------|
| PROZENT (51%) | 14/30 = 47% < 51% | ❌ Nicht erfüllt |
| MEHRHEIT | 14 < 16 | ❌ Nicht erfüllt |

---

### M: Logik (Förderlogik)

Definiert, **wer gefördert wird**, wenn die Quote erfüllt ist.

| Wert | Bei Quote erfüllt | Bei Quote nicht erfüllt |
|------|-------------------|------------------------|
| `Standard` | Nur lokale TN + lokale MA | Nur lokale TN + lokale MA |
| `Auffüllen` | **Alle TN + alle MA** | Nur lokale TN + lokale MA |

> [!IMPORTANT]
> **"Auffüllen" wirkt auf BEIDE Gruppen (TN und MA)!**
> Bei erfüllter Quote werden sowohl alle TN als auch alle MA gefördert.

**Anwendungsfall "Auffüllen":**
Ein Landkreis sagt: "Wenn mehr als die Hälfte unserer Leute sind, bezahlen wir auch die Auswärtigen mit – für Teilnehmer UND Mitarbeiter."

---

## Wechselwirkungen

### Regelkette (Verarbeitungsreihenfolge)

```
1. ALTERSFILTER
   └── TN werden nach MIN_ALTER_SOFT / MAX_ALTER gefiltert
   
2. QUOTE-BERECHNUNG
   └── Basierend auf den gefilterten TN
   
3. LOGIK-ANWENDUNG (vereinheitlicht für TN und MA)
   └── Standard: Nur lokale TN + lokale MA
   └── Auffüllen + Quote erfüllt: Alle TN + alle MA
   └── Auffüllen + Quote nicht erfüllt: Nur lokale TN + lokale MA
   
4. FÖRDERUMFANG
   └── Definiert, welche Gruppen aktiv sind (TN, MA, oder beide)
```

> [!NOTE]
> Die Suffix-Codes `_K` und `_P` im Förderumfang definieren nur, welche Gruppen **aktiv** sind.
> Die eigentliche Unterscheidung lokal/alle wird durch die **Logik** gesteuert.

### Kritischer Fall: Altersfilter kippt Quote

**Szenario:**
- 30 lokale TN (davon 5 sind 5-Jährige)
- 28 auswärtige TN (alle 7+ Jahre)

**Bei MIN_ALTER_SOFT = 5:**
- Lokale TN: 30
- Auswärtige TN: 28
- Quote (MEHRHEIT): 30 > 28 → ✅ Erfüllt
- Mit "Auffüllen": **58 TN** werden gefördert

**Bei MIN_ALTER_SOFT = 6:**
- Lokale TN: 25 (5 fallen raus)
- Auswärtige TN: 28
- Quote (MEHRHEIT): 25 < 28 → ❌ Nicht erfüllt
- Nur lokale: **25 TN** werden gefördert

> **Fazit:** Eine kleine Änderung am Altersfilter kann die Quote kippen und das Ergebnis drastisch ändern!

---

## Beispielkonfigurationen

### Jugendfreizeit (Standard RLP)

| Feld | Wert | Begründung |
|------|------|------------|
| Förderumfang | `TN_K_MA_K` | TN + MA aktiv |
| MIN_TN | `5` | Mindestens 5 Teilnehmer |
| MIN_ALTER | `7` | Offiziell ab 7 Jahren |
| MAX_ALTER | `27` | Bis 27 Jahre |
| MIN_ALTER_SOFT | `6` | 6-Jährige toleriert |
| MIN_TAGE | `3` | Mindestens 3 Tage |
| Quote | `51` | Mehrheit lokal |
| QUOTE_MODUS | `PROZENT` | Prozentuale Berechnung |
| Logik | `Auffüllen` | Bei erfüllter Quote: alle TN + alle MA |

### Schulung (keine Altersbeschränkung)

| Feld | Wert | Begründung |
|------|------|------------|
| Förderumfang | `TN_K_MA_K` | TN + MA aktiv |
| MIN_TN | `3` | Mindestens 3 Teilnehmer |
| MIN_ALTER | `0` | Kein Mindestalter |
| MAX_ALTER | `999` | Kein Höchstalter |
| MIN_ALTER_SOFT | `0` | Kein Filter |
| MIN_TAGE | `1` | Auch Tagesveranstaltungen |
| Quote | `0` | Keine Quote-Prüfung |
| QUOTE_MODUS | `MEHRHEIT` | Irrelevant bei Quote=0 |
| Logik | `Standard` | Nur lokale TN + lokale MA |

### Offene Veranstaltung (alle Personen)

| Feld | Wert | Begründung |
|------|------|------------|
| Förderumfang | `TN_P_MA_P` | TN + MA aktiv |
| MIN_TN | `1` | Mindestens 1 Person |
| MIN_ALTER | `0` | Kein Mindestalter |
| MAX_ALTER | `999` | Kein Höchstalter |
| MIN_ALTER_SOFT | `0` | Kein Filter |
| MIN_TAGE | `0` | Keine Mindestdauer |
| Quote | `0` | Keine Quote-Prüfung |
| QUOTE_MODUS | `MEHRHEIT` | Irrelevant bei Quote=0 |
| Logik | `Auffüllen` | Alle TN + alle MA |

---

## Testergebnisse (Verifiziert)

Die folgenden Tests wurden mit realen Daten durchgeführt:

### Test-Datenbasis

| Gruppe | Lokal (Rhein-Lahn-Kreis) | Auswärtig | Gesamt |
|--------|--------------------------|-----------|--------|
| TN | ~26-30 | ~25 | ~51-55 |
| MA | 4 | 4 | 8 |

### Testszenarien

| # | MIN_ALTER_SOFT | Quote | QUOTE_MODUS | Logik | Ergebnis | Erklärung |
|---|----------------|-------|-------------|-------|----------|-----------|
| 1 | 5 | 0% | MEHRHEIT | Auffüllen | **59** | Quote=0 → immer erfüllt → alle |
| 2 | 6 | 0% | MEHRHEIT | Auffüllen | **59** | Quote=0 → immer erfüllt → alle |
| 3 | 6 | 51% | MEHRHEIT | Auffüllen | **29** | Quote nicht erfüllt → nur Lokale |
| 4 | 12 | 0% | PROZENT | Auffüllen | **54** | Alle, aber nur Alter 12+ |
| 5 | 0 | 0% | MEHRHEIT | Standard | **29** | Standard → immer nur Lokale |

### Wichtige Erkenntnisse

1. **Quote = 0** deaktiviert die Quote-Prüfung komplett (sowohl PROZENT als auch MEHRHEIT)
2. **Auffüllen** wirkt auf **TN und MA** einheitlich
3. **Der Altersfilter beeinflusst die Quote-Berechnung** – kleine Änderungen können große Auswirkungen haben
4. **Gruppierte Sortierung** funktioniert: Lokale zuerst, dann Auswärtige (alphabetisch)

---

## Fehlermeldungen

| Meldung | Ursache | Lösung |
|---------|---------|--------|
| ❌ Key: 'XYZ' nicht gefunden | Rule-Key existiert nicht in CACHE_RULES | KEY in RULES prüfen |
| ⚠️ Keine passenden Teilnehmer | Keine angemeldeten TN mit gültigem Landkreis | TN_LISTE prüfen |
| ⚠️ Mindestdauer nicht erreicht | Veranstaltung zu kurz | Datum in SETUP oder MIN_TAGE prüfen |
| ⚠️ Min TN nicht erreicht | Zu wenige förderfähige Personen | Daten oder MIN_TN prüfen |
| ⚠️ Keine Personen nach Filter | Alle durch Filter ausgeschlossen | Alters-/Förderumfang-Einstellungen prüfen |

---

## Glossar

| Begriff | Definition |
|---------|------------|
| **Lokal** | Person aus dem Ziel-Landkreis/Bundesland |
| **Auswärtig** | Person aus einem anderen Landkreis/Bundesland |
| **TN** | Teilnehmer (unterliegt Altersfilter) |
| **MA** | Mitarbeitende (kein Altersfilter) |
| **REF** | Referent:in (kein Altersfilter, immer pauschal) |
| **Quote** | Verhältnis lokaler zu gesamten TN |
| **Auffüllen** | Bei erfüllter Quote werden auch Auswärtige gefördert |

