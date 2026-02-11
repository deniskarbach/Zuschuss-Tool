/**
 * Zuschuss-Tool V8
 * Copyright (C) 2026 Denis Karbach
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

// onOpen wurde entfernt, um Ladezeiten zu optimieren.
// Die Sidebar wird nun ausschließlich über den Button im SETUP-Blatt gestartet.

function showSidebar() {
    const html = HtmlService.createHtmlOutputFromFile('Sidebar')
        .setTitle('Zuschuss Export')
        .setWidth(450);
    SpreadsheetApp.getUi().showSidebar(html);
}

function openExportDialog(selectedSheets) {
    // Store selection in UserProperties to retrieve it in the modal
    PropertiesService.getUserProperties().setProperty('EXPORT_SELECTION', JSON.stringify(selectedSheets));

    const html = HtmlService.createHtmlOutputFromFile('ExportDialog')
        .setWidth(520)
        .setHeight(600);
    SpreadsheetApp.getUi().showModalDialog(html, 'Export');
}

function getSheetNames() {
    // Returns list of visible sheets that look like subsidy lists
    return SpreadsheetApp.getActiveSpreadsheet().getSheets()
        .filter(s => !s.isSheetHidden()) // Exclude hidden sheets
        .map(s => s.getName())
        .filter(n => !['SETUP', 'RULES', 'CACHE_RULES', 'TN_LISTE'].includes(n) && !n.endsWith('_Backup'));
}

function processExport() {
    const selectionProps = PropertiesService.getUserProperties().getProperty('EXPORT_SELECTION');
    if (!selectionProps) return null;
    const sheets = JSON.parse(selectionProps);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const blobs = [];
    const token = ScriptApp.getOAuthToken(); // Current Auth Token for internal fetch

    // 1. Generate PDFs
    sheets.forEach(sheetName => {
        const sheet = ss.getSheetByName(sheetName);
        if (!sheet) return;

        // PDF Generation via Export URL
        // We export the specific gid
        const url = `https://docs.google.com/spreadsheets/d/${ss.getId()}/export?format=pdf&gid=${sheet.getSheetId()}&size=A4&portrait=true&fitw=true&gridlines=false`;
        const response = UrlFetchApp.fetch(url, { headers: { 'Authorization': 'Bearer ' + token } });
        blobs.push(response.getBlob().setName(`${sheetName}.pdf`));
    });

    // 2. Generate Real XLSX
    // Strategy: Create a temp spreadsheet, copy the single sheet there, export that SS as XLSX
    sheets.forEach(sheetName => {
        const sheet = ss.getSheetByName(sheetName);
        if (!sheet) return;

        // Read values from ORIGINAL sheet (where all formula references are intact)
        const values = sheet.getDataRange().getValues();

        // Create Temp Spreadsheet and copy sheet (preserves formatting)
        const tempSS = SpreadsheetApp.create(`Temp_${sheetName}`);
        const tempSheet = sheet.copyTo(tempSS);
        tempSheet.setName(sheetName);
        tempSS.deleteSheet(tempSS.getSheets()[0]); // Delete the default "Sheet1"

        // FLATTEN: Overwrite broken formulas with correct values from original
        tempSheet.getRange(1, 1, values.length, values[0].length).setValues(values);

        // Flush to ensure changes are saved before export
        SpreadsheetApp.flush();

        // Export Temp SS as XLSX
        const url = `https://docs.google.com/spreadsheets/d/${tempSS.getId()}/export?format=xlsx`;
        const response = UrlFetchApp.fetch(url, { headers: { 'Authorization': 'Bearer ' + token } });
        blobs.push(response.getBlob().setName(`${sheetName}.xlsx`));

        // Cleanup: Delete Temp SS
        DriveApp.getFileById(tempSS.getId()).setTrashed(true);
    });

    // 3. ZIP
    const zip = Utilities.zip(blobs, 'Zuschuss_Export_2026.zip');

    // 4. Create Drive Link
    const folder = DriveApp.createFolder("Zuschuss_Export_Temp");
    const file = folder.createFile(zip);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

    return file.getDownloadUrl();
}
