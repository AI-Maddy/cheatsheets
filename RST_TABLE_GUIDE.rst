================================================================================
RST Table Formatting Guide - Cheatsheet Library Standard
================================================================================

**Purpose:** Ensure tables render correctly in all viewers (GitHub, browsers, docs)

**NEVER USE:** Box-drawing characters (╔═╗║╠╣╚═╝) - they don't render as tables!

================================================================================
✅ RECOMMENDED: List-Table Directive
================================================================================

**When to use:** Data tables, comparison matrices, specifications

**Template:**

.. code-block:: rst

   .. list-table:: Table Title
      :header-rows: 1
      :widths: 20 20 20 20 20
   
   * - Header 1
     - Header 2
     - Header 3
     - Header 4
     - Header 5
   * - Row 1, Col 1
     - Row 1, Col 2
     - Row 1, Col 3
     - Row 1, Col 4
     - Row 1, Col 5
   * - Row 2, Col 1
     - Row 2, Col 2
     - Row 2, Col 3
     - Row 2, Col 4
     - Row 2, Col 5

**Real Example:**

.. list-table:: i.MX Processor Comparison
   :header-rows: 1
   :widths: 15 20 20 18 22

   * - Feature
     - i.MX 93
     - i.MX 8M Plus
     - i.MX 8M Nano
     - i.MX 8QuadMax
   * - Process Node
     - 28nm FD-SOI
     - 14nm FinFET
     - 14nm FinFET
     - 28nm
   * - CPU Cores
     - Dual A55 @1.7GHz
     - Quad A53 @1.8GHz
     - Quad A53 @1.5GHz
     - 4×A72 + 2×A53
   * - GPU
     - ❌ None
     - ✅ GC7000UL
     - ✅ GC7000Lite
     - ✅ GC7000XS×4

**Benefits:**
- ✅ Renders as proper HTML table
- ✅ Works on GitHub, GitLab, ReadTheDocs
- ✅ Easy to maintain (just edit list items)
- ✅ Supports multi-line cells

================================================================================
✅ ALTERNATIVE: Simple Grid Tables
================================================================================

**When to use:** Small tables (< 5 columns), quick reference

**Template:**

.. code-block:: rst

   +----------+----------+----------+
   | Header 1 | Header 2 | Header 3 |
   +==========+==========+==========+
   | Cell 1   | Cell 2   | Cell 3   |
   +----------+----------+----------+
   | Cell 4   | Cell 5   | Cell 6   |
   +----------+----------+----------+

**Benefits:**
- ✅ Renders as HTML table
- ✅ Visually clear in source
- ⚠️  Hard to maintain for large tables

================================================================================
✅ FOR DECORATIVE BOXES: Code-Block
================================================================================

**When to use:** ASCII art, diagrams, decorative headers (not data tables)

**Template:**

.. code-block:: rst

   .. code-block:: text
   
      ┌─────────────────────────────────┐
      │  Decorative Box or ASCII Art    │
      │  This won't become a table      │
      └─────────────────────────────────┘

**Benefits:**
- ✅ Preserves box-drawing characters for visual appeal
- ✅ Clearly marked as non-table content
- ✅ Fixed-width font rendering

================================================================================
❌ NEVER USE: Raw Box-Drawing in Tables
================================================================================

**BAD - Don't do this:**

.. code-block:: rst

   ╔═══════════════════════════════════════╗
   ║ Feature     │ Value 1  │ Value 2     ║
   ╠═══════════════════════════════════════╣
   ║ CPU         │ Dual A55 │ Quad A53    ║
   ╚═══════════════════════════════════════╝

**Problem:** Renders as plain text, not a table. Users can't copy data properly.

================================================================================
🔧 VALIDATION WORKFLOW
================================================================================

**Before committing:**

1. **Run validator:**

   .. code-block:: bash
   
      python3 validate_rst.py

2. **Preview in browser:**

   .. code-block:: bash
   
      ./preview.sh path/to/your_file.rst

3. **Check table rendering** - Should see proper HTML tables, not plain text

**CI/CD Integration (optional):**

Add to `.github/workflows/validate.yml`:

.. code-block:: yaml

   - name: Validate RST files
     run: python3 validate_rst.py

================================================================================
📋 QUICK DECISION TREE
================================================================================

.. code-block:: text

   Need to show tabular data?
   │
   ├─ YES: Data/specs/comparison
   │   │
   │   ├─ Large table (>5 columns or >10 rows)?
   │   │   └─→ Use .. list-table::
   │   │
   │   └─ Small quick-reference table?
   │       └─→ Use +---+---+ grid table
   │
   └─ NO: Just decoration/diagram
       └─→ Use .. code-block:: text with box-drawing

================================================================================
🎯 EXAMPLES FROM THIS LIBRARY
================================================================================

**Good Examples (after fixes):**

- ``i.MX_Platform.rst`` - Line 25: Processor comparison (list-table)
- ``Embedded/Embedded_display.rst`` - Line 890: Framework comparison (list-table)
- ``Avionics/ARINC_404.rst`` - Line 95: ATR sizes (list-table)

**Study these for reference when creating new tables.**

================================================================================
✅ CHECKLIST
================================================================================

Before pushing RST changes:

☐ All data tables use ``.. list-table::`` or grid tables
☐ Box-drawing characters only in ``.. code-block:: text`` sections
☐ Ran ``python3 validate_rst.py`` - no warnings
☐ Ran ``./preview.sh <file>`` - tables render correctly in browser
☐ Table headers clearly labeled
☐ Column widths specified (for list-table)

================================================================================
