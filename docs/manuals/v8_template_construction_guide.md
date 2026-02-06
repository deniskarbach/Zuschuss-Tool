
# Anleitung: Einrichtung `RULES`-Blatt

Diese Anleitung hilft dir, das Blatt `RULES` in der `CVJM_MASTER_DB` benutzerfreundlich und sicher zu gestalten.

## 1. Benutzerführung & Hilfe (Notizen & Eingabehilfe)

Um das Blatt übersichtlich zu halten, nutzen wir keine Kommentare (Thread-Gefahr), sondern **Notizen** (für Spaltentitel) und die **Eingabehilfe** der Datenvalidierung (für die Zellen).

### A. Spalten-Beschreibungen (Notizen)
Rechtsklick auf den Spalten-Buchstaben (z.B. **D**) oder die Kopfzeile (Zelle **D1**) > **Notiz einfügen**.

| Spalte | Titel | Beschreibung für Notiz |
| :--- | :--- | :--- |
| **D** | **Min TN** | Mindestanzahl Teilnehmer, damit der Zuschuss gezahlt wird. |
| **E** | **Min Alter** | Mindestalter für Teilnehmer am Stichtag (Beginn). |
| **F** | **Max Alter** | Höchstalter für Teilnehmer (gilt NICHT für MA/REF). |
| **G** | **Min Tage** | Mindestdauer der Maßnahme in Tagen. |
| **H** | **Quote** | Erforderlicher Anteil an Zielgruppe (z.B. 0,51 für 51%). |

---

### B. Ausfüllhilfe (Eingabehilfe)
Für Spalten mit komplexer Logik nutzen wir die **Eingabehilfe**. Diese erscheint nur, wenn der Nutzer die Zelle anklickt.

**Vorgehen:** *Daten* > *Datenvalidierung* > *Regel bearbeiten/hinzufügen* > *Erweiterte Optionen* > *Hilfetext für eine ausgewählte Zelle anzeigen*.

| Spalte | Titel | Hilfetext für die Datenvalidierung |
| :--- | :--- | :--- |
| **I** | **Logik** | `Standard`: Nur Einheimische zählen. <br>`Auffüllen`: Einheimische "tragen" Externe, solange die Quote (Spalte H) stimmt. |
| **J** | **Förder-Umfang** | `TN`: Nur Kinder. <br>`TN+MA`: Betreuer nur bei gleichem Wohnkreis. <br>`Global`: Betreuer zählen immer (Bypass für Wohnort). |
| **K** | **Hinweis** | Hier kannst du einen Text hinterlegen, der später im Setup-Cockpit als Info/Warnung für diesen Zuschuss erscheint. |

---

## 2. Datenvalidierung (Dropdowns) einrichten

Damit niemand Tippfehler macht (z.B. "Rhein-Lahn" vs "Rhein-Lahn-Kreis"), nutzen wir Dropdowns.

### Schritt A: Die Liste der Landkreise vorbereiten
1.  Gehe in das Blatt **`REF_LISTS`** (falls noch nicht da, erstelle es).
2.  Schreibe in Zelle **A1** die Formel:
    ```excel
    =SORT(UNIQUE(PLZDB!C:C))
    ```
    *Ergebnis:* Eine automatisch sortierte Liste aller Landkreise, die in deiner PLZ-Datenbank vorkommen.

### Schritt B: Das Dropdown im RULES-Blatt erstellen
1.  Gehe in das Blatt **`RULES`**.
2.  Markiere die ganze **Spalte B** (Klick auf den Buchstaben B), oder den Bereich B2:B100.
3.  Gehe im Menü auf **Daten** > **Datenvalidierung**.
4.  Klicke auf **+ Regel hinzufügen**.
5.  Wähle bei "Kriterien": **Dropdown (aus einem Bereich)**.
6.  Klicke auf das Feld für den Bereich und wähle im Blatt `REF_LISTS` die Spalte A aus (`REF_LISTS!A:A`).
7.  Klicke auf **Fertig**.
    *   *Test:* Wenn du jetzt in Spalte B klickst, siehst du alle Landkreise zur Auswahl.

### Schritt C: Manuelle Dropdowns (Art, Logik, Umfang)
Für die anderen Spalten, die feste Optionen haben:

1.  **Markiere Spalte C ("Art")**.
2.  **Daten > Datenvalidierung > Regel hinzufügen**.
3.  Kriterium: **Dropdown**.
4.  Gib die Optionen händisch ein:
    *   `Erholung`
    *   `Bildung`
    *   `Schulung`
    *   `Sonstiges`
5.  Klicke auf **Fertig**.
6.  Wiederhole das für:
    *   **Spalte I ("Logik")**: `Standard`, `Auffüllen`.
    *   **Spalte J ("Förder-Umfang")**: `TN (Standard)`, `TN + MA (Wohnort)`, `TN + MA (Global)`, `Alle (Pauschal)`.

Damit ist dein Blatt robust gegen Tippfehler!

---

## 3. Formate & Validierung für Zahlenwerte

Damit Berechnungen später funktionieren, müssen Zahlen (Min TN, Alter, Tage) und Prozente (Quote) korrekt eingegeben werden.

### A. Ganze Zahlen (Spalten E, F, G, H)
*Betrifft: MIN TN, MIN Alter, MAX Alter, MIN Tage.*

1.  Markiere die entsprechenden Spalten (E bis H).
2.  **Daten > Datenvalidierung > Regel hinzufügen**.
3.  Kriterium: **Größer als oder gleich**.
4.  Wert: `0`.
5.  *Optional:* Aktiviere unter **Erweiterte Optionen** die Option „Eingabe ablehnen“, damit keine Buchstaben eingegeben werden können.

### B. Proportional-Werte / Quote (Spalte I)
*Betrifft: Quote.*

Die Quote wird im Hintergrund als Dezimalzahl (0,51 für 51%) verarbeitet, sollte für den Nutzer aber als Prozent erkennbar sein.

1.  **Formatierung:** Markiere **Spalte I**. Klicke in der Symbolleiste auf das **%**-Symbol.
2.  **Validierung:** 
    *   **Daten > Datenvalidierung > Regel hinzufügen**.
    *   Kriterium: **Zwischen**.
    *   Werte: `0` und `1` (da 100% = 1).
3.  **Hilfetext:** Füge (wie in Section 1B beschrieben) den Hinweis hinzu: *"Bitte als Prozentwert angeben (z.B. 51%)."*

---

## 4. Caching in der Event-Datei (Template)

Um die **Master-DB** zu entlasten, greifen die Formeln in der Event-Datei **nicht direkt** auf sie zu. Stattdessen nutzen wir lokale "Cache-Blätter" im Template.

### Prinzip
`Master-DB` -> *IMPORTRANGE* -> `Event-Template (Cache-Blatt)` -> *VLOOKUP* -> `Event-Logik`

### Schritt A: Cache-Blätter anlegen
Erstelle im Template zwei neue Blätter (du kannst sie später ausblenden):
1.  **`CACHE_RULES`**
2.  **`CACHE_PLZDB`**

### Schritt B: Die Verbindung herstellen
Schreibe in die Zelle **A1** der jeweiligen Cache-Blätter die Import-Formel:

**In `CACHE_RULES` A1:**
```excel
=IMPORTRANGE("URL_DER_MASTER_DB"; "RULES!A:Z")
```

**In `CACHE_PLZDB` A1:**
```excel
=IMPORTRANGE("URL_DER_MASTER_DB"; "PLZDB!A:Z")
```
*(Du musst einmalig auf "Zugriff zulassen" klicken)*

### Schritt C: Lokale Formeln nutzen
Deine Dropdowns und VLOOKUPs im Event-Sheet greifen nun **nur noch auf diese internen Blätter** zu.

*   *Beispiel SVERWEIS:* `=SVERWEIS(B2; CACHE_RULES!A:Z; 4; FALSCH)`
*   *Beispiel Dropdown:* Bereich `CACHE_PLZDB!A:A`

**Vorteil:** Die Event-Datei muss nur 2 Verbindungen aufbauen, egal wie viele Formeln du nutzt.

---

## 5. Best Practice: Der "Setup-Button" für ImportRange

Damit Nutzer die Verbindung einfach genehmigen können, ohne in versteckten Blättern zu suchen, bauen wir einen "Schalter" in das sichtbare `SETUP`-Blatt.

### Das Problem mit WENNFEHLER
Viele verpacken `IMPORTRANGE` in `WENNFEHLER`, um Warnungen auszublenden.
**Gefahr:** Beim ersten Verbinden erzeugt Google einen Fehler (`#REF!`), der den "Zugriff zulassen"-Button enthält. `WENNFEHLER` versteckt diesen Button!

### Die Lösung: Der 2-Stufen-Schalter

1.  Erstelle ein Dropdown (z.B. in Zelle **B10**) mit den Optionen: `🔒 Aus`, `Legitimieren`.
2.  Nutze daneben (z.B. **C10**) diese Formel, die den Inhalt versteckt, aber den **"Zugriff zulassen"-Button** (Fehler) durchlässt:

    ```excel
    =WENN(B10="Legitimieren"; WENN(ISTFEHLER(IMPORTRANGE("URL_DEINER_MASTER_DB"; "MASTER_DB_INFO!A1")); IMPORTRANGE("URL_DEINER_MASTER_DB"; "MASTER_DB_INFO!A1"); "Status: OK"); "🔒 Bitte legitimieren")
    ```

3.  **Status-Anzeige (Optional):**
    Damit der Nutzer direkt sieht, was los ist, kannst du eine Status-Zelle (z.B. **D10**) daneben setzen:

    ```excel
    =WENN(B10="Legitimieren"; WENN(ISTFEHLER(C10); "⚠️ Maus über #REF! halten & klicken"; "✅ Dauerhaft Verbunden"); "")
    ```

4.  **Ablauf für den Nutzer:**
    *   Nutzer stellt Dropdown auf `Legitimieren`.
    *   Import-Zelle zeigt `#REF!`, Status zeigt Warnung.
    *   Nutzer klickt **"Zugriff zulassen"**.
    *   Status springt auf "✅ Dauerhaft Verbunden".
    *   Nutzer kann Dropdown so lassen oder zurückstellen.

---

---

---

## 6. Das Zuschuss-Cockpit: Intelligenz einbauen

Du hast eine Liste von Landkreisen (Spalte A) und möchtest für jeden automatisch wissen: Wie viele sind dabei? Darf ich drucken? Was beachten?
Da sich die Regeln je nach "Art der Maßnahme" (Feld **$B$8**) ändern, nutzen wir dynamische Formeln.

### Spalte "Anzahl" (Zählen)
Zählt, wie viele Personen aus deiner TN-Liste aus diesem Landkreis kommen.
*(Angenommen: In deinem Blatt `TN_LISTE` stehen die Landkreise in Spalte **F**)*.

```excel
=ZÄHLENWENN(TN_LISTE!F:F; A55)
```

### Spalte "Status" (Prüfung)
Prüft, ob die Anzahl ("Anzahl" in B55) für die **aktuell gewählte Maßnahme** ausreicht. Dazu holen wir das "Min TN" aus den Cache-Regeln.

```excel
=WENN( B55 >= SVERWEIS(A55 & "_" & $B$8; CACHE_RULES!A:Z; 4; FALSCH); "✅ Druckbar"; "⚠️ Zu wenig TN" )
```
*(Die `4` steht für die Spalte **Min TN** in der Master-DB).*

### Spalte "Hinweis" (Info)
Zeigt den passenden Hinweistext für diese Kombination (Landkreis + Art).

```excel
=SVERWEIS( A55 & "_" & $B$8 ; CACHE_RULES!A:Z ; 11 ; FALSCH )
```
*(Die `11` steht für die Spalte **Hinweis** in der Master-DB).*

**Ergebnis:** Wählst du oben "Soziale Bildung", aktualisieren sich Status und Hinweise für alle Landkreise sofort automatisch.

---

---

## 7. Daten-Import (Vereinfacht: Die 2-Blatt-Lösung)

Wir reduzieren die Komplexität. Du brauchst nur **1 sichtbares Blatt** für alles.

### Blatt 1: `INPUT_ONLINE` (Der unsichtbare Helfer)
In dieses Blatt kommt nicht einfach nur ein Import, sondern deine intelligente "Schaltzentrale".
Kopiere diese Formel in **Zelle A1**:

```excel
=WENN(SETUP!B37=""; "Keine URL in Tabellenblatt Info Zelle B23 vorhanden"; WENNFEHLER(WENN(Info!B33="Ja"; IMPORTRANGE(Info!B28; "Teilnehmende_Powertag!A1:ZZ200"); WENN(Info!B33="Nein"; "Bitte Daten händisch in Tabellenblatt übertragen..."; "Import muss im Tabellenblatt Info definiert werden")); "Fehler beim Import"))
```

**Was diese Formel tut:**
1.  **Sicherheits-Check:** Prüft, ob überhaupt eine URL im Setup (`SETUP!B37`) steht.
2.  **Schalter ("Ja"/"Nein"):** Prüft das Dropdown (`Info!B33`), ob Daten importiert werden sollen.
3.  **Import:** Nur bei "Ja" werden die Daten gezogen.

**Wichtig:** Nach dem Einfügen Rechtsklick auf den Reiter -> **"Blatt ausblenden"**.

### Blatt 2: `TN_LISTE` (Deine Kommandozentrale)
Dies ist das einzige Blatt, mit dem du arbeitest. Es ist in zwei Zonen geteilt:

**Zone A: Automatisch (Zeile 5 bis 200)**
Hier landen die Online-Daten. Wir verknüpfen direkt und sortieren dabei die Spalten (Normalisierung).

> **Wichtig:** Da wir direkt verknüpfen, sollten eure Online-Formulare immer gleich beginnen (z.B. immer Spalte C=Name, D=Vorname). Das spart Arbeit!

*   **Zelle A5 (Name):** `=WENN(INPUT_ONLINE!C2=""; ""; INPUT_ONLINE!C2)`
*   **Zelle B5 (Vorname):** `=WENN(INPUT_ONLINE!D2=""; ""; INPUT_ONLINE!D2)`

> **Erklärung zur Formel:**
> Das `WENN(... = ""; "")` sorgt für Sauberkeit.
> Ohne diesen Zusatz würde Google Sheets für leere Quell-Zellen oft eine **0** anzeigen. So bleibt die Zelle wirklich leer, bis sich jemand anmeldet.

*   *(Passe C2/D2 an, je nachdem wo Name/Vorname in deinem Formular stehen).*
*   Ziehe die Formeln bis Zeile 200.
*   **Schutz:** Markiere Zeile 5-200 -> Rechtsklick -> "Bereich schützen" (Warnt beim Überschreiben).

**Zone B: Manuell (ab Zeile 201)**
Hier ist Platz für Nachmeldungen.
*   Kommt jemand spontan dazu? Scrolle zu Zeile 201 und **schreibe einfach rein**.

### Das Status-Feld
Egal ob Zone A (Formel) oder Zone B (Getippt): Die Spalte "Status" daneben (z.B. Spalte Z) ist frei.
Da Zeile 5 *immer* fest mit der ersten Online-Anmeldung verknüpft ist, verrutscht dein Status ("Storniert") nie.

---

## 8. Fortgeschrittene Technik: Dynamische Filter-Ansicht (Master-Formel)

Diese Formel kombiniert Datenimport, komplexe Berechnungen (z.B. Adress-Zusammenführung) und automatisches Ausblenden von leeren Zeilen.

```excel
=LET(
  // 1. BASISDATEN & KONTEXT
  // Wir holen alles von INPUT_ONLINE, um sicherzustellen, dass die Zeilenhöhe gleich ist.
  raw_data; INPUT_ONLINE!A2:ZZ;
  
  // Definition des "Leit-Kriteriums" für das Ausblenden
  // (z.B. nur anzeigen, wenn Spalte A (Zeitstempel/ID) vorhanden ist)
  ist_datenzeile; INPUT_ONLINE!A2:A <> "";

  // ---------------------------------------------------------
  // 2. SPALTEN A bis F (Direkte Übernahme)
  // ---------------------------------------------------------
  block_A_F; INPUT_ONLINE!A2:F;

  // ---------------------------------------------------------
  // 3. SPALTEN G bis M (Deine komplexen Formeln)
  // ---------------------------------------------------------
  // Jede Formel muss ein Array zurückgeben, das genau so hoch ist wie A2:A.
  
  // Beispiel Spalte G (Die Formel hier einfügen)
  col_G; ...DEINE_FORMEL_FÜR_G...; 
  
  // Beispiel Spalte H
  col_H; ...DEINE_FORMEL_FÜR_H...;
  
  // ... Platzhalter für I, J ...
  
  // Spalte K (Deine Adress-Formel von vorhin):
  col_K; WENNFEHLER(
           BYROW(
             FILTER(raw_data; REGEXMATCH(INPUT_ONLINE!A1:ZZ1; "(?i)Stra.e|Haus_?nr|Nr\.|Anschrift|Adresse")*NICHT(REGEXMATCH(INPUT_ONLINE!A1:ZZ1; "(?i)E-?Mail"))); 
             LAMBDA(z; TEXTJOIN(" "; WAHR; z))
           ); 
           ""
         );

  // ... Platzhalter für L, M ...
  
  // Den Block G-M horizontal zusammensetzen:
  block_G_M; HSTACK(col_G; col_H; ... col_I ...; col_K; ... col_M);

  // ---------------------------------------------------------
  // 4. SPALTEN N bis P (Direkte Übernahme)
  // ---------------------------------------------------------
  block_N_P; INPUT_ONLINE!N2:P;

  // ---------------------------------------------------------
  // 5. ZUSAMMENBAU & FILTER
  // ---------------------------------------------------------
  // Alles nebeneinander stapeln
  alle_spalten; HSTACK(block_A_F; block_G_M; block_N_P);
  
  // Filtern: Nur Zeilen ausgeben, wo Daten vorhanden sind
  FILTER(alle_spalten; ist_datenzeile)
)
```

---

## 9. Einrichtung der Status-Spalte (TN_LISTE)

Wir verzichten auf komplexe Skripte und nutzen einen stabilen, manuellen Workflow für den Freizeitleiter ("Opt-In Prinzip").

### A. Einrichtung (Spalte B)
1.  Markiere **Spalte B** (ab Zeile 5).
2.  **Daten > Datenvalidierung > Regel hinzufügen**.
3.  Kriterium: **Dropdown**.
4.  Optionen definieren:
    *   `Angemeldet` (Grün)
    *   `Abgemeldet` (Grau)
    *   `Storniert` (Rot)
    *   *Optional:* `Warteliste` (Gelb)
5.  **Wichtig:** Unter "Erweiterte Optionen" den Anzeigestil auf **Chip** setzen.

### B. Der Workflow
*   **Neue Anmeldung:** Erscheint durch den Import automatisch in der Liste. Das Status-Feld ist zunächst **leer** ⚪.
*   **Bestätigung:** Der Freizeitleiter prüft die Zeile und setzt den Status manuell auf **"Angemeldet"** 🟢.
*   **Vorteil:**
    1.  **Kontrolle:** Kein Teilnehmer rutscht "unbemerkt" durch. Leere Status-Felder signalisieren "Noch zu bearbeiten".
    2.  **Stabilität:** Keine Formeln, die überschrieben werden oder kaputtgehen können.
    3.  **Saubere Daten:** Spätere Listen filtern strikt nach `Status = 'Angemeldet'`. Leere oder stornierte Zeilen werden ignoriert.
