# Selenium Capstone 1 - E-commerce Test Automation

This project contains an automated test suite for the TutorialsNinja e-commerce website using Selenium WebDriver.

## Project Structure
```
Selenium_Capstone_1/
├── tests/
│   └── test_ecommerce.py          # Main test script with multiple test cases
├── utils/
│   ├── excel_reader.py           # Utility for reading test data from Excel
│   └── screenshot_utils.py       # Utility for handling screenshots
├── test_data/
│   └── test_data.xlsx            # Test data in Excel format
├── screenshots/                  # Screenshots from test execution
├── reports/                      # Test reports
├── test_ecommerce.py             # Simplified version for quick testing
├── HOW_THIS_WORKS.md             # Detailed explanation of how the test works
├── IMPROVEMENTS_SUMMARY.md       # Summary of improvements made
└── README.md                     # This file
```

## Features
- Automates complete e-commerce flow: login/register → search product → add to cart → update quantity → verify
- Data-driven testing using Excel test data
- Robust element locating with fallback strategies
- Comprehensive logging and screenshot documentation
- Continues test execution despite individual test case failures
- Generates HTML test reports

## Setup Instructions
1. Install Python 3.x
2. Install required packages:
   ```
   pip install selenium openpyxl pytest pytest-html
   ```
3. Prepare test data in `test_data/test_data.xlsx` with columns:
   - TestCase (e.g., TC001, TC002)
   - Email (base email for test account)
   - Password
   - Product (exact product name to search for)
   - Quantity (desired quantity to test)
   - ExpectedResult (optional)

## Running the Tests
### Option 1: Run the simplified test (single test case)
```bash
python test_ecommerce.py
```

### Option 2: Run the full test suite (multiple test cases from Excel)
```bash
python tests/test_ecommerce.py
```

## Viewing Results
- Console output shows pass/fail status for each test case
- Screenshots are saved in the `screenshots/` directory
- HTML reports are generated in the `reports/` directory

## How It Works
See `HOW_THIS_WORKS.md` for a detailed, beginner-friendly explanation of how the Selenium test automation works.

## Improvements Made
See `IMPROVEMENTS_SUMMARY.md` for details on the enhancements made to improve test robustness and maintainability.

## Troubleshooting
- If elements aren't found, check if the website has changed and update locators accordingly
- For login issues, verify credentials in the Excel file
- Ensure Chrome browser is installed and up-to-date
- Check screenshots in the `screenshots/` directory to see exactly what happened during test execution

---
*Created for Selenium Capstone 1 - September 24, 2026*
