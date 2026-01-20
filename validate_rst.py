#!/usr/bin/env python3
"""
RST File Validator - Checks for common issues before committing
"""
import sys
import re
from pathlib import Path

# Box-drawing characters that don't render as tables in browsers
BOX_DRAWING_CHARS = r'[╔╗╚╝║╠╣╦╩╬═]'

def check_file(filepath):
    """Check a single RST file for issues"""
    issues = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        # Check for box-drawing characters
        if re.search(BOX_DRAWING_CHARS, line):
            issues.append(f"Line {i}: Box-drawing characters detected (use list-table or code-block instead)")
    
    return issues

def main():
    """Validate all RST files in the workspace"""
    cheatsheets_dir = Path(__file__).parent
    rst_files = list(cheatsheets_dir.rglob('*.rst'))
    
    total_issues = 0
    files_with_issues = []
    
    print("🔍 Validating RST files...")
    print("=" * 70)
    
    for rst_file in sorted(rst_files):
        issues = check_file(rst_file)
        if issues:
            files_with_issues.append(rst_file)
            total_issues += len(issues)
            print(f"\n❌ {rst_file.relative_to(cheatsheets_dir)}")
            for issue in issues[:3]:  # Show first 3 issues per file
                print(f"   {issue}")
            if len(issues) > 3:
                print(f"   ... and {len(issues) - 3} more issues")
    
    print("\n" + "=" * 70)
    
    if total_issues == 0:
        print("✅ All RST files validated successfully!")
        return 0
    else:
        print(f"⚠️  Found {total_issues} issues in {len(files_with_issues)} files")
        print("\nFix suggestions:")
        print("  • Replace box-drawing tables with .. list-table::")
        print("  • Or wrap decorative boxes in .. code-block:: text")
        return 1

if __name__ == '__main__':
    sys.exit(main())
