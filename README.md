# Zuschuss-System V8

**Ein Open-Source-Werkzeug für das Zuschussmanagement und die Erstellung von Förderlisten für Jugendfreizeiten und Bildungsmaßnahmen.**

Dieses Projekt stellt eine leistungsfähige, tabellenbasierte Lösung (Google Sheets + Apps Script) bereit, um Teilnehmerlisten zu führen, Zuschüsse automatisch zu berechnen (z.B. Landesjugendplan RLP/Hessen/NRW, diverse Landkreise) und fertige Antragslisten zu exportieren.

---

## 🚀 Funktionen

*   **Zentrale Datenhaltung:** Alle Teilnehmerdaten an einem Ort (`TN_LISTE`).
*   ** Automatische Regel-Prüfung:** Das System prüft Alter, Wohnort und Dauer gegen hinterlegte Förderrichtlinien (die "RULES").
*   **Dynamische Berechnung:** Unterstützung für komplexe Logiken wie Quotenregelungen (z.B. 50% Einheimischen-Quote), Mindestteilnehmerzahlen und Stichtagsregelungen.
*   **PDF- & Excel-Export:** Integrierte Sidebar zum Erstellen von druckfertigen Listen für Zuschussgeber.
*   **Datenschutz-freundlich:** Lokale Verarbeitung im eigenen Google Sheet möglich (Audit-Modus).

## 📂 Datei-Struktur

Dieses Repository ist wie folgt aufgebaut:

*   **`src/`**: Der Quellcode für die Google Apps Script Erweiterungen (Export-Sidebar, PDF-Generierung).
*   **`formulas/`**: Die Kern-Logik des Systems. Hier liegen die komplexen Excel/Google-Sheets-Formeln als Textdateien, sortiert nach Bundesland (z.B. `RLP`, `NRW`) und Landkreis. Diese Formeln werden in die entsprechenden Zellen der Tabellenblätter kopiert.
*   **`docs/`**: Handbücher und technische Dokumentationen.
*   **`SETUP_INSTRUCTIONS.txt`**: Wichtige Hinweise und Lizenztexte für die Einrichtung im Spreadsheet.

## 🛠 Installation & Nutzung

Da es sich um eine Google Sheets Anwendung handelt, gibt es keine klassische "Installation".

1.  **Code integrieren:** Öffnen Sie den Script-Editor in Ihrem Google Sheet (`Erweiterungen > Apps Script`) und kopieren Sie die Inhalte aus `src/` (Code.js und HTML-Dateien).
2.  **Formeln nutzen:** Die Logik für die Zuschüsse befindet sich in den Textdateien unter `formulas/`. Der Inhalt dieser Dateien entspricht der Formel, die in die Zelle `A1` (oder die entsprechende Startzelle) des jeweiligen Zuschuss-Blattes gehört.
3.  **Setup:** Beachten Sie die Hinweise in `SETUP_INSTRUCTIONS.txt` für die Konfiguration des `SETUP`-Blattes.

## ⚖️ Lizenz & Rechtliches

**Lizenz:** GNU Affero General Public License v3.0 (GNU AGPL v3)
Dieses Projekt ist komplexe Software, die Rechte an Code und Logik liegen beim Autor. Nutzung und Weiterentwicklung sind unter den Bedingungen der AGPL gestattet. Das bedeutet insbesondere: Wer dieses Tool als Dienst (z.B. SaaS) anbietet, muss den Quellcode inkl. aller Änderungen offenlegen.

**Haftungsausschluss:**
Dieses Tool ist eine unverbindliche Hilfestellung. Die Nutzung erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für abgelehnte Zuschüsse, Rechenfehler oder versäumte Fristen. Es obliegt dem Nutzer, alle Ergebnisse vor der Einreichung bei Behörden zu prüfen.

---
*Copyright (C) 2026 Denis Karbach*
