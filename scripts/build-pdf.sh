#!/bin/bash

# Temporarily enable PDF configuration
sed -i.bak 's/# \[output\.pdf\]/[output.pdf]/' book.toml
sed -i.bak 's/# enable/enable/' book.toml
sed -i.bak 's/# renderer/renderer/' book.toml
sed -i.bak 's/# command/command/' book.toml

# Build PDF
mdbook build

# Restore original configuration
mv book.toml.bak book.toml

echo "PDF has been generated at book/pdf/output.pdf"