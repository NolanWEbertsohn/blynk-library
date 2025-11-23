# Preprocessor Directive Scanner

This script scans all C/C++ source files in the Blynk library repository to find and document all preprocessor directives.

## Usage

```bash
python3 scan_preprocessor_directives.py
```

## Output

The script generates two output files:

1. **preprocessor_directives.csv** - CSV format with columns:
   - Directive: The actual preprocessor directive text
   - File: Relative path to the file
   - Line Number: Line number in the file
   - Description: Human-readable description of the directive's purpose

2. **preprocessor_directives.md** - Markdown format with:
   - Summary statistics by directive type
   - Complete table of all directives

## Preprocessor Directives Detected

The scanner recognizes the following preprocessor directives:

- `#define` - Defines a macro or constant
- `#undef` - Undefines a previously defined macro
- `#include` - Includes the contents of a file
- `#if` - Conditional compilation (evaluates compile-time expression)
- `#ifdef` - Conditional compilation (checks if macro is defined)
- `#ifndef` - Conditional compilation (checks if macro is not defined)
- `#elif` - Else-if for conditional compilation
- `#else` - Else clause for conditional compilation
- `#endif` - Ends conditional compilation block
- `#error` - Generates a compilation error with a message
- `#warning` - Generates a compilation warning with a message
- `#pragma` - Compiler-specific directive
- `#line` - Changes the line number for compiler messages

## File Types Scanned

The script scans files with the following extensions:
- `.h` - C/C++ header files
- `.hpp` - C++ header files
- `.c` - C source files
- `.cpp` - C++ source files
- `.cc` - C++ source files
- `.ino` - Arduino sketch files

## Examples

From the scan results, you can find:
- All header guards used in the codebase
- All included files and their dependencies
- All conditional compilation blocks
- All macros and constants defined
- All error and warning directives

## Statistics

Recent scan results (as of the last run):
- Total directives found: 3,461
- Most common: `#include` (716 occurrences)
- Files scanned: 225 source files
