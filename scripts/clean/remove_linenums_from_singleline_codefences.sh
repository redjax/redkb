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

  # Process the file to remove linenums="1" only for single-line code blocks
  awk '
    BEGIN { inside_fence = 0; code_lines = ""; }
    {
        if ($0 ~ /^```/) {
            if (inside_fence == 0) {
                # Start of a code block
                inside_fence = 1;
                opening_fence = $0;  # Capture the opening fence
                code_lines = "";
            } else {
                # End of a code block
                if (length(code_lines) == 1) {
                    # If there was exactly one line inside the block, remove linenums="1"
                    gsub(/ linenums="1"/, "", opening_fence);  # Remove linenums="1"
                    print opening_fence;
                    print code_lines[1];  # Print the single line inside the block
                } else {
                    # If the block contains more than one line, print as is
                    print opening_fence;
                    for (i = 1; i <= length(code_lines); i++) {
                        print code_lines[i];
                    }
                }
                print $0;  # Always print the closing fence
                inside_fence = 0;
                code_lines = "";
            }
        } else if (inside_fence == 1) {
            # Capture the lines inside the block
            code_lines[length(code_lines) + 1] = $0;
        } else {
            # Outside of a code block, print the line
            print $0;
        }
    }' "$FILE" >"$TEMP_FILE"

  # Replace the original file with the processed content
  mv "$TEMP_FILE" "$FILE"
}

echo "This script is currently broken."
exit 0

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
