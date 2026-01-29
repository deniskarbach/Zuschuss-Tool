# 📘 V8 Zuschuss-Formel - Das Handbuch

**Stand:** Januar 2026
**Version:** V8 (v1.5 UX Optimiert)

Dieses Dokument beschreibt die Logik, Konfiguration und Wartung der V8-Formel. Es dient dazu, das System auch in Jahren noch verstehen und anpassen zu können.

---

## 1. Philosophie: "Die Formel ist nur der Motor"

Im Gegensatz zu früher (V7 und älter) enthält die V8-Formel **keine landkreisspezifischen Regeln** mehr im Code.
*   **Der Code** ist eine generische Maschine (Engine).
*   **Die Regeln** stehen zu 100% in der Google Tabelle (`RULES` Sheet).
*   **Der Vorteil:** Neue Landkreise oder Regeländerungen erfordern **keinen Codes-Eingriff**. Man ändert nur die Tabelle.

---

## 2. Die Konfiguration (`RULES` Sheet)

Die Formel liest die Konfiguration aus dem Blatt `CACHE_RULES` (oder `RULES`).
**Wichtig:** Die Formel ignoriert Spalte A. Sie beginnt ab **Spalte B** (Index 1).

### Die 22 Säulen der V8 (Spalten-Referenz)

| Excel-Spalte | Index | Parameter | Zweck | Format / Beispiel |
| :--- | :--- | :--- | :--- | :--- |
| **B** | 1 | `KEY` | **Eindeutiger ID**. Verbindet Setup mit Regel. | `Landkreis_EventTyp` (z.B. `Rhein-Lahn-Kreis_Freizeit`) |
| **C-E** | 2-4 | (Meta) | Infos (Landkreisname, Typ, Kürzel). | Rein informativ. |
| **F** | 5 | `MIN_ANZAHL` | Mindestanzahl Köpfe (Hard Stop). | Zahl (z.B. `7`). |
| **G** | 6 | `MIN_ANZAHL_BEZUG` | **Wer zählt?** (Filter vor Quote). | `TN` oder `TN;MA` oder `ALLE`. |
| **H** | 7 | `MIN_TAGE` | Mindestdauer Tage. | Zahl (z.B. `2`). |
| **I** | 8 | `MIN_ANWESENHEIT` | Min. Anwesenheit pro Person. | Zahl (0 = Egal). |
| **J** | 9 | `MIN_ALTER_TN` | Hartes Mindestalter (TN). | Zahl (z.B. `6`). |
| **K** | 10 | `MAX_ALTER_TN` | Hartes Höchstalter (TN). | Zahl (z.B. `27`) oder `0` (keines). |
| **L** | 11 | `MIN_ALTER_SOFT` | Weiches Mindestalter (Regel-Untergrenze). Prioritär genutzt. | Zahl (z.B. `6`). |
| **M** | 12 | `MIN_ALTER_MA` | Mindestalter Mitarbeiter. | Zahl (z.B. `16`). |
| **N** | 13 | `MIN_ALTER_LEITUNG` | Mindestalter Leitung. | Zahl (z.B. `18`). |
| **O** | 14 | `TARGET_GROUPS` | **Wer steht auf der Liste?** (z.B. `TN;MA;LEITUNG`). | Alles andere wird ignoriert. |
| **P** | 15 | `GRUPPEN_NUR_LOKAL` | **Wer MUSS Einheimischer sein?** | `TN` (MA dürfen oft Externe sein). |
| **Q** | 16 | `MIN_QUOTE` | Quoten-Hürde (Prozent/Mehrheit). | `0,5` (für 50%). |
| **R** | 17 | `QUOTE_MODUS` | Wie wird gerechnet? | `PROZENT` oder `MEHRHEIT`. |
| **S** | 18 | `QUOTE_BEZUG` | **Wer zählt in den Nenner?** | `TN` (Quote berechnet sich nur aus TN). |
| **T** | 19 | `QUOTE_AKTION` | **Was passiert bei Quote?** | `SOLIDARISCH`, `STRIKT_LOKAL`, `KEINE_QUOTE`. (Siehe Kap. 3). |
| **U** | 20 | `OUTPUT_COLUMNS` | **Was wird gedruckt?** (Start ab Sp. U!). Template. | `{Nachname}, {Vorname}; {Wohnort}`. |
| **V** | 21 | `LABEL_MAP` | Übersetzer (optional). | `Funktion:PH=MA;Status:Storno=X` |
| **W** | 22 | `SORT_ORDER` | Sortierung. | `ALPHA`, `LOKAL_FIRST;ALPHA`, etc. |

---

## 3. Die Logik der Mindestanzahl

Die V8-Formel unterscheidet präzise zwischen **Listen-Gültigkeit** und **Förderfähigkeit**.

1.  **Filterung:** Zuerst werden Personen gefiltert, die NICHT auf die Liste gehören (Falscher Status, zu Jung als MA, zu Jung als TN).
    *   *Beispiel:* Ein 5-jähriges Kind (bei Mindestalter 6) fliegt raus.
    *   *Beispiel:* Ein 23-jähriger MA (bei Mindestalter 16) bleibt drin.
2.  **Mindestanzahl-Check:** Nun zählt die Formel die verbliebenen Köpfe.
    *   Es zählen nur die Funktionen, die in `MIN_ANZAHL_BEZUG` (Spalte G) stehen.
    *   Steht dort `TN;MA`, zählt der 23-jährige MA mit zur Mindestanzahl.
    *   Wird die Zahl unterschritten -> FEHLER ("Zu wenige Teilnehmer").
3.  **Quoten-Check:** Erst danach prüft die Quote (z.B. Verhältnis Einheimische).

**Wichtig für Admins:**
Stellen Sie sicher, dass in `MIN_ANZAHL_BEZUG` wirklich alle Gruppen stehen, die zur Hürde beitragen sollen. Vergessen Sie "MA" nicht, wenn diese mitzählen dürfen!

---

## 4. Die Logik-Modi (Keywords)

Diese Begriffe steuern das Verhalten. Sie müssen exakt so (in Großbuchstaben) in der Config stehen.

### 4.1 Quoten-Aktionen (`QUOTE_AKTION`)

1.  **`SOLIDARISCH`** (Der Standard)
    *   *Szenario:* "Wir fördern alle, solange genug Einheimische da sind."
    *   *Verhalten:* Wenn Quote erfüllt -> Zeige ALLE (auch Externe). Wenn Quote scheitert -> Zeige nur Einheimische (Rettungsanker).
2.  **`STRIKT_LOKAL`** (Lokal-Fokus)
    *   *Szenario:* "Wir bezahlen nur für unsere eigenen Leute. Quote dient nur der Prüfung."
    *   *Verhalten:* Zeige IMMER nur Einheimische. (Prüfe im Hintergrund trotzdem, ob die Maßnahme gültig ist).
3.  **`KEINE_QUOTE`** (Bedingungslos)
    *   *Szenario:* "Quote ist egal. Alle sind willkommen."
    *   *Verhalten:* Zeige ALLE. Keine Quotenprüfung.

### 4.2 Sortierung (`SORT_ORDER`)

1.  **`ALPHA`** (Nachname A-Z)
2.  **`LOKAL_FIRST;ALPHA`** (Erst Einheimische, dann Externe – jeweils A-Z)
3.  **`FUNKTION_ALPHA`** (Hierarchisch: TN -> LEITUNG -> MA -> REF. Dann A-Z)
4.  **`LANDKREIS_ALPHA`** (Nach Landkreis gruppiert)
5.  **`ALTER`** (Jüngste zuerst)

---

**Entwickler-Hinweis:**
Der Code der V8-Formel ist "Minified" (kommentarfrei) und nutzt verschachtelte IF-Funktionen statt SWITCH, um maximale Kompatibilität mit Google Sheets Arrays zu gewährleisten.
Bitte den Code nicht manuell "verschönern" oder Kommentare (`/*`) einfügen – das zerstört die Formel.
