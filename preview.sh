#!/bin/bash
# Quick preview script - Generate HTML and open in browser

set -e

PREVIEW_DIR="html_preview"
PORT=8765

# Create preview directory
mkdir -p "$PREVIEW_DIR"

# Function to convert RST to HTML
convert_rst() {
    local rst_file="$1"
    local html_file="$PREVIEW_DIR/$(basename "${rst_file%.rst}.html")"
    
    echo "Converting: $rst_file"
    rst2html.py "$rst_file" "$html_file" 2>/dev/null || \
        rst2html5.py "$rst_file" "$html_file" 2>/dev/null || \
        echo "  ⚠️  Warning: Could not convert $rst_file"
}

# Convert specified files or all RST files
if [ $# -eq 0 ]; then
    echo "Usage: ./preview.sh <file.rst> [file2.rst ...]"
    echo "   or: ./preview.sh --all"
    exit 1
fi

if [ "$1" == "--all" ]; then
    echo "🔄 Converting all RST files..."
    find . -name "*.rst" -type f | while read -r file; do
        convert_rst "$file"
    done
else
    for file in "$@"; do
        if [ -f "$file" ]; then
            convert_rst "$file"
        else
            echo "❌ File not found: $file"
        fi
    done
fi

# Check if server is already running
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ HTML files ready at: http://127.0.0.1:$PORT/"
    echo "   Server already running"
else
    echo "✅ HTML files generated"
    echo "🌐 Starting preview server..."
    echo "   Open: http://127.0.0.1:$PORT/"
    echo "   Press Ctrl+C to stop"
    cd "$PREVIEW_DIR" && python3 -m http.server $PORT --bind 127.0.0.1
fi
