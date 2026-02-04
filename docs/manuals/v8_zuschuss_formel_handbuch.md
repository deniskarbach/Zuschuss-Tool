# 📘 V8 Zuschuss-System: Technisches Handbuch (Version 8)

*Version: 8.1.0*
*Datum: 04.02.2026*

---

## 1. Einführung und Funktionsweise

Die "V8"-Formel ist ein vollständig konfigurierbares, regelbasiertes System zur automatisierten Berechnung von Zuschusslisten für Jugendfreizeiten. Sie arbeitet nach dem Prinzip der **dynamischen Regel-Injektion**: Die Logik ist in einer einzigen Formel gekapselt, während die Parameter (Regeln) extern im Blatt `RULES` (technisch `CACHE_RULES`) verwaltet werden.

### Der Prozess im Überblick
1.  **Datenerfassung:** Die Formel liest die Rohdaten aus dem Blatt `TN_LISTE` (Zeile 2 bis Ende).
2.  **Kontext-Bestimmung:** Anhand von `SETUP!B18` (Veranstaltungstyp, z.B. "Freizeit") und dem voreingestellten Landkreis wird der korrekte Datensatz aus `CACHE_RULES` geladen.
3.  **Filterung (Individuell):** Jeder Datensatz wird gegen definierte Kriterien (Alter, Status, Dauer) geprüft.
4.  **Logik-Prüfung (Gruppe):** Die verbleibende Menge wird gegen Gruppenkriterien geprüft (Mindestteilnehmerzahl, Quote).
5.  **Output-Generierung:** Die qualifizierten Datensätze werden sortiert, formatiert und ausgegeben.

---

## 2. Detaillierte Parameter-Dokumentation (RULES)

Das Blatt `RULES` (bzw. `CACHE_RULES`) steuert das Verhalten der Formel. Die Konfiguration erfolgt spaltenweise von B bis W.

### 2.1 Master-Tabelle (Spalten-Übersicht)

| Spalte | Parameter | Datentyp | Beschreibung |
| :--- | :--- | :--- | :--- |
| **B** | `KEY` | Text | Eindeutiger Identifikator des Regelsatzes (z.B. `Main-Taunus-Kreis_Freizeit`). Wird aus `Gebietskörperschaft` + `TYP` gebildet. |
| **C** | `Gebietskörperschaft` | Text | Name des Landkreises oder der Stadt (muss exakt mit Dropdown übereinstimmen). |
| **D** | `TYP` | Text | Veranstaltungstyp (z.B. `Freizeit`, `Schulung`, `Seminar`). |
| **E** | `KUERZEL` | Text | Internes Kürzel (optional, für Berichte). |
| **F** | `MIN_ANZAHL` | Ganzzahl | **Mindestanzahl Personen.** Unterschreitung sperrt die Liste. |
| **G** | `MIN_ANZAHL_BEZUG` | Text | Wer zählt zur Mindestanzahl? (`TN`, `MA`, `LEITUNG` oder `ALLE`). Default: `TN`. |
| **H** | `MIN_TAGE` | Ganzzahl | **Mindestdauer der Maßnahme.** Vergleicht `(Ende - Start + 1)` mit diesem Wert. |
| **I** | `MIN_ANWESENHEIT` | Ganzzahl | **Mindestanwesenheit pro Person.** Personen mit weniger Tagen werden gefiltert. |
| **J** | `MIN_ALTER_TN` | Ganzzahl | **Reguläres Mindestalter TN.** (Harte Grenze, wenn kein Soft-Wert gesetzt). |
| **K** | `MAX_ALTER_TN` | Ganzzahl | **Höchstalter TN.** (`0` = inaktiv). |
| **L** | `MIN_ALTER_SOFT_TN` | Ganzzahl | **Weiches Mindestalter TN.** Wenn gesetzt (`>0`), überschreibt dies `MIN_ALTER_TN`. |
| **M** | `MIN_ALTER_MA` | Ganzzahl | **Mindestalter Mitarbeiter (MA).** |
| **N** | `MIN_ALTER_LEITUNG` | Ganzzahl | **Mindestalter Leitung.** Prioritär vor `MIN_ALTER_MA`. |
| **O** | `TARGET_GROUPS` | Text | **Positiv-Liste.** Welche Funktionen werden betrachtet? (z.B. `TN;MA;LEITUNG`). |
| **P** | `GRUPPEN_NUR_LOKAL` | Text | Welche Gruppen müssen **zwingend** aus dem Landkreis kommen? (z.B. `TN`). |
| **Q** | `MIN_QUOTE` | Dezimal | **Quote.** Anteil Einheimische (z.B. `0,5` für 50%). |
| **R** | `QUOTE_MODUS` | Text | Modus: `PROZENT` oder `MEHRHEIT`. |
| **S** | `QUOTE_BEZUG` | Text | Wer zählt in die Quote? (z.B. `TN`). Wichtig! |
| **T** | `QUOTE_AKTION` | Text | Konsequenz bei Nichterfüllung: `KEINE_QUOTE`, `SOLIDARISCH`, `STRIKT_LOKAL`. |
| **U** | `OUTPUT_COLUMNS` | Text | Semikolon-Liste der Ausgabespalten (z.B. `Name;Vorname;Geburtsdatum`). |
| **V** | `LABEL_MAP` | Text | Mapping für Header-Umbenennung (z.B. `Name:Nachname|Geburtsdatum:Geburtsjahr`). |
| **W** | `SORT_ORDER` | Text | Sortierung (z.B. `LOKAL_FIRST;ALPHA`). |
| **X** | `DISPLAY_MODE` | Text | Anzeigemodus: `FILTERED` (nur Förderfähige) oder `SHOW_ALL` (alle Angemeldeten). |

---

### 2.2 Altersgrenzen und Override-Logik (Spalten J-N)

Das System verwendet eine duale Logik aus "Harten" und "Weichen" Grenzen für Teilnehmer (TN).

| Parameter (Spalte) | Beschreibung | Interaktion |
| :--- | :--- | :--- |
| `MIN_ALTER_TN` (J) | **Standard-Mindestalter.** Der reguläre Wert. | Wird **ignoriert**, wenn `MIN_ALTER_SOFT_TN` aktiv ist. |
| `MIN_ALTER_SOFT_TN` (L) | **Ausnahme-Mindestalter.** Ermöglicht jüngeren Teilnehmern den Zugang. | **Priorität:** Wenn Wert > 0, ersetzt er die Spalte J als Untergrenze.<br>*Formel:* `Effektiv = IF(SOFT>0; SOFT; HARD)` |
| `MAX_ALTER_TN` (K) | **Höchstalter.** Älter als dieser Wert = Ausschluss. | Wert `0` deaktiviert die Obergrenze. |

> **Wichtig:** Das Alter wird dynamisch zum **Ende der Maßnahme** (`SETUP!H23`) berechnet: `DATEDIF(Geburtsdatum; Ende; "Y")`.

---

### 2.3 Quoten-Steuerung (Spalten Q-T)

Steuert das Verhältnis von einheimischen zu auswärtigen Teilnehmern.

| Parameter (Spalte) | Beschreibung |
| :--- | :--- |
| `MIN_QUOTE` (Q) | **Schwellenwert.** (Dezimal: 0,5 = 50%). Ignoriert bei `MEHRHEIT`. |
| `QUOTE_MODUS` (R) | `PROZENT` (Anteil >= Quote) oder `MEHRHEIT` (Lokal > Extern). |
| `QUOTE_BEZUG` (S) | **Bezugsgruppe.** (Siehe Warnung unten!). Bestimmt die Basis der Berechnung. |
| `QUOTE_AKTION` (T) | **Konsequenz.** |

#### ⚠️ KRITISCH: Der Parameter `QUOTE_BEZUG` (Spalte S)
Der Parameter `QUOTE_BEZUG` definiert, **welche Funktionen zur Quoten-Berechnung herangezogen werden**.
Z.B. `TN` oder `TN;MA`.
Wenn `QUOTE_BEZUG` auf `--` oder leer gesetzt wird, zählt die Formel **niemanden** zur Quote. Das Ergebnis ist immer `0 von 0 (0%)`.

#### `QUOTE_AKTION` (Spalte T) im Detail
| Wert | Verhalten |
| :--- | :--- |
| **`KEINE_QUOTE`** | Die Quote wird komplett ignoriert. Alle Externen bleiben auf der Liste. |
| **`STRIKT_LOKAL`** | Alle Externen werden **immer** entfernt, egal ob Quote erfüllt oder nicht. |
| **`SOLIDARISCH`** | **Bedingte Filterung:**<br>✅ Quote erfüllt → Externe dürfen bleiben.<br>❌ Quote nicht erfüllt → Alle Externen werden entfernt. |

> [!TIP]
> - `KEINE_QUOTE`: Für Schulungen/Seminare ohne Wohnort-Anforderung.
> - `STRIKT_LOKAL`: Wenn nur Einheimische gefördert werden dürfen.
> - `SOLIDARISCH`: Die faire Option. Externe dürfen mit, solange genug Einheimische dabei sind.

#### Praxisbeispiel: Der "Berliner-Fall"
**Situation:** 4 lokale TN + 1 externer TN (aus Berlin).
| Konfiguration | Ergebnis |
| :--- | :--- |
| `BEZUG=TN`, `MODE=MEHRHEIT`, `ACTION=SOLIDARISCH` | Quote 4 > 1 → ✅ Erfüllt. Berliner **bleibt**. |
| `BEZUG=--`, `MODE=MEHRHEIT`, `ACTION=SOLIDARISCH` | Quote 0 > 0 → ❌ Fail! Berliner **fliegt raus**. |

---

### 2.4 Zielgruppen und Output (Spalten O, P, U-W)

*   **`TARGET_GROUPS` (O):** Nur Personen mit diesen Funktionen werden in die Liste aufgenommen (Filter 1).
*   **`GRUPPEN_NUR_LOKAL` (P):** Personen dieser Funktionen werden entfernt, wenn sie nicht aus dem Landkreis kommen (Filter 2, vor Quote).
*   **`OUTPUT_COLUMNS` (U):** Liste der Spalten (z.B. `Name;PLZ`), die ausgegeben werden.
*   **`LABEL_MAP` (V):** Umbenennung (z.B. `Name:Nachname`).
*   **`SORT_ORDER` (W):** Sortierlogik (z.B. `LOKAL_FIRST;ALPHA`).

---

### 2.5 Anzeigemodus (Spalte X)

Der Parameter `DISPLAY_MODE` steuert ausschließlich die **Darstellung** der berechneten Liste, nicht die Förderfähigkeit der Maßnahme an sich.
> **Wichtig:** Eine ungültige Maßnahme (z.B. zu wenige Teilnehmer) gibt aus Sicherheitsgründen **niemals** eine Liste aus, egal welcher Modus gewählt ist.

| Wert | Beschreibung |
| :--- | :--- |
| **`FILTERED`** (Standard) | Zeigt streng nur die Personen an, die **individuell förderfähig** sind (Alter, Wohnort, Quote erfüllt). |
| **`SHOW_ALL`** | Zeigt **alle gültigen Anmeldungen** der Zielgruppe (Basis-Pool). <br>Dient der Vollständigkeit für die Sachbearbeitung, addiert also auch nicht-förderfähige Personen zur Liste dazu (solange die Maßnahme als Ganzes gültig ist). |

---

### 2.6 Definition: Die "Zielgruppe" (Basis-Pool)
Die "Zielgruppe" (technisch `mask_base_pool`) definiert die Menge an Personen, die für die aktuelle Liste überhaupt in Frage kommen – **noch vor** jeder Prüfung auf Förderfähigkeit (Alter, Wohnort, etc.).
Nur wer zur Zielgruppe gehört, wird im Modus `SHOW_ALL` angezeigt.

Eine Person gehört zur Zielgruppe, wenn sie **alle drei** folgenden Bedingungen erfüllt (UND-Verknüpfung):

1.  **Gültiger Status:** Die Person muss den Status "Angemeldet" haben. (Stornierte oder auf Warteliste befindliche Personen werden sofort ignoriert).
2.  **Dateikompatibilität (`filter_function`):** Die Person muss zur Art der Datei passen.
    *   *Beispiel:* Eine reine Teilnehmer-Liste (`...TN1.txt`) hat intern den Filter auf "TN". Mitarbeiter (MA) gehören hier **nicht** zur Zielgruppe, selbst wenn sie angemeldet sind.
3.  **Regelkonformität (`TARGET_GROUPS`):** Die Funktion der Person muss im Regelsatz (Spalte O) erlaubt sein.
    *   *Beispiel:* Wenn Spalte O nur `TN;MA` enthält, gehören Referenten (`REF`) **nicht** zur Zielgruppe.

> **Zusammengefasst:** Die Zielgruppe ist die Schnittmenge aus **Anmeldung** + **Dateityp** + **Erlaubnis**.

---

## 3. Logik-Ketten im Detail

### 3.1 Die Kaskade der Altersprüfung
Jeder Datensatz durchläuft diese Prüfung:
1.  **Funktion ermitteln:** Ist es TN, MA oder LEITUNG?
2.  **Referenz-Alter wählen:**
    *   Für TN: Prüfe `MIN_ALTER_TN_SOFT`. Ist es gesetzt?
        *   JA: Nutze `SOFT` als Untergrenze.
        *   NEIN: Nutze `MIN_ALTER_TN` als Untergrenze.
    *   Für MA: Nutze `MIN_ALTER_MA`.
3.  **Prüfung:** `Alter >= Untergrenze` UND `Alter <= Obergrenze`.

### 3.2 Die Intelligente Orts-Prüfung ("Local Check")
Die Formel ermittelt automatisch, ob eine Person aus dem Landkreis kommt. Dabei gilt folgende Priorität:
1.  **Zuschuss-Tags (Spalte AS):** Wenn hier ein Wert steht, wird dieser genutzt (für manuelle Zuweisungen bei Stadt/Kreis-Listen).
2.  **Landkreis (Spalte AQ):** Wenn die Tags leer sind, nutzt die Formel den Wert aus dieser Spalte (Fallback).
*Dieses Verfahren garantiert, dass sowohl Datenbank-Imports als auch manuelle Korrekturen korrekt erkannt werden.*

### 3.3 Die Quoten-Logik (Aktions-Matrix)
Wenn die Quote (Prozent oder Mehrheit) **NICHT** erfüllt ist, greift `QUOTE_AKTION`:

1.  **`KEINE_QUOTE`**: Keine Aktion. Die Quote wird ignoriert. Alle externen Teilnehmer verbleiben auf der Liste. (Typisch für Schulungen).
2.  **`STRIKT_LOKAL`**: Harter Filter. Alle Teilnehmer, deren Wohnort nicht dem Landkreis entspricht, werden entfernt. Unabhängig von der Quote.
3.  **`SOLIDARISCH`**: Bedingter Filter.
    *   Ist die Quote erfüllt? → Keine Aktion (Externe dürfen bleiben).
    *   Ist die Quote **nicht** erfüllt? → Alle externen Teilnehmer werden entfernt. Damit verbleiben nur Einheimische, womit die Quote (jetzt 100%) formal erfüllt ist und die Förderung für die Einheimischen gesichert wird.

### 3.4 Die Sortier-Logik
Die Ausgabe wird gesteuert durch `SORT_ORDER` (Spalte W).
*   **Format:** `KEY1;KEY2` (Primär- und Sekundärschlüssel).
*   **Schlüssel `LOKAL_FIRST`:** Sortiert Einheimische nach oben, Externe nach unten.
*   **Schlüssel `ALPHA`:** Sortiert alphabetisch nach Nachnamen.
*   **Schlüssel `FUNKTION_ALPHA`:** Sortiert nach Funktion (TN > LEITUNG > MA > REF), dann alphabetisch.

---

## 4. Fehlersuche (Troubleshooting)

### Fall A: "❌ Maßnahme zu kurz" / "❌ Zu wenige Teilnehmer"
Dies sind **globale Sperren**. Die V8 gibt keine Namensliste aus, um zu verhindern, dass eine ungültige Liste eingereicht wird.
*Lösung:* Prüfen Sie die Dauer in `SETUP` bzw. die Anzahl der *gültigen* Teilnehmer.

### Fall B: "✅ Keine Personen nach aktuellen Kriterien."
Die Filterung war zu strikt – niemand ist übrig geblieben.
In neueren Versionen (ab V8.1) enthält diese Meldung eine Statistik (`Stats -> BasePool | Eligible | Local`), die verrät, an welcher Stelle die Filter greifen.
*   `Local: 0` -> Prüfen Sie die Schreibweise von Landkreis in `SETUP` und `TN_LISTE` (Spalte AQ).

### Fall C: Leere Felder in der Ausgabe
*Ursache:* Die Spaltennamen in der V8-Konfiguration (`OUTPUT_COLUMNS`) stimmen nicht exakt mit den Headern in `TN_LISTE` überein.
*Lösung:* Prüfen Sie auf Tippfehler (z.B. "Straße" vs. "Strasse").
