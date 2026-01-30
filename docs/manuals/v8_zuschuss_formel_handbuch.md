# 📘 V8 Zuschuss-System: Technisches Handbuch (Version 8)

*Version: 8.0.0*
*Datum: 30.01.2026*

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

Das Blatt `RULES` (bzw. `CACHE_RULES`) steuert das Verhalten der Formel. Jede Spalte repräsentiert einen Parameter.

### 2.1 Grundlegende Rahmenbedingungen

| Spalte | Parameter | Datentyp | Beschreibung & Logik |
| :--- | :--- | :--- | :--- |
| **H** | `MIN_ANWESENHEIT` | Ganzzahl | **Mindestanwesenheitstage pro Person.**<br>Vergleicht die Spalte "Anwesenheit" (oder "Tage") der Person mit diesem Wert.<br>*Beispiel:* `3` = Wer nur 2 Tage anwesend war, wird ausgeschlossen. |
| **I** | `MIN_TAGE` | Ganzzahl | **Mindestdauer der Maßnahme.**<br>Vergleicht die berechnete Dauer (`Ende - Start + 1` aus SETUP) mit diesem Wert.<br>*Effekt:* Wird der Wert unterschritten, wird die **gesamte Liste** mit dem Fehler "❌ Maßnahme zu kurz" gesperrt. |
| **G** | `MIN_ANZAHL` | Ganzzahl | **Mindestteilnehmerzahl.**<br>Definiert, wie viele *förderfähige* Personen am Ende übrig bleiben müssen.<br>*Effekt:* Wird die Anzahl unterschritten, wird die gesamte Liste mit "❌ Zu wenige Teilnehmer" gesperrt. |
| **H** | `MIN_ANZAHL_BEZUG` | Text | **Bezugsgruppe für Mindestanzahl.**<br>Definiert, *welche* Personen gezählt werden.<br>*Werte:* `TN` (nur Teilnehmer), `ALLE` (TN + MA).<br>*Standard:* `TN`. |

---

### 2.2 Altersgrenzen und Override-Logik

Das System verwendet eine duale Logik aus "Harten" und "Weichen" Grenzen für Teilnehmer (TN).

| Spalte | Parameter | Beschreibung | Interaktion |
| :--- | :--- | :--- | :--- |
| **J** | `MIN_ALTER_TN` | **Standard-Mindestalter (Hard).**<br>Der reguläre Wert laut Richtlinie.<br>*Beispiel:* `8`. | Wird **ignoriert**, wenn `MIN_ALTER_TN_SOFT` gesetzt ist. |
| **L** | `MIN_ALTER_TN_SOFT` | **Ausnahme-Mindestalter (Soft).**<br>Ermöglicht jüngeren Teilnehmern den Zugang.<br>*Beispiel:* `6`. | **Priorität:** Wenn Wert > 0, ersetzt er `MIN_ALTER_TN` als Untergrenze.<br>*Formel:* `Effektiv = IF(SOFT>0; SOFT; HARD)` |
| **K** | `MAX_ALTER_TN` | **Höchstalter (Hard).**<br>Teilnehmer älter als dieser Wert werden ausgeschlossen.<br>*Beispiel:* `26` (bis vollendetes 26. Lebensjahr). | Wert `0` deaktiviert die Obergrenze. |
| **M** | `MIN_ALTER_MA` | **Mindestalter Mitarbeiter.**<br>Gilt nur für Personen mit Funktion "MA" oder "LEITUNG". | Unabhängig von TN-Regeln. |
| **N** | `MIN_ALTER_LEITUNG` | **Mindestalter Leitung.**<br>Gilt spezifisch für Funktion "LEITUNG". | Wenn gesetzt, überschreibt es `MIN_ALTER_MA` für die Leitung. |

> **Wichtig:** Das Alter wird dynamisch zum **Ende der Maßnahme** (`SETUP!H23`) berechnet: `DATEDIF(Geburtsdatum; Ende; "Y")`.

---

### 2.3 Quoten-Steuerung (Lokal vs. Extern)

Steuert das Verhältnis von einheimischen zu auswärtigen Teilnehmern. **Dieses Modul ist komplex und erfordert sorgfältige Konfiguration.**

| Spalte | Parameter | Beschreibung |
| :--- | :--- | :--- |
| **P** | `MIN_QUOTE` | **Schwellenwert.** (Dezimal: 0,5 = 50%).<br>Wird im Modus `MEHRHEIT` ignoriert. |
| **Q** | `QUOTE_MODE` | **Berechnungsmodus.**<br>`PROZENT`: Prüft `Anteil_Lokal >= MIN_QUOTE`.<br>`MEHRHEIT`: Prüft `Anzahl_Lokal > Anzahl_Extern`. |
| **R** | `QUOTE_BEZUG` | **Bezugsgruppe für die Quote.** (Siehe Warnung unten!) |
| **S** | `QUOTE_ACTION` | **Konsequenz bei Nichterfüllung.** (Siehe Details unten). |

---

#### ⚠️ KRITISCH: Der Parameter `QUOTE_BEZUG`

Der Parameter `QUOTE_BEZUG` definiert, **welche Funktionen zur Quoten-Berechnung herangezogen werden**.

| Wert | Bedeutung | Beispiel-Szenario |
| :--- | :--- | :--- |
| `TN` | Nur Teilnehmer zählen. | "Externe Referenten sollen die Quote nicht beeinflussen." |
| `TN;MA` | Teilnehmer + Mitarbeiter. | "Alle Personen außer REF zählen zur Quote." |
| `--` oder leer | **⛔ FEHLER!** Niemand wird gezählt. | Führt zu Quote 0/0 → Fail! |

> [!CAUTION]
> **Häufiger Konfigurationsfehler:**
> Wenn `QUOTE_BEZUG` auf `--` oder leer gesetzt wird, zählt die Formel **niemanden** zur Quote.
> Das Ergebnis ist immer `0 von 0 (0%)`.
> Bei `QUOTE_MODE=MEHRHEIT` bedeutet das: `0 > 0` ist **FALSCH**.
> Bei `QUOTE_ACTION=SOLIDARISCH` werden dann **alle Externen gefiltert**, obwohl die Quote "eigentlich" erfüllt wäre!
>
> **Lösung:** Setze `QUOTE_BEZUG` immer auf einen gültigen Wert, z.B. `TN`.

---

#### Die Quoten-Berechnung Schritt für Schritt

1.  **Kandidaten filtern:** Die Formel identifiziert alle Personen, die `QUOTE_BEZUG` entsprechen (z.B. alle TN).
2.  **Zählen:**
    *   `cnt_base` = Anzahl aller Kandidaten (Lokal + Extern).
    *   `cnt_local` = Anzahl der Kandidaten aus dem Landkreis.
3.  **Quote prüfen:**
    *   `PROZENT`: `cnt_local / cnt_base >= MIN_QUOTE`?
    *   `MEHRHEIT`: `cnt_local > (cnt_base - cnt_local)`?
4.  **Aktion ausführen:** Basierend auf `QUOTE_ACTION` (siehe unten).

---

#### `QUOTE_ACTION` im Detail

| Wert | Verhalten |
| :--- | :--- |
| **`KEINE_QUOTE`** | Die Quote wird komplett ignoriert. Alle Externen bleiben auf der Liste. |
| **`STRIKT_LOKAL`** | Alle Externen werden **immer** entfernt, egal ob Quote erfüllt oder nicht. |
| **`SOLIDARISCH`** | **Bedingte Filterung:**<br>✅ Quote erfüllt → Externe dürfen bleiben.<br>❌ Quote nicht erfüllt → Alle Externen werden entfernt. |

> [!TIP]
> **Wann nutze ich was?**
> - `KEINE_QUOTE`: Für Schulungen/Seminare ohne Wohnort-Anforderung.
> - `STRIKT_LOKAL`: Wenn nur Einheimische gefördert werden dürfen.
> - `SOLIDARISCH`: Die faire Option. Externe dürfen mit, solange genug Einheimische dabei sind.

---

#### Praxisbeispiel: Der "Berliner-Fall"

**Situation:** 4 lokale TN + 1 externer TN (aus Berlin).

| Konfiguration | Ergebnis |
| :--- | :--- |
| `QUOTE_BEZUG=TN`, `MODE=MEHRHEIT`, `ACTION=SOLIDARISCH` | Quote 4 > 1 → ✅ Erfüllt. Berliner **bleibt**. |
| `QUOTE_BEZUG=--`, `MODE=MEHRHEIT`, `ACTION=SOLIDARISCH` | Quote 0 > 0 → ❌ Fail! Berliner **fliegt raus**. |
| `QUOTE_BEZUG=TN`, `MODE=MEHRHEIT`, `ACTION=STRIKT_LOKAL` | Berliner fliegt **immer** raus (Strikt). |

---

### 2.4 Zielgruppen und Filter

| Spalte | Parameter | Beschreibung |
| :--- | :--- | :--- |
| **O** | `TARGET_GROUPS` | **Positiv-Liste der Funktionen.**<br>Nur Funktionen, die hier gelistet sind (getrennt durch `;`), werden überhaupt betrachtet.<br>*Beispiel:* `TN;MA` (Teilnehmer und Mitarbeiter). |
| **P** | `GRUPPEN_NUR_LOKAL` | **Zwingend Lokale Gruppen.**<br>Funktionen, die hier gelistet sind, MÜSSEN aus dem Landkreis kommen. Externe dieser Gruppe werden sofort gefiltert.<br>*Beispiel:* `TN` (TN müssen lokal sein, MA dürfen extern sein). |

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

### 3.2 Die Quoten-Logik (Aktions-Matrix)
Wenn die Quote (Prozent oder Mehrheit) **NICHT** erfüllt ist, greift `QUOTE_ACTION`:

1.  **`KEINE_QUOTE`**: Keine Aktion. Die Quote wird ignoriert. Alle externen Teilnehmer verbleiben auf der Liste. (Typisch für Schulungen).
2.  **`STRIKT_LOKAL`**: Harter Filter. Alle Teilnehmer, deren Wohnort nicht dem Landkreis entspricht, werden entfernt. Unabhängig von der Quote.
3.  **`SOLIDARISCH`**: Bedingter Filter.
    *   Ist die Quote erfüllt? → Keine Aktion (Externe dürfen bleiben).
    *   Ist die Quote **nicht** erfüllt? → Alle externen Teilnehmer werden entfernt. Damit verbleiben nur Einheimische, womit die Quote (jetzt 100%) formal erfüllt ist und die Förderung für die Einheimischen gesichert wird.

### 3.3 Die Sortier-Logik
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
*Ursache:* Oft falsche Datumsangaben (Freizeit in Vergangenheit/Zukunft) oder zu strenge Altersgrenzen.

### Fall C: Leere Felder in der Ausgabe
*Ursache:* Die Spaltennamen in der V8-Konfiguration (`OUTPUT_COLUMNS`) stimmen nicht exakt mit den Headern in `TN_LISTE` überein.
*Lösung:* Prüfen Sie auf Tippfehler (z.B. "Straße" vs. "Strasse").
