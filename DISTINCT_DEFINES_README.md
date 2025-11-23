# Distinct #define Directives Extractor

This script extracts all unique `#define` macro names from the preprocessor directives scan results.

## Usage

```bash
python3 extract_distinct_defines.py
```

**Prerequisites:** You must first run `scan_preprocessor_directives.py` to generate the `preprocessor_directives.csv` file.

## Output Files

The script generates four output files:

### 1. distinct_defines_list.txt
A simple, clean list of all unique macro names (one per line).

**Use case:** Quick reference, copy-paste operations, or scripting.

Example:
```
ADAFRUIT_CC3000_CS
ADAFRUIT_CC3000_IRQ
BLYNK_PRINT
BLYNK_BUFFERS_SIZE
...
```

### 2. distinct_defines_detailed.txt
Detailed information for each unique macro including:
- Macro name
- Full directive from first occurrence
- File and line number of first occurrence
- Total number of occurrences

**Use case:** Detailed analysis and understanding macro definitions.

Example:
```
Macro: BLYNK_PRINT
  Directive: #define BLYNK_PRINT Serial
  First occurrence: src/BlynkSimpleEsp8266.h:42
  Total occurrences: 80
```

### 3. distinct_defines.csv
CSV format with columns:
- Macro Name
- Directive
- File
- Line
- Occurrences

**Use case:** Import into spreadsheet software, database, or data analysis tools.

### 4. distinct_defines.md
Comprehensive Markdown report with:
- Statistics (total directives, unique macros, averages)
- Top 20 most frequently defined macros
- Complete table of all unique macros

**Use case:** Documentation, reports, and easy viewing on GitHub.

## Statistics from Latest Scan

- **Total #define directives:** 1,158
- **Unique macro names:** 490
- **Average occurrences per macro:** 2.36

## Most Frequently Defined Macros

1. `BLYNK_INFO_DEVICE` - 117 occurrences
2. `BLYNK_PRINT` - 80 occurrences
3. `BLYNK_INFO_CONNECTION` - 49 occurrences
4. `BLYNK_BUFFERS_SIZE` - 32 occurrences
5. `BLYNK_USE_128_VPINS` - 31 occurrences

## See Also

- `PREPROCESSOR_SCANNER_README.md` - Main preprocessor directive scanner
- `scan_preprocessor_directives.py` - Scan all preprocessor directives
- `preprocessor_directives.csv` - Complete list of all preprocessor directives
