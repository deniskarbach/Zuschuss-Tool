# COL_DEF Spalten-Mapping V7

**Zweck:** Definiert pro KEY, welche Output-Schlüssel auf welche TN_LISTE-Spalten mappen.

---

## Struktur

| Spalte | Inhalt |
|--------|--------|
| A | KEY | `*` = Wildcard für alle |
| B | SCHLUESSEL | z.B. `Name`, `PLZ+Ort` |
| C | TN_HEADER | Header-Name in TN_LISTE |
| D | TYP | `DIREKT` / `KOMBINIERT` / `FORMEL` / `LEER` |
| E | FORMEL | Für KOMBINIERT/FORMEL |

---

## Standard-Einträge (Wildcard `*`)

| KEY | SCHLUESSEL | TN_HEADER | TYP | FORMEL |
|-----|------------|-----------|-----|--------|
| `*` | Name | Nachname | DIREKT | |
| `*` | Vorname | Vorname | DIREKT | |
| `*` | Geburtsdatum | Geburtsdatum | DIREKT | |
| `*` | Jahr | Geburtsdatum | FORMEL | `YEAR({Geburtsdatum})` |
| `*` | PLZ | PLZ | DIREKT | |
| `*` | Ort | Wohnort | DIREKT | |
| `*` | PLZ+Ort | - | KOMBINIERT | `{PLZ} & ", " & {Ort}` |
| `*` | Straße | Straße | DIREKT | |
| `*` | Alter | Alter | DIREKT | |
| `*` | Landkreis | Landkreis | DIREKT | |
| `*` | Bundesland | Bundesland | DIREKT | |
| `*` | Funktion | Funktion | DIREKT | |
| `*` | Anwesenheit | Anwesenheit | DIREKT | |
| `*` | Unterschrift | - | LEER | |
| `*` | Name+Vorname | - | KOMBINIERT | `{Nachname} & ", " & {Vorname}` |
| `*` | Vorname+Name | - | KOMBINIERT | `{Vorname} & " " & {Nachname}` |
| `*` | Vor- u. Zuname | - | KOMBINIERT | `{Vorname} & " " & {Nachname}` |
| `*` | Kreis | Landkreis | DIREKT | |
| `*` | Geburts-jahr | Geburtsdatum | FORMEL | `YEAR({Geburtsdatum})` |
| `*` | Teiln. Tage | Anwesenheit | DIREKT | |

---

## Kreis-spezifische Überschreibungen

| KEY | SCHLUESSEL | TN_HEADER | TYP | FORMEL |
|-----|------------|-----------|-----|--------|
| `Landkreis Westerwaldkreis_*` | Name | - | KOMBINIERT | `{Nachname} & ", " & {Vorname}` |

---

## Lookup-Logik

```excel
get_col_def; LAMBDA(key; schluessel;
  LET(
    exact; FILTER(COL_DEF!A:E; (A:A=key)*(B:B=schluessel));
    wildcard; FILTER(COL_DEF!A:E; (A:A="*")*(B:B=schluessel));
    IFERROR(INDEX(exact;1); IFERROR(INDEX(wildcard;1); "NOT_FOUND"))
  )
);
```
