# Feature Request: Erweiterte Anzeigesteuerung über RULES

**Status:** Planungsphase / Backlog
**Priorität:** Mittel

## Aktuelle Situation (V8)
- Die Variable `filter_function` (welche Funktionsgruppen angezeigt werden) ist in den `.txt` Dateien "hardcoded" (z.B. `"TN"` oder `"TN|MA|LEITUNG"`).
- Die RULES-Spalte `TARGET_GROUPS` steuert aktuell nur die **Mindestanzahl**-Prüfung, hat aber keinen Einfluss auf die **Anzeige**.

## Gewünschtes Feature
Es soll möglich sein, über RULES gezielt Personengruppen für die Anzeige ein- oder auszuschließen, ohne die Formel-Datei ändern zu müssen.

### Szenario
Eine Liste ist als Mixed-List konfiguriert (`TN|MA|LEITUNG|REF`). In manchen Fällen sollen aber **keine Referenten** erscheinen.

### Lösungsansatz
Einführung einer Logikverknüpfung in allen V8-Formeln:
```excel
Anzeige = (Hardcoded-Filter) UND (RULES-Filter)
```

**Beispiel:**
- Hardcoded: `TN|MA|LEITUNG|REF`
- RULES (`TARGET_GROUPS`): `TN;MA;LEITUNG`
- **Ergebnis:** Referenten werden ausgeblendet.

## Umsetzungsmöglichkeiten
1. **Implizit über TARGET_GROUPS:** Wie oben beschrieben (Filterung durch Schnittmenge).
2. **Explizit über GRUPPEN_NUR_LOKAL:** Nutzung einer existierenden oder neuen Spalte für spezifische Ausschlüsse.
3. **Neue Spalte DISPLAY_FILTER:** Einführung einer dedizierten Spalte zur Steuerung der Anzeige.

## Nächste Schritte
- Evaluation bei der Planung der nächsten Version (V9?).
- Entscheidung über die bevorzugte RULES-Spalte.
