#!/usr/bin/env python3
"""
Extract and list all distinct #define directives from the preprocessor directives scan.
"""

import csv
import re
import sys

def extract_defines(csv_file='preprocessor_directives.csv'):
    """
    Extract all #define directives from the CSV file.
    Returns a dictionary mapping macro names to their occurrences.
    """
    defines = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                directive = row['Directive']
                if directive.startswith('#define'):
                    # Extract the macro name and optional value
                    match = re.match(r'#define\s+(\w+)(?:\s+(.+))?', directive)
                    if match:
                        macro_name = match.group(1)
                        macro_value = match.group(2) if match.group(2) else '(no value)'
                        defines.append({
                            'name': macro_name,
                            'value': macro_value,
                            'directive': directive,
                            'file': row['File'],
                            'line': row['Line Number']
                        })
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}", file=sys.stderr)
        print("Please run scan_preprocessor_directives.py first.", file=sys.stderr)
        sys.exit(1)
    
    return defines

def group_by_macro_name(defines):
    """
    Group defines by macro name.
    """
    grouped = {}
    for define in defines:
        name = define['name']
        if name not in grouped:
            grouped[name] = []
        grouped[name].append(define)
    
    return grouped

def main():
    print("Extracting #define directives...")
    defines = extract_defines()
    
    print(f"Total #define directives found: {len(defines)}")
    
    grouped = group_by_macro_name(defines)
    print(f"Unique macro names: {len(grouped)}")
    print()
    
    # Generate distinct list output files
    
    # 1. Simple list of unique macro names
    with open('distinct_defines_list.txt', 'w', encoding='utf-8') as f:
        f.write("Distinct #define Macro Names\n")
        f.write("=" * 50 + "\n\n")
        for macro_name in sorted(grouped.keys()):
            f.write(f"{macro_name}\n")
    
    print("Created: distinct_defines_list.txt (simple list of macro names)")
    
    # 2. Detailed list with first occurrence
    with open('distinct_defines_detailed.txt', 'w', encoding='utf-8') as f:
        f.write("Distinct #define Directives with Details\n")
        f.write("=" * 80 + "\n\n")
        
        for macro_name in sorted(grouped.keys()):
            occurrences = grouped[macro_name]
            first = occurrences[0]
            
            f.write(f"Macro: {macro_name}\n")
            f.write(f"  Directive: {first['directive']}\n")
            f.write(f"  First occurrence: {first['file']}:{first['line']}\n")
            f.write(f"  Total occurrences: {len(occurrences)}\n")
            f.write("\n")
    
    print("Created: distinct_defines_detailed.txt (detailed info with first occurrence)")
    
    # 3. CSV format with all occurrences
    with open('distinct_defines.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Macro Name', 'Directive', 'File', 'Line', 'Occurrences'])
        
        for macro_name in sorted(grouped.keys()):
            occurrences = grouped[macro_name]
            first = occurrences[0]
            writer.writerow([
                macro_name,
                first['directive'],
                first['file'],
                first['line'],
                len(occurrences)
            ])
    
    print("Created: distinct_defines.csv (CSV format with occurrence counts)")
    
    # 4. Markdown table
    with open('distinct_defines.md', 'w', encoding='utf-8') as f:
        f.write("# Distinct #define Directives\n\n")
        f.write(f"Total unique macro names: {len(grouped)}\n\n")
        
        # Statistics
        f.write("## Statistics\n\n")
        f.write(f"- Total #define directives: {len(defines)}\n")
        f.write(f"- Unique macro names: {len(grouped)}\n")
        f.write(f"- Average occurrences per macro: {len(defines) / len(grouped):.2f}\n\n")
        
        # Most frequently defined
        f.write("## Most Frequently Defined Macros\n\n")
        sorted_by_freq = sorted(grouped.items(), key=lambda x: len(x[1]), reverse=True)[:20]
        f.write("| Rank | Macro Name | Occurrences |\n")
        f.write("|------|------------|-------------|\n")
        for i, (name, occurrences) in enumerate(sorted_by_freq, 1):
            f.write(f"| {i} | `{name}` | {len(occurrences)} |\n")
        
        f.write("\n## All Unique Macros\n\n")
        f.write("| Macro Name | First Occurrence | File | Line | Total Occurrences |\n")
        f.write("|------------|------------------|------|------|-------------------|\n")
        
        for macro_name in sorted(grouped.keys()):
            occurrences = grouped[macro_name]
            first = occurrences[0]
            directive_short = first['directive'][:60] + '...' if len(first['directive']) > 60 else first['directive']
            directive_escaped = directive_short.replace('|', '\\|')
            f.write(f"| `{macro_name}` | `{directive_escaped}` | {first['file'][:40]} | {first['line']} | {len(occurrences)} |\n")
    
    print("Created: distinct_defines.md (Markdown report with statistics)")
    
    print("\nSummary:")
    print(f"  {len(grouped)} unique macro names")
    print(f"  {len(defines)} total #define directives")
    print(f"\nMost frequently defined macros:")
    for i, (name, occurrences) in enumerate(sorted_by_freq[:10], 1):
        print(f"    {i}. {name}: {len(occurrences)} occurrences")

if __name__ == '__main__':
    main()
