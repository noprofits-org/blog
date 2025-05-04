---
title: Building a Spreadsheet-Based API Tool with Google Sheets
date: 2025-05-03
tags: Google Apps Script, web app, ProPublica API, spreadsheet automation, Excel alternatives
description: How to leverage Google Sheets and Google Apps Script to create a powerful data retrieval system that connects to external APIs, demonstrating capabilities beyond what free Excel Online can offer.
---

# Abstract

This project demonstrates how Google Sheets combined with Google Apps Script can overcome limitations found in Excel's free online version by enabling direct API connectivity. I developed a spreadsheet system that connects to the ProPublica Nonprofit Explorer API to retrieve financial data for organizations based on their Employer Identification Number (EIN). The solution includes a custom menu in the spreadsheet and a web app interface that allows users without Google accounts to access the functionality. By implementing this data retrieval system using Google's free tools, I showcase how users can automate complex data operations without premium spreadsheet subscriptions. The approach serves as a practical template for connecting spreadsheets to various data sources through APIs, opening possibilities for enhanced data analysis within free cloud-based spreadsheet platforms.

# Introduction

Spreadsheet applications remain essential tools for data analysis, but their capabilities vary significantly between paid and free versions. The free online version of Excel notably restricts users from connecting to external data sources through APIs, limiting automation possibilities for data collection and analysis. This constraint poses challenges for users who need regular access to external data but lack the resources for premium spreadsheet solutions.

Google Sheets, combined with Google Apps Script, offers a compelling alternative by providing free access to API connectivity. Google Apps Script, a JavaScript-based scripting platform integrated with Google Workspace, enables users to extend spreadsheet functionality through custom code. This capability addresses a critical gap in free spreadsheet offerings: the ability to programmatically retrieve data from external sources.

This study demonstrates this advantage by developing a system that connects to the ProPublica Nonprofit Explorer API. This API provides structured financial data from IRS Form 990 filings for tax-exempt organizations, delivering information in JSON format when queried with an organization's EIN.[@ProPublica2025] While the nonprofit sector serves as our test case, the methodology applies broadly to any scenario requiring spreadsheet integration with external data sources.

Our implementation includes two key components: a script bound to a Google Workbook that handles API requests and data processing, and a web app deployment that extends accessibility beyond Google account holders. This dual-interface approach showcases how Google's ecosystem can support both internal and external data workflows without additional licensing costs. By documenting this process, I provide a practical framework for overcoming limitations in free spreadsheet applications, empowering users to create more sophisticated data solutions without financial barriers.

# Experimental

Code 1. Google Apps Script for fetching and processing nonprofit data from the ProPublica API, including functions for workbook manipulation and custom menu integration.
```python
/**
 * Configuration object to avoid redeclaration issues
 */
var Config = {
  API_BASE_URL: "https://projects.propublica.org/nonprofits/api/v2/organizations/"
};

/**
 * Serves the web app HTML interface
 */
function doGet() {
  return HtmlService.createHtmlOutput(
    '<!DOCTYPE html>' +
    '<html>' +
    '<head>' +
    '<title>Nonprofit Data Fetcher</title>' +
    '<style>' +
    'body { font-family: Arial, sans-serif; margin: 20px; }' +
    'h2 { color: #4285F4; }' +
    '.form-container { max-width: 400px; }' +
    'input[type="text"] { width: 100%; padding: 8px; margin: 10px 0; }' +
    'input[type="submit"] { background-color: #4285F4; color: white; padding: 10px 20px; border: none; cursor: pointer; }' +
    'input[type="submit"]:hover { background-color: #357AE8; }' +
    '#result { margin-top: 20px; color: #333; }' +
    '.error { color: red; }' +
    'table { border-collapse: collapse; width: 100%; margin-top: 20px; }' +
    'th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }' +
    'th { background-color: #D9EAD3; font-weight: bold; }' +
    'tr:nth-child(even) { background-color: #F3F3F3; }' +
    'tr:nth-child(odd) { background-color: #E6F2FF; }' +
    '.org-info { font-weight: bold; margin-bottom: 10px; }' +
    '</style>' +
    '</head>' +
    '<body>' +
    '<h2>Fetch Nonprofit Data</h2>' +
    '<div class="form-container">' +
    '<form id="einForm" onsubmit="handleSubmit(event)">' +
    '<label for="ein">Enter EIN (e.g., 123456789):</label><br>' +
    '<input type="text" id="ein" name="ein" placeholder="Enter 9-digit EIN" required><br>' +
    '<input type="submit" value="Fetch Data">' +
    '</form>' +
    '<div id="result"></div>' +
    '</div>' +
    '<script>' +
    'function handleSubmit(event) {' +
    '  event.preventDefault();' +
    '  const ein = document.getElementById("ein").value;' +
    '  document.getElementById("result").innerHTML = "Fetching data...";' +
    '  google.script.run' +
    '    .withSuccessHandler(showResult)' +
    '    .withFailureHandler(showError)' +
    '    .fetchAndDisplayData(ein);' +
    '}' +
    'function showResult(result) {' +
    '  let html = "<p>Data successfully loaded into sheet: " + result.sheetName + "</p>";' +
    '  html += "<div class=\\"org-info\\">Organization: " + result.orgName + " (EIN: " + result.ein + ")</div>";' +
    '  if (result.filings.length === 0) {' +
    '    html += "<p>No filing data available for this organization.</p>";' +
    '  } else {' +
    '    html += "<table>";' +
    '    html += "<tr><th>Year</th><th>Total Revenue</th><th>Total Expenses</th><th>Total Assets</th>" +' +
    '            "<th>Total Liabilities</th><th>Net Assets</th><th>Contributions & Grants</th>" +' +
    '            "<th>Program Revenue</th><th>Investment Income</th></tr>";' +
    '    result.filings.forEach(filing => {' +
    '      html += "<tr>" +' +
    '        "<td>" + filing.year + "</td>" +' +
    '        "<td>$" + filing.totalRevenue.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.totalExpenses.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.totalAssets.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.totalLiabilities.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.netAssets.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.contributionsGrants.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.programRevenue.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "<td>$" + filing.investmentIncome.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2}) + "</td>" +' +
    '        "</tr>";' +
    '    });' +
    '    html += "</table>";' +
    '  }' +
    '  document.getElementById("result").innerHTML = html;' +
    '}' +
    'function showError(error) {' +
    '  document.getElementById("result").innerHTML = \'<span class="error">Error: \' + error.message + \'</span>\';' +
    '}' +
    '</script>' +
    '</body>' +
    '</html>'
  ).setTitle('Nonprofit Data Fetcher');
}

/**
 * Adds a custom menu to the spreadsheet when it opens
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Nonprofit Tools')
    .addItem('Apply Working Sheet Format', 'formatWorkingSheet')
    .addItem('Clear All Formatting', 'clearAllFormatting')
    .addItem('Fetch Nonprofit Data by EIN', 'showEinInputDialog')
    .addItem('Adjust Column Widths', 'setOptimalColumnWidths')
    .addToUi();
}

/**
 * Shows a dialog box for entering an EIN (for sheet UI)
 */
function showEinInputDialog() {
  var ui = SpreadsheetApp.getUi();
  var response = ui.prompt(
    'Enter Nonprofit EIN',
    'Please enter the EIN (Employer Identification Number) of the nonprofit:',
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() == ui.Button.OK) {
    var ein = response.getResponseText().trim();
    ein = ein.replace(/-/g, '');
    
    if (isValidEIN(ein)) {
      fetchAndDisplayData(ein);
    } else {
      ui.alert('Invalid EIN Format', 'Please enter a valid 9-digit EIN.', ui.ButtonSet.OK);
    }
  }
}

/**
 * Validates if the string is a proper EIN (9 digits)
 */
function isValidEIN(ein) {
  return /^\d{9}$/.test(ein);
}

/**
 * Fetches nonprofit data from ProPublica API and displays it in a new sheet
 */
function fetchAndDisplayData(ein) {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  ein = ein.replace(/-/g, '');
  
  if (!isValidEIN(ein)) {
    throw new Error('Invalid EIN Format. Please enter a valid 9-digit EIN.');
  }
  
  try {
    var options = {
      'headers': {
        'User-Agent': 'NonprofitDataFetcher/1.0 (Google Apps Script)'
      }
    };
    var response = UrlFetchApp.fetch(Config.API_BASE_URL + ein + ".json", options);
    Logger.log('API Response Status: ' + response.getResponseCode());
    
    var data = JSON.parse(response.getContentText());
    
    var orgName = data.organization.name;
    var safeOrgName = orgName.replace(/[^a-zA-Z0-9\s-_]/g, '');
    var sheetNameBase = safeOrgName.substring(0, 80) + " (" + ein + ")";
    var sheetName = sheetNameBase.substring(0, 100);
    var counter = 1;
    
    while (spreadsheet.getSheetByName(sheetName)) {
      sheetName = sheetNameBase.substring(0, 95) + "_" + counter;
      counter++;
    }
    
    var sheet = spreadsheet.insertSheet(sheetName);
    sheet.clear();
    
    sheet.getRange(1, 1, 1, 9).merge();
    sheet.getRange(1, 1).setValue("NONPROFIT DATA: " + orgName + " (EIN: " + ein + ")");
    sheet.getRange(1, 1).setFontSize(14);
    sheet.getRange(1, 1).setFontWeight("bold");
    sheet.getRange(1, 1).setHorizontalAlignment("center");
    sheet.getRange(1, 1).setBackground("#4285F4");
    
    var headers = [
      "Year", "Total Revenue", "Total Expenses", "Total Assets",
      "Total Liabilities", "Net Assets", "Contributions & Grants",
      "Program Revenue", "Investment Income"
    ];
    
    for (var i = 0; i < headers.length; i++) {
      sheet.getRange(2, i + 1).setValue(headers[i]);
      sheet.getRange(2, i + 1).setFontWeight("bold");
      sheet.getRange(2, i + 1).setBackground("#D9EAD3");
    }
    
    var filings = data.filings_with_data;
    var filingData = [];
    if (filings && filings.length > 0) {
      filings.sort(function(a, b) { return b.tax_prd - a.tax_prd; });
      
      for (var i = 0; i < filings.length; i++) {
        var filing = filings[i];
        var row = i + 3;
        var yearStr = String(filing.tax_prd_yr);
        var values = [
          yearStr, filing.totrevenue || 0, filing.totfuncexpns || 0,
          filing.totassetsend || 0, filing.totliabend || 0,
          (filing.totnetassetend || 0), filing.totcntrbgfts || 0,
          filing.totprgmrevnue || 0, filing.invstmntinc || 0
        ];
        sheet.getRange(row, 1, 1, values.length).setValues([values]);
        filingData.push({
          year: yearStr,
          totalRevenue: filing.totrevenue || 0,
          totalExpenses: filing.totfuncexpns || 0,
          totalAssets: filing.totassetsend || 0,
          totalLiabilities: filing.totliabend || 0,
          netAssets: filing.totnetassetend || 0,
          contributionsGrants: filing.totcntrbgfts || 0,
          programRevenue: filing.totprgmrevnue || 0,
          investmentIncome: filing.invstmntinc || 0
        });
      }
      
      sheet.getRange(3, 2, filings.length, 8).setNumberFormat("$#,##0.00");
      setOptimalColumnWidths(sheet);
      sheet.setFrozenRows(2);
      applyAlternatingRowColors(sheet, 3, filings.length);
      sheet.getRange(1, 1, filings.length + 2, 9).setBorder(
        true, true, true, true, true, true, "black", SpreadsheetApp.BorderStyle.SOLID
      );
    } else {
      sheet.getRange(3, 1).setValue("No filing data available for this organization.");
    }
    
    spreadsheet.setActiveSheet(sheet);
    SpreadsheetApp.flush();
    
    return {
      sheetName: sheetName,
      orgName: orgName,
      ein: ein,
      filings: filingData
    };
  } catch (error) {
    Logger.log('Error: ' + error.message);
    throw new Error("Failed to fetch data: " + error.message);
  }
}

/**
 * Sets optimal column widths based on content
 */
function setOptimalColumnWidths(sheet) {
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  
  var columnWidths = [
    60, 120, 120, 120, 120, 120, 150, 120, 120
  ];
  
  for (var i = 0; i < columnWidths.length; i++) {
    sheet.setColumnWidth(i + 1, columnWidths[i]);
  }
}

/**
 * Clears all data from the sheet except for any formatting
 */
function clearSheetData() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var lastRow = Math.max(sheet.getLastRow(), 100);
  var lastCol = Math.max(sheet.getLastColumn(), 9);
  
  sheet.getRange(1, 1, lastRow, lastCol).clearContent();
  
  try {
    var headerRange = sheet.getRange(1, 1, 1, lastCol);
    headerRange.breakApart();
  } catch (e) {
    Logger.log("Note: Could not unmerge cells: " + e.message);
  }
}

/**
 * Apply alternating row colors to the data rows
 */
function applyAlternatingRowColors(sheet, startRow, numRows) {
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  }
  
  var currentBandings = sheet.getBandings();
  for (var i = 0; i < currentBandings.length; i++) {
    currentBandings[i].remove();
  }
  
  var dataRange = sheet.getRange(startRow, 1, numRows, 9);
  var banding = dataRange.applyRowBanding();
  banding.setHeaderRowColor(null);
  banding.setFirstRowColor("#F3F3F3");
  banding.setSecondRowColor("#E6F2FF");
}

/**
 * Formats the working sheet
 */
function formatWorkingSheet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var lastColumn = Math.max(1, sheet.getLastColumn());
  var lastRow = Math.max(1, sheet.getLastRow());
  
  if (lastColumn >= 1) {
    var headerRange = sheet.getRange(1, 1, 1, lastColumn);
    headerRange.setHorizontalAlignment("center");
    headerRange.merge();
    headerRange.setValue("WORKING SHEET");
    headerRange.setFontSize(14);
    headerRange.setFontWeight("bold");
    headerRange.setHorizontalAlignment("center");
    headerRange.setVerticalAlignment("middle");
    headerRange.setBackground("#4285F4");
  }
  
  if (lastColumn >= 1 && lastRow >= 2) {
    var firstDataRow = sheet.getRange(2, 1, 1, lastColumn);
    firstDataRow.setFontWeight("bold");
    firstDataRow.setHorizontalAlignment("left");
    firstDataRow.setBackground("#D9EAD3");
  }
  
  if (lastColumn >= 1 && lastRow >= 3) {
    var dataRange = sheet.getRange(3, 1, Math.max(1, lastRow - 2), lastColumn);
    var currentBandings = sheet.getBandings();
    for (var i = 0; i < currentBandings.length; i++) {
      currentBandings[i].remove();
    }
    
    var banding = dataRange.applyRowBanding();
    banding.setHeaderRowColor(null);
    banding.setFirstRowColor("#F3F3F3");
    banding.setSecondRowColor("#E6F2FF");
  }
  
  sheet.setFrozenRows(2);
  
  if (lastColumn >= 1 && lastRow >= 1) {
    var fullRange = sheet.getRange(1, 1, lastRow, lastColumn);
    fullRange.setBorder(true, true, true, true, true, true, "black", SpreadsheetApp.BorderStyle.SOLID);
  }
  
  setOptimalColumnWidths(sheet);
  
  SpreadsheetApp.getActive().toast("Working sheet formatting applied successfully!", "Format Complete", 5);
}

/**
 * Clears all formatting from the sheet while preserving data
 */
function clearAllFormatting() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var lastColumn = Math.max(1, sheet.getLastColumn());
  var lastRow = Math.max(1, sheet.getLastRow());

  if (lastColumn >= 1 && lastRow >= 1) {
    try {
      sheet.getRange(1, 1, lastRow, lastColumn).breakApart();
    } catch (e) {
      Logger.log("Note: Could not unmerge cells: " + e.message);
    }

    var currentBandings = sheet.getBandings();
    for (var i = 0; i < currentBandings.length; i++) {
      currentBandings[i].remove();
    }

    var fullRange = sheet.getRange(1, 1, lastRow, lastColumn);
    fullRange.clearFormat();
    fullRange.clearNote();
    fullRange.setFontFamily(null);
    fullRange.setFontSize(10);
    fullRange.setFontWeight("normal");
    fullRange.setFontStyle("normal");
    fullRange.setHorizontalAlignment("left");
    fullRange.setVerticalAlignment("bottom");
    fullRange.setBackground(null);
    fullRange.setBorder(false, false, false, false, false, false);

    sheet.clearConditionalFormatRules();

    for (var i = 1; i <= lastColumn; i++) {
      sheet.setColumnWidth(i, 100);
    }

    sheet.setFrozenRows(0);
    sheet.setFrozenColumns(0);
  }

  SpreadsheetApp.getActive().toast("All formatting has been cleared!", "Clear Complete", 5);
}
```

Code 2. Configuration for deploying the Google Apps Script as a web app, including HTML interface and server-side settings.
```python
{
  "timeZone": "America/New_York",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/script.external_request"
  ],
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE"
  }
}
```

# Results

<img src="/images/web_app_view.png" alt="Web App Interface" />

**Figure 1.** Screenshot of the web app interface displaying nonprofit financial data retrieved from the ProPublica API for a sample organization, including a table of filing years and metrics.

<img src="/images/workbook_view.png" alt="Google Sheet Output" />

**Figure 2.** Screenshot of the Google Workbook showing a dynamically created sheet with nonprofit financial data, formatted with headers and alternating row colors.

# Discussion

The implementation successfully demonstrates how Google Sheets with Google Apps Script overcomes a major limitation of Excel's free online version: the inability to connect directly to external APIs. Our solution provides seamless API integration with an intuitive interface, enabling users to retrieve and analyze external data without premium spreadsheet subscriptions.

The web app interface shown in Figure 1 represents a significant advantage of this approach, allowing anyone to access the data retrieval functionality without a Google account. The interface provides a simple form for entering an EIN, delivering results in a clearly formatted table with financial metrics across multiple years. This external accessibility extends the utility of spreadsheet-based tools beyond organizational boundaries, making it valuable for public-facing applications where data transparency is important.

The Google Workbook output in Figure 2 illustrates how the retrieved data seamlessly integrates into the spreadsheet environment. Each organization's data populates a new sheet named with the organization's details, applying consistent formatting with bold headers, frozen rows, and currency formatting. This automatic sheet creation and formatting eliminates manual data entry and presentation tasks, streamlining the workflow for analyzing multiple organizations.

From a technical perspective, several features enhance the system's robustness and usability. The namespaced configuration approach prevents variable conflicts, a common issue in larger script projects. The implementation of a User-Agent header in API requests ensures compatibility with external servers that might otherwise reject automated queries. Comprehensive error handling provides clear feedback when issues arise, improving the user experience for both technical and non-technical users.

One key benefit of this Google-based approach is the elimination of licensing costs that would typically accompany similar functionality in commercial spreadsheet applications. Enterprise versions of Excel that support API connectivity require significant investment, while our implementation leverages entirely free tools. This cost advantage makes advanced data capabilities accessible to individuals, small organizations, and educational settings where budget constraints might otherwise limit technological solutions.

The methodology also offers flexibility for adaptation to other data sources. While I demonstrated connectivity with the ProPublica API, the same approach works with virtually any REST API that returns structured data. Users could modify this template to connect to weather services, stock market data, social media metrics, or internal organizational APIs with minimal changes to the core functionality.

Limitations of this approach include dependence on Google's ecosystem and potential API rate limits imposed by data providers. Future enhancements could include adding export capabilities from the web app, implementing caching to reduce API calls, and creating visualization options directly within the interface. Despite these considerations, the implementation successfully demonstrates how free Google tools can match or exceed capabilities found in premium spreadsheet applications.

# References

