# Issue: Klärung Landkreis Mainz-Bingen (MZ-BIN) V6

**Status:** ⚠️ Blocked / Rücksprache nötig

## Hintergrund
Das Formular für Mainz-Bingen weicht stark vom Standard ab. Spalte B enthält Status-Codes statt Namen/Nummern.

## Offene Punkte

### 1. Status-Logik (Spalte B)
Es werden folgende Kürzel gefordert:
- **HA:** Hauptamtlich
- **J:** Juleica-Inhaber
- **PH:** Pädagogischer Helfer (ohne Juleica)
- **B:** Behindert
- **S:** Sozial benachteiligt
- **V:** Volljährig (>26 oder Status)

**Fragen:**
- Korrespondieren diese Merkmale mit den Spalten **T bis Z** in der `TN_LISTE`?
- **Mehrfach-Status:** Wie soll verfahren werden, wenn eine Person mehrere Merkmale hat (z.B. Juleica + Volljährig)?
  - *Vorschlag:* Codes verketten (z.B. "J, V").

### 2. Referenten (REF)
Das Formular enthält unten (Zelle B52) einen separaten Bereich *"Kostennachweis für Referentinnen"*.
- **Frage:** Soll dieser Bereich automatisch mit Personen vom Typ `REF` befüllt werden?

### 3. Layout Seite 2
Der Screenshot deutet an, dass Seite 2 kürzer ist (gestaucht durch REF-Tabelle?).
- **Frage:** Wie viele Zeilen stehen auf Seite 2 exakt zur Verfügung?

---
**Nächste Schritte:**
- [ ] Feedback zu Status-Spalten einholen
- [ ] Entscheidung zu REF-Bereich treffen
- [ ] Formel implementieren
