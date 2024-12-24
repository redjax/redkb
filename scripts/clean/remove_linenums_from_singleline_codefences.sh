#!/bin/bash

##
# Script removes the 'linenums="1"' part of a ```codefence if the fence has only 1 line.
#
# Example:
#
# ```bash title="example" linenums="1"
#    echo "Hello, world!"
# ```
#
# Becomes:
#
# ```bash title="example"
#    echo "Hello, world!"
# ```
##
# Directory to scan
DOCS_DIR=${1:-"./docs"}

# Function to process a single file
process_file() {
  local FILE="$1"
  local TEMP_FILE="${FILE}.temp"

  # Process the file to remove linenums="1" for single-line code blocks
  awk '
    BEGIN { inside_fence = 0; code_line = ""; }
    {
        if ($0 ~ /^```/) {
            if (inside_fence == 0) {
                # Start of a code block
                inside_fence = 1;
                opening_fence = $0;
            } else {
                # End of a code block
                if (code_line != "") {
                    # Single-line code block detected
                    gsub(/ linenums="1"/, "", opening_fence);
                    print opening_fence;
                    print code_line;
                } else {
                    # Multi-line block or empty block, print as is
                    print opening_fence;
                }
                print $0;  # Always print the closing code fence
                inside_fence = 0;
                code_line = "";
            }
        } else if (inside_fence == 1) {
            # Capture the single code line
            if (code_line == "") {
                code_line = $0;
            } else {
                # Multi-line block detected, reset
                print opening_fence;
                print code_line;
                print $0;
                inside_fence = 0;
                code_line = "";
            }
        } else {
            # Outside of a code block
            print $0;
        }
    }' "$FILE" >"$TEMP_FILE"

  # Replace the original file with the processed content
  mv "$TEMP_FILE" "$FILE"
}

echo "Scanning ${DOCS_DIR} for .md files..."

## Recursively find all .md files in the specified directory and process them
find "$DOCS_DIR" -type f -name "*.md" | while read -r file; do
  echo "Processing: $file"
  process_file "$file"
done

if [[ $? -eq 0 ]]; then
  echo "Processing complete."
else
  echo "Non-zero exit code processing files in ${DOCS_DIR}. Exit code: $?"

  exit $?
fi
