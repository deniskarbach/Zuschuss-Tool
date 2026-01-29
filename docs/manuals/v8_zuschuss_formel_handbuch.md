# 📘 V8 Zuschuss-Formel - Das Handbuch

**Stand:** Januar 2026
**Version:** V8 (Final Gold Master)

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

### Die 21 Säulen der V8 (Spalten-Referenz)

| Excel-Spalte | Index | Parameter | Zweck | Format / Beispiel |
| :--- | :--- | :--- | :--- | :--- |
| **B** | 1 | `KEY` | **Eindeutiger ID**. Verbindet Setup mit Regel. | `Landkreis_EventTyp` (z.B. `Rhein-Lahn-Kreis_Freizeit`) |
| **C-E** | 2-4 | (Meta) | Infos (Landkreisname, Typ, Kürzel). | Rein informativ. |
| **F** | 5 | `MIN_TN` | Mindestanzahl Teilnehmer. | Zahl (z.B. `7`). |
| **G** | 6 | `MIN_TAGE` | Mindestdauer Tage. | Zahl (z.B. `2`). |
| **H** | 7 | `MIN_ANWESENHEIT` | Min. Anwesenheit pro Person. | Zahl (0 = Egal). |
| **I** | 8 | `MIN_ALTER_TN` | Hartes Mindestalter. | Zahl (z.B. `6`). |
| **J** | 9 | `MAX_ALTER_TN` | Hartes Höchstalter. | Zahl (z.B. `27`) oder `0` (keines). |
| **K** | 10 | `MIN_ALTER_SOFT` | Weiches Mindestalter (Richtwert). | Zahl (z.B. `6`). |
| **L** | 11 | `MIN_ALTER_MA` | Mindestalter Mitarbeiter. | Zahl (z.B. `16`). |
| **M** | 12 | `MIN_ALTER_LEIT` | Mindestalter Leitung. | Zahl (z.B. `18`). |
| **N** | 13 | `TARGET_GROUPS` | **Wer zählt überhaupt?** (Filter). | `TN;MA;LEITUNG` |
| **O** | 14 | `GRUPPEN_NUR_LOKAL` | **Wer MUSS Einheimischer sein?** | `TN` (MA dürfen oft Externe sein). |
| **P** | 15 | `MIN_QUOTE` | Quoten-Hürde (Prozent). | `0,5` (für 50%) oder `0,3`. |
| **Q** | 16 | `QUOTE_MODUS` | Wie wird gerechnet? | `PROZENT` oder `MEHRHEIT`. |
| **R** | 17 | `QUOTE_BEZUG` | **Wer zählt in den Nenner?** | `TN` (Quote berechnet sich nur aus TN). |
| **S** | 18 | `QUOTE_AKTION` | **Was passiert bei Quote?** | `SOLIDARISCH`, `STRIKT_LOKAL`, `KEINE_QUOTE`. (Siehe Kap. 3). |
| **T** | 19 | `OUTPUT_COLUMNS` | **Was wird gedruckt?** (Template). | `{Nachname}, {Vorname}; {Wohnort}`. |
| **U** | 20 | `LABEL_MAP` | Übersetzer (optional). | `Funktion:PH=MA;Status:Storno=X` |
| **V** | 21 | `SORT_ORDER` | Sortierung. | `ALPHA`, `LOKAL_FIRST;ALPHA`, etc. |

---

## 3. Die Logik-Modi (Keywords)

Diese Begriffe steuern das Verhalten. Sie müssen exakt so (in Großbuchstaben) in der Config stehen.

### 3.1 Quoten-Aktionen (`QUOTE_AKTION`)

1.  **`SOLIDARISCH`** (Der Standard)
    *   *Szenario:* "Wir fördern alle, solange genug Einheimische da sind."
    *   *Verhalten:* Wenn Quote erfüllt -> Zeige ALLE (auch Externe). Wenn Quote scheitert -> Zeige nur Einheimische (Rettungsanker).
2.  **`STRIKT_LOKAL`** (Lokal-Fokus)
    *   *Szenario:* "Wir bezahlen nur für unsere eigenen Leute. Quote dient nur der Prüfung."
    *   *Verhalten:* Zeige IMMER nur Einheimische. (Prüfe im Hintergrund trotzdem, ob die Maßnahme gültig ist).
3.  **`KEINE_QUOTE`** (Bedingungslos)
    *   *Szenario:* "Quote ist egal. Alle sind willkommen."
    *   *Verhalten:* Zeige ALLE. Keine Quotenprüfung.

### 3.2 Sortierung (`SORT_ORDER`)

1.  **`ALPHA`** (Nachname A-Z)
2.  **`LOKAL_FIRST;ALPHA`** (Erst Einheimische, dann Externe – jeweils A-Z)
3.  **`FUNKTION_ALPHA`** (Hierarchisch: TN -> LEITUNG -> MA -> REF. Dann A-Z)
4.  **`LANDKREIS_ALPHA`** (Nach Landkreis gruppiert)
5.  **`ALTER`** (Jüngste zuerst)

---

## 4. Output & Formatierung

### Der Template-Motor (`OUTPUT_COLUMNS`)
Sie definieren, welche Spalten die Formel ausspuckt:
`{Vorname} {Nachname}; {Wohnort}; {Geburtsdatum}`

*   **Texte:** `{Vorname} {Nachname}` (z.B. "Max Müller") wird als **Text** ausgegeben.
*   **Werte (Zahlen/Datum):** Wenn eine Spalte NUR aus einem Platzhalter besteht (z.B. `{Geburtsdatum}` oder `{Alter}`), gibt die V8-Formel den **echten Zahlenwert** zurück.
    *   *Vorteil:* Sie können in Google Sheets die Zelle formatieren (als Datum `TT.MM.JJJJ`), und es funktioniert korrekt.

---

## 5. Troubleshooting (Erste Hilfe)

*   **Fehler `#N/A` oder "Rule Key not found":**
    *   Prüfen Sie `SETUP!B18` (Typ) und den Landkreisnamen. Der Key in der Rules-Tabelle muss exakt `Landkreis_Typ` heißen (z.B. `Rhein-Lahn-Kreis_Freizeit`). Leerzeichen beachten!
*   **Fehler "Config fehlt: OUTPUT_COLUMNS":**
    *   Spalte T (Index 19) ist leer. Die Formel weiß nicht, was sie anzeigen soll.
*   **Alle Externe fehlen plötzlich:**
    *   Prüfen Sie `GRUPPEN_NUR_LOKAL`. Steht dort `TN`? Dann werden externe TN hart gefiltert.
    *   Prüfen Sie `QUOTE_AKTION`. Ist sie `STRIKT_LOKAL`? Dann werden Externe nie angezeigt.
    *   Ist die Quote (`MIN_QUOTE`) erreicht? Wenn nicht, und Modus ist `SOLIDARISCH`, fliegen Externe raus.

---

**Entwickler-Hinweis:**
Der Code der V8-Formel ist "Minified" (kommentarfrei) und nutzt verschachtelte IF-Funktionen statt SWITCH, um maximale Kompatibilität mit Google Sheets Arrays zu gewährleisten.
Bitte den Code nicht manuell "verschönern" oder Kommentare (`/*`) einfügen – das zerstört die Formel.
