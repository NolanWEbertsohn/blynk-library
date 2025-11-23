#!/usr/bin/env python3
"""
Scan all C/C++ files in the repository for preprocessor directives.
Outputs: directive type, file name, line number, and description of intended use.
"""

import os
import re
import csv
import sys
from pathlib import Path

# Common preprocessor directives and their descriptions
DIRECTIVE_DESCRIPTIONS = {
    '#define': 'Defines a macro or constant',
    '#undef': 'Undefines a previously defined macro',
    '#include': 'Includes the contents of a file',
    '#if': 'Conditional compilation - evaluates compile-time expression',
    '#ifdef': 'Conditional compilation - checks if macro is defined',
    '#ifndef': 'Conditional compilation - checks if macro is not defined',
    '#elif': 'Else-if for conditional compilation',
    '#else': 'Else clause for conditional compilation',
    '#endif': 'Ends conditional compilation block',
    '#error': 'Generates a compilation error with a message',
    '#warning': 'Generates a compilation warning with a message',
    '#pragma': 'Compiler-specific directive',
    '#line': 'Changes the line number for compiler messages',
}

def get_directive_description(directive_line):
    """
    Get a detailed description of what a specific directive is doing.
    """
    directive_line = directive_line.strip()
    
    # Extract the directive type
    directive_type = None
    for key in DIRECTIVE_DESCRIPTIONS.keys():
        if directive_line.startswith(key):
            directive_type = key
            break
    
    if not directive_type:
        return "Unknown preprocessor directive"
    
    base_desc = DIRECTIVE_DESCRIPTIONS[directive_type]
    
    # Add context-specific description
    if directive_type == '#define':
        match = re.search(r'#define\s+(\w+)', directive_line)
        if match:
            macro_name = match.group(1)
            return f"{base_desc} ({macro_name})"
        
    elif directive_type == '#include':
        match = re.search(r'#include\s+[<"]([^>"]+)[>"]', directive_line)
        if match:
            include_file = match.group(1)
            return f"{base_desc} ({include_file})"
    
    elif directive_type == '#ifdef':
        match = re.search(r'#ifdef\s+(\w+)', directive_line)
        if match:
            macro_name = match.group(1)
            return f"{base_desc} ({macro_name})"
    
    elif directive_type == '#ifndef':
        match = re.search(r'#ifndef\s+(\w+)', directive_line)
        if match:
            macro_name = match.group(1)
            return f"{base_desc} ({macro_name}) - likely header guard"
    
    elif directive_type == '#if':
        return f"{base_desc} - {directive_line[3:].strip()}"
    
    elif directive_type == '#error':
        msg = directive_line[6:].strip()
        return f"{base_desc}: {msg}"
    
    elif directive_type == '#warning':
        msg = directive_line[8:].strip()
        return f"{base_desc}: {msg}"
    
    elif directive_type == '#pragma':
        return f"{base_desc} - {directive_line[7:].strip()}"
    
    return base_desc

def is_preprocessor_directive(line):
    """
    Check if a line is a preprocessor directive.
    """
    line = line.strip()
    return line.startswith('#') and any(line.startswith(d) for d in DIRECTIVE_DESCRIPTIONS.keys())

def scan_file(filepath):
    """
    Scan a single file for preprocessor directives.
    Returns a list of tuples: (directive, filename, line_number, description)
    """
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if is_preprocessor_directive(line):
                    directive = line.strip()
                    description = get_directive_description(directive)
                    results.append((directive, str(filepath), line_num, description))
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    
    return results

def find_source_files(root_dir):
    """
    Find all C/C++ source files in the repository.
    """
    extensions = {'.h', '.hpp', '.c', '.cpp', '.cc', '.ino'}
    source_files = []
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['build', 'dist', 'node_modules']]
        
        for file in files:
            if Path(file).suffix in extensions:
                source_files.append(os.path.join(root, file))
    
    return sorted(source_files)

def main():
    """
    Main function to scan all files and output results.
    """
    # Get the repository root (current directory)
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Scanning repository: {repo_root}")
    print("Finding source files...")
    
    source_files = find_source_files(repo_root)
    print(f"Found {len(source_files)} source files")
    
    all_directives = []
    
    print("Scanning files for preprocessor directives...")
    for filepath in source_files:
        directives = scan_file(filepath)
        all_directives.extend(directives)
    
    print(f"Found {len(all_directives)} preprocessor directives")
    
    # Output as CSV
    csv_output = os.path.join(repo_root, 'preprocessor_directives.csv')
    with open(csv_output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Directive', 'File', 'Line Number', 'Description'])
        for directive, filename, line_num, description in all_directives:
            # Make file path relative to repo root
            rel_path = os.path.relpath(filename, repo_root)
            writer.writerow([directive, rel_path, line_num, description])
    
    print(f"Results written to: {csv_output}")
    
    # Also output as Markdown
    md_output = os.path.join(repo_root, 'preprocessor_directives.md')
    with open(md_output, 'w', encoding='utf-8') as mdfile:
        mdfile.write("# Preprocessor Directives in Blynk Library\n\n")
        mdfile.write(f"Total directives found: {len(all_directives)}\n\n")
        mdfile.write("## Summary by Directive Type\n\n")
        
        # Count by directive type
        directive_counts = {}
        for directive, _, _, _ in all_directives:
            dtype = directive.split()[0]
            directive_counts[dtype] = directive_counts.get(dtype, 0) + 1
        
        for dtype, count in sorted(directive_counts.items()):
            mdfile.write(f"- `{dtype}`: {count}\n")
        
        mdfile.write("\n## All Directives\n\n")
        mdfile.write("| Directive | File | Line | Description |\n")
        mdfile.write("|-----------|------|------|-------------|\n")
        
        for directive, filename, line_num, description in all_directives:
            rel_path = os.path.relpath(filename, repo_root)
            # Escape pipes in directive and description for markdown
            directive_escaped = directive.replace('|', '\\|')
            description_escaped = description.replace('|', '\\|')
            mdfile.write(f"| `{directive_escaped}` | {rel_path} | {line_num} | {description_escaped} |\n")
    
    print(f"Results also written to: {md_output}")
    
    print("\nSummary by directive type:")
    for dtype, count in sorted(directive_counts.items()):
        print(f"  {dtype}: {count}")

if __name__ == '__main__':
    main()
