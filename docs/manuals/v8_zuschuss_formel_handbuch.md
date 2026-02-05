# 📘 V8 Zuschuss-System: Benutzerhandbuch & Technische Referenz

*Version: 8.2.0*
*Datum: 05.02.2026*

---

# Teil 1: Schritt-für-Schritt Anleitung (Für Nutzer)

Diese Anleitung führt Sie durch den Prozess der Erstellung einer Zuschussliste, von der Datenpflege bis zum fertigen PDF.

## Schritt 1: Teilnehmer-Daten pflegen (`TN_LISTE`)
Alle Berechnungen basieren auf der zentralen Liste im Blatt `TN_LISTE`.
1.  Tragen Sie alle Personen (Teilnehmende und Mitarbeitende) in die Liste ein.
2.  **Pflichtfelder:** Stellen Sie sicher, dass folgende Spalten korrekt gefüllt sind:
    *   **Funktion:** `TN`, `MA`, `LEITUNG` oder `REF`.
    *   **Status:** Muss `Angemeldet` sein. (Personen auf "Warteliste" oder "Storniert" werden ignoriert).
    *   **Wohnort & PLZ:** Wichtig für die Orts-Prüfung.
    *   **Landkreis (Spalte AQ):** Muss exakt der offiziellen Schreibweise entsprechen (z.B. "Landkreis Mainz-Bingen").
    *   **Geburtsdatum:** Für die Altersprüfung.
    *   **Anwesenheit:** (Optional) Anzahl der Tage, falls abweichend von der Gesamtdauer.

## Schritt 2: Maßnahme konfigurieren (`SETUP`)
Wechseln Sie in das Blatt `SETUP`. Hier steuern Sie die globale Konfiguration für die aktuelle Freizeit.
1.  **Veranstaltungstyp (B18):** Wählen Sie den Typ (z.B. "Freizeit", "Schulung"). *Dies bestimmt, welche Regeln geladen werden.*
2.  **Zeitraum (B23/H23):** Prüfen Sie Start- und Enddatum. *Dies bestimmt die Dauer und das Stichtags-Alter.*
3.  **Local Mode / Audit Check (B60+):**
    *   Suchen Sie in der Liste ab Zeile 60 Ihren Landkreis.
    *   Standard-Einstellung: `(Leer)` oder `Normal` -> Die Liste wird normal berechnet (gefiltert).
    *   Einstellung `Audit`: Schaltet die Liste in den Prüfmodus (siehe Schritt 4).

## Schritt 3: Liste prüfen (Zuschuss-Blätter)
Gehen Sie in das entsprechende Tabellenblatt für Ihren Zuschuss (z.B. `Mainz-Bingen`, `Hessen`).
*   **Fall A: Die Liste ist gefüllt.**
    *   Prüfen Sie stichprobenartig, ob alle erwarteten Personen enthalten sind.
    *   Achten Sie auf die Sortierung (z.B. Einheimische zuerst).
*   **Fall B: Die Liste ist leer / Fehlermeldung.**
    *   `❌ Maßnahme zu kurz`: Prüfen Sie das Datum im SETUP.
    *   `❌ Zu wenige Teilnehmer`: Es haben sich nicht genug Personen qualifiziert (Mindestanzahl nicht erreicht).

## Schritt 4: Fehlerursachen finden ("Audit Mode")
Fehlt eine Person auf der Liste? Nutzen Sie den integrierten **Audit Mode**:
1.  Gehen Sie zurück ins `SETUP`.
2.  Stellen Sie bei Ihrem Landkreis (Bereich B60:Z100) den Modus auf **`Audit`**.
3.  Wechseln Sie wieder in das Zuschuss-Blatt.
4.  Sie sehen nun eine Tabelle mit **allen** Personen und dem Grund ihres Ausschlusses (z.B. "Alter ungültig", "Nicht Lokal", "Status-Fehler").
5.  Korrigieren Sie die Daten in der `TN_LISTE` und stellen Sie den Modus im `SETUP` zurück auf Leer/Normal.

---

# Teil 2: Technische Dokumentation (V8 Logik)

Die "V8"-Formel ist ein vollständig konfigurierbares, regelbasiertes System ("Dynamische Regel-Injektion"). Die Logik ist in einer einzigen Formel gekapselt, Parameter kommen aus `CACHE_RULES`.

### 2.1 Detaillierte Parameter-Referenz (CACHE_RULES)

Hier finden Sie eine Erklärung zu jeder Spalte im `RULES`-Blatt.

**Spalte B: `KEY` (Regel-Schlüssel)**
Der eindeutige Identifikator für den Datensatz, z.B. `Mainz-Bingen_Freizeit`. Er wird aus `Gebietskörperschaft` und `TYP` zusammengesetzt. Die V8-Formel sucht exakt nach diesem Schlüssel, um ihre Konfiguration zu laden.

**Spalte C: `Gebietskörperschaft`**
Der offizielle Name des Landkreises oder der Stadt (z.B. `Landkreis Mainz-Bingen`). Dieser Wert wird als Standard für die lokale Prüfung verwendet, wenn keine Tags gesetzt sind. Er muss exakt mit der Schreibweise in `TN_LISTE` (Spalte AQ) übereinstimmen.

**Spalte D: `TYP`**
Die Art der Veranstaltung, z.B. `Freizeit`, `Schulung` oder `Seminar`. Dieser Wert wird mit der Auswahl im `SETUP` (Zelle B18) abgeglichen. Nur wenn Typ und Landkreis passen, wird die Regel geladen.

**Spalte F: `MIN_ANZAHL` (Mindest-Teilnehmer)**
Die absolute Untergrenze für die *förderfähige* Gruppengröße (z.B. `7`). Wenn weniger Personen qualifiziert sind als hier angegeben, gibt die Formel den Fehler `❌ Zu wenige Teilnehmer` aus. Sie dient als globale Sperre für ungültige Maßnahmen.

**Spalte G: `MIN_ANZAHL_BEZUG`**
Bestimmt, welche Personengruppen für die Mindestanzahl gezählt werden (z.B. `TN` oder `ALLE`). Standardmäßig zählen nur Teilnehmer (`TN`). Wenn hier `ALLE` steht, zählen auch Mitarbeitende zur Erfüllung der Mindestgröße.

**Spalte H: `MIN_TAGE` (Mindest-Dauer)**
Die erforderliche Mindestdauer der Maßnahme in Tagen (z.B. `3`). Die Formel prüft `(Ende - Start + 1)` gegen diesen Wert. Ist die Maßnahme zu kurz, wird die gesamte Liste mit `❌ Maßnahme zu kurz` gesperrt.

**Spalte I: `MIN_ANWESENHEIT`**
Die Mindestanzahl an Tagen, die eine *einzelne Person* anwesend sein muss, um zu zählen. Wer weniger Tage da war (Spalte "Anwesenheit" oder "Tage" in `TN_LISTE`), wird individuell herausgefiltert. Leere Anwesenheitsfelder werden wie "volle Dauer" behandelt.

**Spalte J: `MIN_ALTER_TN` (Mindestalter TN - Hart)**
Das reguläre Mindestalter für Teilnehmer (z.B. `6`). Dies ist die harte Untergrenze. Teilnehmer, die am Stichtag jünger sind, werden entfernt – es sei denn, Spalte L (`SOFT`) definiert eine Ausnahme.

**Spalte K: `MAX_ALTER_TN` (Höchstalter TN)**
Das maximale Alter für Teilnehmer (z.B. `26`). Wer am Stichtag älter ist, wird aussortiert. Ein Wert von `0` oder Leer bedeutet "kein Höchstalter".

**Spalte L: `MIN_ALTER_SOFT_TN` (Mindestalter TN - Weich)**
Eine optionale, niedrigere Altersgrenze (z.B. `5`), die die harte Grenze (`MIN_ALTER_TN`) überschreibt, falls gesetzt. Dies erlaubt flexible Regeln wie "Eigentlich ab 6, aber ab 5 toleriert". Wenn leer, gilt strikt Spalte J.

**Spalte M: `MIN_ALTER_MA` (Mindestalter Mitarbeiter)**
Das Mindestalter für Personen mit der Funktion `MA`. Mitarbeitende müssen oft älter sein als Teilnehmer (z.B. `16`). Wer jünger ist, wird aus der Mitarbeiter-Liste entfernt.

**Spalte N: `MIN_ALTER_LEITUNG` (Mindestalter Leitung)**
Das spezifische Mindestalter für die Funktion `LEITUNG` (z.B. `18`). Es überschreibt das allgemeine Mitarbeiter-Alter. Eine zu junge Leitung wird nicht als Leitung anerkannt (und fliegt von der Liste).

**Spalte O: `TARGET_GROUPS` (Erlaubte Funktionen)**
Eine Positiv-Liste der Funktionen, die auf dieser Liste erscheinen dürfen (z.B. `TN` oder `TN;MA;LEITUNG`). Wer eine Funktion hat, die hier nicht steht (z.B. `REF`), wird sofort ausgeblendet. Dies trennt z.B. Teilnehmer-Listen von Mitarbeiter-Listen.

**Spalte P: `GRUPPEN_NUR_LOKAL` (Zwingend Lokal)**
Definiert Funktionen, die *zwingend* aus dem eigenen Landkreis kommen müssen, um gefördert zu werden (z.B. `TN`). Auswärtige Personen dieser Gruppe werden individuell gefiltert, noch **bevor** die Quote berechnet wird.

**Spalte Q: `MIN_QUOTE` (Quote)**
Der erforderliche Anteil an Einheimischen als Dezimalzahl (z.B. `0,5` für 50%). Dieser Wert ist die Zielvorgabe. Er interagiert direkt mit `QUOTE_AKTION`: Wird die Quote verfehlt, treten die dort definierten Maßnahmen in Kraft.

**Spalte R: `QUOTE_MODUS`**
Legt die Berechnungsmethode fest: `PROZENT` (Anteil >= Min_Quote) oder `MEHRHEIT` (Einheimische > Auswärtige). "Mehrheit" ist oft strikter als 50%, da bei Gleichstand die Bedingung nicht erfüllt ist.

**Spalte S: `QUOTE_BEZUG` (Basis der Quote)**
Bestimmt, wer in die Quotenberechnung einfließt (z.B. `TN` oder `TN;MA`). Gruppen, die hier nicht genannt sind, sind "neutral" und beeinflussen die Quote nicht. Dies verhindert, dass z.B. viele auswärtige Referenten die Teilnehmer-Quote verfälschen.

**Spalte T: `QUOTE_AKTION` (Konsequenz)**
Regelt das Verhalten bei verfehlter Quote. `KEINE_QUOTE` ignoriert das Ergebnis. `STRIKT_LOKAL` wirft alle Auswärtigen raus. `SOLIDARISCH` wirft Auswärtige nur raus, wenn die Quote *nicht* erfüllt ist – ein fairer Kompromiss.

**Spalte U: `OUTPUT_COLUMNS` (Ausgabe-Spalten)**
Eine Liste der Spalten, die im finalen Tabellenblatt erscheinen sollen (z.B. `Nachname;Vorname;Geburtsdatum`). Sie bestimmt Reihenfolge und Inhalt der PDF-Liste. Namen müssen mit den Headern in `TN_LISTE` übereinstimmen.

**Spalte V: `LABEL_MAP` (Spalten-Umbenennung)**
Erlaubt das Umbenennen von Spalten für den Ausdruck (z.B. `Geburtsdatum=Geburtsjahr`). Das Format ist `Original=Neu`. Nützlich, wenn das Amt andere Begriffe verlangt als die Datenbank (z.B. "Wohnort" statt "Ort").

**Spalte W: `SORT_ORDER` (Sortierung)**
Bestimmt die Reihenfolge der Zeilen (z.B. `LOKAL_FIRST;ALPHA`). `LOKAL_FIRST` stellt Einheimische voran (wichtig für die Prüfung), `ALPHA` sortiert nach Namen. Mehrere Kriterien werden nacheinander angewendet.

**Spalte X: `DISPLAY_MODE` (Anzeige-Modus)**
Schaltet zwischen `FILTERED` (nur Förderfähige zeigen) und `SHOW_ALL` (alle Anmeldungen zeigen) um. `SHOW_ALL` ist für Anwesenheitslisten gedacht, ignoriert aber nicht die globalen Sperren (Min-Anzahl/Dauer).

### 2.2 Die Kaskade der Altersprüfung
Jeder Datensatz durchläuft diese Prüfung:
1.  **Funktion ermitteln:** Ist es TN, MA oder LEITUNG?
2.  **Referenz-Alter wählen:**
    *   Für TN: Ist `MIN_ALTER_TN_SOFT` gesetzt?
        *   JA: Nutze `SOFT` als Untergrenze.
        *   NEIN: Nutze `MIN_ALTER_TN` als Untergrenze.
    *   Für MA: Nutze `MIN_ALTER_MA`.
3.  **Berechnung:** Alter am **letzten Tag** der Maßnahme (`SETUP!H23`).

### 2.3 Die Intelligente Orts-Prüfung ("Local Check")
Die Formel ermittelt automatisch, ob eine Person aus dem Landkreis kommt. Priorität:
1.  **Zuschuss-Tags (Spalte AS):** Manueller Override (z.B. "Mainz-Bingen" eintragen, um Zuweisung zu erzwingen).
2.  **Landkreis (Spalte AQ):** Automatischer Wert aus Datenbank/Import (Fallback).

### 2.4 Quoten-Logik (Aktions-Matrix)
Wenn die Quote nicht erfüllt ist, greift `QUOTE_AKTION`:
*   **`SOLIDARISCH`**: Die faire Option. Solange die Quote erfüllt ist, dürfen Auswärtige bleiben. Wird sie unterschritten, werden Auswärtige entfernt, bis nur noch Einheimische übrig sind (wodurch die Quote formal 100% wird und die Förderung für diese gesichert ist).
*   **`STRIKT_LOKAL`**: Es werden grundsätzlich keine Auswärtigen geduldet.

### 2.5 Audit & Display Mode
*   **DISPLAY_MODE=SHOW_ALL** (in `RULES`): Zeigt pauschal alle angemeldeten Personen der Zielgruppe an. Nützlich für "Anwesenheitslisten", aber nicht für Zuschussanträge.
*   **AUDIT_MODE** (im `SETUP`): Erzeugt einen detaillierten Fehlerbericht statt der normalen Liste. Zeigt pro Person, warum sie abgelehnt wurde (Alter, Wohnort, Dauer etc.).

---

# Teil 3: Troubleshooting

### "❌ Maßnahme zu kurz" / "❌ Zu wenige Teilnehmer"
Dies sind **globale Sperren**. Die V8 gibt keine Namensliste aus, um zu verhindern, dass eine ungültige Liste eingereicht wird.
*Lösung:* Prüfen Sie die Dauer in `SETUP` oder fügen Sie mehr qualifizierte Teilnehmer hinzu.

### "✅ Keine Personen nach aktuellen Kriterien."
Niemand hat die Prüfung bestanden.
*   Prüfen Sie im `SETUP` den **Audit-Modus**, um zu sehen, woran es liegt.
*   Oft ist das Alter der Teilnehmer zu niedrig oder der Landkreis falsch geschrieben.

### Leere Felder in der Ausgabe
Die Spaltennamen in `OUTPUT_COLUMNS` (RULES) stimmen nicht mit `TN_LISTE` überein.
*Lösung:* Tippfehler prüfen (z.B. "Strasse" vs. "Straße").
