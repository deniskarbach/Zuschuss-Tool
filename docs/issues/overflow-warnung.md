# Feature: Warnung bei Überlauf in festen Formularbereichen (max_rows)

## Problem

Die V6-Formeln für verschiedene Landkreise haben feste Bereiche mit begrenzter Zeilenanzahl:

| Bereich | Beispiel Bad Kreuznach | max_rows |
|---------|------------------------|----------|
| MA | B4:G15 | 12 |
| REF | B20:G22 | 3 |
| TN | B29:G177 | 149 |

**Aktuelles Verhalten:** Wenn mehr Personen vorhanden sind als `max_rows` erlaubt, werden die überzähligen stillschweigend abgeschnitten (`MIN(ROWS(data); max_rows)`). Der Benutzer erhält **keine Warnung**.

### Risiko

Personen könnten auf der Zuschussliste fehlen, ohne dass dies bemerkt wird.

---

## Lösungsvorschläge

### Option A: Warnmeldung statt Daten

Bei Überlauf Fehlermeldung anzeigen:
```
⚠️ 15 MA gefunden, aber nur 12 Plätze! Bitte manuell prüfen.
```
- ✅ Klar sichtbar
- ❌ Keine Daten mehr sichtbar

### Option B: Daten + Hinweis in letzter Zeile

Letzte Zeile zeigt Überlauf-Info:
```
[...12 von 15...] (+3 weitere)
```
- ✅ Daten bleiben sichtbar
- ❌ Komplexe Formatierung

### Option C: Separate "Überlauf"-Zelle

Extra Zelle im Layout (z.B. neben Header):
```
ℹ️ +3 MA nicht angezeigt
```
- ✅ Daten unverändert, Hinweis klar
- ❌ Layoutanpassung nötig

### Option D: Warnung nur im DEBUG_MODUS

Bei `SETUP!B69 = "Ja"` und Überlauf → Warnung statt Daten  
Bei `SETUP!B69 = "Nein"` → Abschneiden ohne Meldung (für Druck)
- ✅ Konsistent mit bestehendem Debug-System
- ❌ Im Druck-Modus unsichtbar

---

## Betroffene Dateien

- `RLP/Kreise/V6/Bad-Kreuznach/badkreuznachV6.md`
- `RLP/Kreise/V6/Altenkirchen/altenkirchenV6.md`
- `RLP/Kreise/V6/Rhein-Lahn-Kreis/rheinlahnkreisV6.md`
- `RLP/Kreise/V6/Westerwaldkreis/westerwaldkreisV6.md`
- `RLP/Land/RLP/V6/rheinlandpfalzV6.md`

---

## Labels

`enhancement`, `v6-formeln`, `ux`
