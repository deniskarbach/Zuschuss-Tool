# Walkthrough - Enhanced Cell Information

I have updated the documentation to use more professional and less intrusive methods for providing information to users in Google Sheets.

## Changes Made

### Documentation Update
- **File:** [google_sheets_anleitung.md](file:///Users/deniskarbach/git/zuschuesse/google_sheets_anleitung.md)
- **Feature:** Replaced "Comments" with a two-tier approach:
    1.  **Notes (Notizen):** For static column headers (e.g., "Min TN", "Min Alter"). These appear on hover and don't create notification threads.
    2.  **Help Text (Eingabehilfe):** For cells with logic (e.g., "Logik", "Förder-Umfang"). These appear only when a cell is selected, reducing visual clutter.
- **Section 3: Numerical Validation & Formatting:** Added clear steps for:
    - Restricting Min TN, Age, and Days to **whole numbers** (>= 0).
    - Formatting the **Quote** column as a percentage and restricting its range between 0% and 100%.
    - Formatting the **Quote** column as a percentage and restricting its range between 0% and 100%.
- **Section 4: Cache Architecture:** Documented the setup of local `CACHE_RULES` and `CACHE_PLZDB` sheets in the template to minimize external calls to the Master DB.
- **Section 5: Setup Button (Fix):** Explains why `IFERROR` must be removed to see the "Allow Access" button and provides the correct formula pattern.
    - **Advanced Status Formula:** Added a nested `IF` formula that guides the user based on both the Dropdown state ("Legitimieren") and the Import status ("#REF!" vs Success).
- **Section 6: Dynamic Rule Retrieval:** Documented the `VLOOKUP` logic and clarified that formulas go directly into the target cells (e.g., "Min TN") of the Setup sheet.
    - **Cockpit Logic:** Added specific formulas for the Summary Table ("Zuschuss-Cockpit"):
        - **Anzahl:** `COUNTIFS` from Participant List.
        - **Status:** Conditional check (`Count >= Min TN`).
        - **Hinweis:** `VLOOKUP` for specific notes.
- **Section 7: Data Ingestion (Simplified):** Reduced the architecture to just **1 Visible Sheet**.
    - **Hidden Helper:** `INPUT_ONLINE` now uses a **Smart Formula** (User-provided) to conditionally import data or show manual instructions based on the Setup Dropdown ("Ja"/"Nein").
    - **TN_LISTE (Master):**
        - **Rows 5-200:** Direct formulas (`=INPUT_ONLINE!C2`) handle normalization and data pull.
        - **Rows 201+:** Empty rows for direct manual typing.
        - **Status:** Safe to edit everywhere due to fixed row mapping.
    - **Best Practice:** Noted that Google Forms should share a standard initial structure (Cols C, D, E...) to make this template universal.

## Verification Results

### Visual Review
- The logic descriptions for Spalte I (Logik) and J (Förder-Umfang) have been refined to be more concise while maintaining clarity.
- The formatting uses clear headers and action-oriented instructions ("Vorgehen: ...").

render_diffs(file:///Users/deniskarbach/git/zuschuesse/google_sheets_anleitung.md)
