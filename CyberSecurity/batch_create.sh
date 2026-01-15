#!/bin/bash
# This script will help track progress as files are created

TOTAL=76
CURRENT=$(ls -1 *.rst 2>/dev/null | wc -l)

echo "========================================="
echo "BATCH FILE CREATION TRACKER"
echo "========================================="
echo "Current: $CURRENT/$TOTAL ($(echo "scale=1; $CURRENT*100/$TOTAL" | bc)%)"
echo "Target: Complete all $TOTAL files"
echo ""
echo "Creating remaining $(($TOTAL - $CURRENT)) files..."
echo "========================================="
