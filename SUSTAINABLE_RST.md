# Sustainable RST Table Management

## The Problem We Solved

Box-drawing characters (╔═╗║╠╣╚═╝) look nice in text editors but **don't render as tables** in browsers, GitHub, or documentation sites. They appear as plain text, making data unreadable.

## The Solution

Three-part sustainable approach:

### 1. **Validation Script** (`validate_rst.py`)

Automatically detects problematic box-drawing characters in RST files.

```bash
# Check all files
python3 validate_rst.py

# Expected output:
# ✅ All RST files validated successfully!
# or
# ⚠️  Found 15 issues in 3 files
```

### 2. **Preview Script** (`preview.sh`)

Generate HTML and preview in browser before committing.

```bash
# Preview specific files
./preview.sh Embedded/Embedded_display.rst i.MX_Platform.rst

# Preview all files
./preview.sh --all

# Opens browser at: http://127.0.0.1:8765/
```

### 3. **Style Guide** (`RST_TABLE_GUIDE.rst`)

Complete reference for creating RST tables correctly.

**Quick reference:**

```rst
# ✅ GOOD - Use list-table for data
.. list-table:: My Table
   :header-rows: 1
   :widths: 20 20 20

   * - Header 1
     - Header 2
     - Header 3
   * - Data 1
     - Data 2
     - Data 3

# ✅ GOOD - Use code-block for decoration
.. code-block:: text

   ┌─────────────┐
   │ ASCII Art   │
   └─────────────┘

# ❌ BAD - Don't use raw box-drawing for tables
╔═══════════╗
║ Table     ║
╚═══════════╝
```

## Workflow Integration

### Before Every Commit

```bash
# 1. Validate
python3 validate_rst.py

# 2. Preview (if you added/modified tables)
./preview.sh path/to/modified_file.rst

# 3. Verify tables render correctly in browser

# 4. Commit
git add .
git commit -m "Added X feature with proper RST tables"
```

### Git Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "🔍 Validating RST files..."
python3 validate_rst.py
if [ $? -ne 0 ]; then
    echo "❌ RST validation failed. Fix issues before committing."
    echo "   See RST_TABLE_GUIDE.rst for help."
    exit 1
fi
```

```bash
chmod +x .git/hooks/pre-commit
```

## Current Status

- ✅ **Fixed Files:**
  - `Embedded/Embedded_display.rst` - Framework comparison table
  - `i.MX_Platform.rst` - Processor comparison table
  - `Avionics/ARINC_404.rst` - ATR size specifications
  - `Media_Networking/SCTE35.rst` - Message structure diagram
  - `Avionics/ARINC_Security_Standards.rst` - Alert box
  - `SystemEngineering SafetyCritical/Bow_Tie_Analysis_Cheatsheet.rst` - Bow-tie diagram

- ⚠️ **Remaining:** ~50+ files with decorative box-drawing (low priority)
  - These are mostly ASCII art diagrams in code blocks
  - Only fix if they're meant to be data tables

## When to Fix

**High Priority (fix immediately):**
- Data tables, comparison matrices, specifications
- Content users need to read/copy

**Low Priority (fix when editing):**
- Decorative headers
- ASCII art diagrams
- Already in code blocks

## Tools Required

```bash
# Install once
pip install docutils

# Verify installation
which rst2html.py  # Should return a path
```

## Quick Fixes

### Convert Box Table → List Table

**Before:**
```rst
╔══════════════════════════════════╗
║ Feature     │ Value 1  │ Value 2 ║
╚══════════════════════════════════╝
```

**After:**
```rst
.. list-table::
   :header-rows: 1
   
   * - Feature
     - Value 1
     - Value 2
   * - Row 1
     - Data 1
     - Data 2
```

### Keep Decorative Boxes

**Wrap in code-block:**
```rst
.. code-block:: text

   ╔══════════════════════════════════╗
   ║  Title - Preserved as ASCII Art  ║
   ╚══════════════════════════════════╝
```

## Benefits

✅ **For You:**
- Tables render correctly everywhere (GitHub, browser, docs)
- Easier to maintain (no manual ASCII alignment)
- Copy-paste friendly for readers
- Professional documentation

✅ **For Readers:**
- Proper HTML tables (sortable, searchable, responsive)
- Screen-reader accessible
- Mobile-friendly
- Can copy data easily

## Support

- See `RST_TABLE_GUIDE.rst` for complete formatting guide
- Run `python3 validate_rst.py` to find issues
- Run `./preview.sh <file>` to test rendering

---

**Last Updated:** January 20, 2026
**Files in Library:** 100+ RST files
**Total Lines:** 28,530+ lines of technical documentation
