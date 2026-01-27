# Named Function Registrierung: Schritt-für-Schritt

## Schritt 1: Benannte Funktionen öffnen

1. Öffne **CVJM_Zuschüsse_DEV_V07** in Google Sheets
2. Klicke auf **Daten** in der Menüleiste
3. Klicke auf **Benannte Funktionen**
4. Klicke auf **+ Neue Funktion hinzufügen**

---

## Schritt 2: Funktion benennen

| Feld | Eintrag |
|------|---------|
| **Name der Funktion** | `ZUSCHUSS_ENGINE` |
| **Beschreibung** | `Zentrale Logik für Zuschuss-Teilnehmerlisten nach V7-Regelwerk` |

---

## Schritt 3: Parameter hinzufügen

Klicke für jeden Parameter auf **+ Argument hinzufügen**:

| # | Name | Optional |
|---|------|----------|
| 1 | `tn_range` | ☐ Nein |
| 2 | `event_start` | ☐ Nein |
| 3 | `event_end` | ☑ Ja |
| 4 | `event_typ` | ☐ Nein |
| 5 | `zone` | ☑ Ja |
| 6 | `filter_function` | ☑ Ja |
| 7 | `debug` | ☑ Ja |

---

## Schritt 4: Formel einfügen

1. Öffne die Datei `/Master/ZUSCHUSS_ENGINE.md`
2. Scrolle zum Abschnitt **"Formeldefinition"** (ca. Zeile 46)
3. Kopiere **alles** von `=LET(` bis zur letzten schließenden Klammer `)`
4. Füge es in das Feld **"Formeldefinition"** ein

> **Hinweis:** Die Formel ist sehr lang (~400 Zeilen). Das ist normal.

---

## Schritt 5: Speichern

1. Klicke auf **Erstellen** (blauer Button unten rechts)
2. Warte, bis "Funktion erstellt" erscheint

---

## Schritt 6: Erster Test

1. Gehe zu einem Zuschuss-Blatt (z.B. `K_RLK`)
2. Klicke in eine leere Zelle (z.B. B4)
3. Gib ein:

```
=ZUSCHUSS_ENGINE(TN_LISTE!B2:AQ1710; SETUP!B23; SETUP!H23; SETUP!B18; ; ; WAHR)
```

4. Drücke **Enter**

---

## Was du sehen solltest

| Ausgabe | Bedeutung |
|---------|-----------|
| `✅ Key: Rhein-Lahn-Kreis_Soziale_Bildung...` | Funktioniert! |
| `❌ Key nicht gefunden: ...` | RULES-Eintrag fehlt |
| `❌ BLATT_NICHT_KONFIGURIERT_...` | CONFIG-Eintrag fehlt |
| `#NAME?` | Formel-Fehler |
| `#NV` | Daten nicht gefunden |

---

## Bei Fehlern

| Fehler | Lösung |
|--------|--------|
| `#NAME?` | Prüfe, ob alle Parameter korrekt benannt sind |
| `BLATT_NICHT_KONFIGURIERT` | Trage Blattname in CONFIG ein |
| `Key nicht gefunden` | Prüfe CACHE_RULES auf den Key |
