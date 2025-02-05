#!/bin/bash

# Install mdBook if not installed
if ! command -v mdbook &> /dev/null; then
    echo "Installing mdBook..."
    cargo install mdbook
    cargo install mdbook-pdf
fi

# Create a temporary directory for book processing
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/chapters"

# Copy only non-empty markdown files
for file in chapters/*.md; do
    if [ -s "$file" ]; then  # Check if file is not empty
        cp "$file" "$TEMP_DIR/chapters/"
    fi
done

# Copy other necessary files
cp README.md book.toml "$TEMP_DIR/"

# Create new SUMMARY.md with only non-empty files
echo "# Summary" > "$TEMP_DIR/SUMMARY.md"
echo "" >> "$TEMP_DIR/SUMMARY.md"
echo "* [Introduction](README.md)" >> "$TEMP_DIR/SUMMARY.md"
echo "" >> "$TEMP_DIR/SUMMARY.md"
echo "## Core Chapters" >> "$TEMP_DIR/SUMMARY.md"
echo "" >> "$TEMP_DIR/SUMMARY.md"

# Add only non-empty chapter files to SUMMARY.md
for file in "$TEMP_DIR/chapters"/*.md; do
    if [ -s "$file" ]; then
        chapter_name=$(head -n 1 "$file" | sed 's/^# //')
        echo "* [$chapter_name](${file#$TEMP_DIR/})" >> "$TEMP_DIR/SUMMARY.md"
    fi
done

# Add license if it exists and is not empty
if [ -f LICENSE ] && [ -s LICENSE ]; then
    cp LICENSE "$TEMP_DIR/chapters/license.md"
    echo "" >> "$TEMP_DIR/SUMMARY.md"
    echo "* [License](chapters/license.md)" >> "$TEMP_DIR/SUMMARY.md"
fi

# Build the book from the temporary directory
cd "$TEMP_DIR"
mdbook build

# Copy the generated book back to the original directory
cd -
rm -rf book/
cp -r "$TEMP_DIR/book" .

# Cleanup
rm -rf "$TEMP_DIR"

echo "Book has been generated!"
echo "HTML version: book/html/index.html"
echo "PDF version: book/pdf/output.pdf"