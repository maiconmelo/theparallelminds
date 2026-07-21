#!/usr/bin/env python3
"""
Generate a keyword presence matrix from keywords.txt (CASE-INSENSITIVE)
Output: matrix.csv (ID, keyword1, keyword2, ...) with 1/0 values
"""

import csv
import re
from collections import OrderedDict

def normalize_keyword(kw):
    """Normalize keyword to lowercase for case-insensitive comparison"""
    return kw.lower().strip()

def parse_keywords_file(filename):
    """Parse the keywords.txt file and return a list of (id, keywords_list)"""
    entries = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split by tab first (ID\tkeywords)
            parts = line.split('\t')
            if len(parts) >= 2:
                entry_id = parts[0].strip()
                keywords_str = parts[1].strip()
            else:
                # Fallback: split by first space or comma
                match = re.match(r'^(\d+)\s+(.+)$', line)
                if match:
                    entry_id = match.group(1)
                    keywords_str = match.group(2)
                else:
                    continue
            
            # Parse keywords (comma-separated, possibly with spaces)
            # Normalize each keyword to lowercase
            keywords = [normalize_keyword(k) for k in keywords_str.split(',') if k.strip()]
            entries.append((entry_id, keywords))
    
    return entries

def build_matrix(entries):
    """Build the presence matrix with case-insensitive keywords"""
    # Collect all unique keywords across all entries (normalized to lowercase)
    all_keywords = OrderedDict()
    for _, keywords in entries:
        for kw in keywords:
            all_keywords[kw] = 0  # placeholder
    
    # Sort keywords alphabetically for consistent output
    sorted_keywords = sorted(all_keywords.keys())
    
    # Build matrix rows
    matrix = []
    for entry_id, keywords in entries:
        row = {'ID': entry_id}
        kw_set = set(keywords)  # Already normalized to lowercase
        for kw in sorted_keywords:
            row[kw] = 1 if kw in kw_set else 0
        matrix.append(row)
    
    return matrix, sorted_keywords

def write_csv(matrix, sorted_keywords, output_file='matrix.csv'):
    """Write the matrix to a CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['ID'] + sorted_keywords
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matrix)
    
    print(f"✅ Matrix written to {output_file}")
    print(f"📊 Total rows: {len(matrix)}")
    print(f"📊 Total columns (unique keywords, case-insensitive): {len(sorted_keywords)}")

def main():
    # Parse the input file
    entries = parse_keywords_file('keywords.txt')
    print(f"📖 Parsed {len(entries)} entries from keywords.txt")
    
    # Build the matrix
    matrix, sorted_keywords = build_matrix(entries)
    
    # Write to CSV
    write_csv(matrix, sorted_keywords, 'matrix.csv')
    
    # Optional: Also save as JSON for programmatic use
    import json
    json_data = {
        'keywords': sorted_keywords,
        'matrix': [
            {'id': row['ID'], 'keywords': [kw for kw in sorted_keywords if row[kw] == 1]}
            for row in matrix
        ]
    }
    with open('matrix.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"✅ Also saved JSON version to matrix.json")
    
    # Print some statistics
    print(f"\n📊 Statistics:")
    print(f"   - Unique keywords: {len(sorted_keywords)}")
    
    # Show examples of normalized keywords that had variations
    variations_found = {
        'xcat': ['xcat', 'xcat'],
        'infiniband': ['infiniband', 'infiniband'],
        'kubernetes': ['kubernetes', 'kubernetes'],
    }
    # (The normalization handles this automatically)

if __name__ == '__main__':
    main()