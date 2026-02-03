# Feature Request: Automatische Kennzeichnung (Spalte B)

**Zugehörigkeit:** Kirchengemeinde Neunkirchen (NRW) / Allgemein V8
**Status:** Backlog
**Basis:** Screenshot Vorgabe

## Anforderung
Die Spalte "Kennzeichnung" (Spalte B) soll automatisch basierend auf Funktion, Alter und Status gefüllt werden.

## Logik (laut Screenshot)

### Mapping-Regeln:
1. **L** = Leiter/in (Funktion: LEITUNG)
2. **LE** = Leiter/in mit Entgelt (Status: Honorar?)
3. **S** = Schüler/in und Student/in (Status oder Alter?)
   - *Hinweis: Gilt laut Screenshot für "Teilnehmer/innen über 20 Jahre"*
4. **W** = Zivil- und Wehrdienstleistende (Status?)
5. **A** = Auszubildende und Arbeitslose (Status: Arbeitslos / Ausbildung)
6. **K** = Küche (Funktion: KÜCHE / MA?)

### Aktuelles Problem (V8)
- V8 unterstützt aktuell nur Mapping von `Funktion` zu einem Kürzel (`LABEL_MAP`).
- Diese Anforderung benötigt komplexe Logik (Alter > 20 UND Schüler/Student/Arbeitslos/etc.).
- Diese Datenfelder (Schüler, Student, Zuvil, Wehr, Azubi) sind in `TN_LISTE` (Spalte "Sozial"?) oft nicht explizit oder strukturiert vorhanden.

## Umsetzungsvorschlag (Zukunft)
- Erweiterung von `Spalte Sozial` in `TN_LISTE` um Dropdowns: "Schüler", "Student", "Azubi", "Arbeitslos", "Wehrdienst".
- Erweiterung der V8-Formel (`_F_LOGIK` / `_G_LOGIK` äquivalent) um eine `_KENNZEICHNUNG_LOGIK`, die diese Felder auswertet.
