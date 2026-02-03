# Feature Request: Integrierter Audit-Modus (Enhanced Debug)

**Status:** Proposed
**Priorität:** Hoch
**Referenz:** Diskussion zur Unzuverlässigkeit der `rheinlahn_v8_audit.txt`

## Problemstellung
Aktuell existiert eine separate "Audit-Formel" (`rheinlahn_v8_audit.txt`), die verwendet wird, um zu prüfen, warum Personen *nicht* auf einer Zuschussliste erscheinen. Diese Lösung hat gravierende Nachteile:
1.  **Redundanz**: Die Logik (Filter, Regeln) muss an zwei Stellen gepflegt werden (Liste & Audit).
2.  **Unzuverlässigkeit**: Das Audit kennt interne Konfigurationen der Liste ("Hardcoded Filter") nicht und liefert falsche "OK"-Ergebnisse für Personen, die auf der Liste fehlen.
3.  **Wartungsaufwand**: Änderungen an V8 müssen manuell ins Audit übertragen werden.

## Lösungsvorschlag
Abschaffung der separaten Audit-Datei zugunsten eines **erweiterten Debug-Modus** direkt in den V8-Listen.

### Funktionsweise
Jede V8-Datei verfügt bereits über einen `debug_mode` (gesteuert über `SETUP!B69`).
Dieser Modus soll erweitert werden, um nicht nur Metadaten, sondern eine **Liste der abgelehnten Personen mit Grund** auszugeben.

**Logik:**
```excel
IF(debug_mode;
  VSTACK(
    "DEBUG REPORT";
    "Valid Rows: " & ROWS(valid_data);
    "--- REJECTED / FILTERED ---";
    reasons_table  <-- Neue Tabelle mit Name, Vorname, Ablehnungsgrund
  );
  result_table
)
```

### Berechnung der Gründe ("Reasons")
Innerhalb der `LET`-Formel wird parallel zur Maskierung (`mask_final`) eine `MAP`-Funktion laufen, die für jede Zeile prüft:
- Wenn `mask_final` = FALSE:
    - Ist `mask_stat` FALSE? -> "Status falsch"
    - Ist `mask_tg_func` FALSE? -> "Filter/Zielgruppe falsch"
    - Ist `age_ok` FALSE? -> "Alter falsch (Ist: X, Soll: Y)"
    - Ist `local_ok` FALSE? -> "Nicht Lokal"
    - etc.

## Vorteile
- **Single Source of Truth**: Die Liste prüft sich selbst. Es gibt keine Abweichung zwischen "Liste" und "Audit".
- **Kontext-Aware**: Die Audit-Logik kennt exakt den Hardcoded-Filter ("TN") und die RULES dieser spezifischen Liste.
- **Einfachheit**: Nutzer stellen einfach `SETUP!B69` auf "Debug" und sehen sofort, wer warum fehlt.

## Nächste Schritte
1.  Proof-of-Concept in einer V8-Datei (z.B. Hessen).
2.  Rollout auf alle V8-Formeln (via Script/sed).
