"""Clean Markdown files of single-line "multiline" codefences.

Description:
    Search for any codefence in a Markdown file that has linenums="1" in the title line,
    but only 1 line of fenced code, and remove the linenums="1" portion.
"""
from __future__ import annotations
import os
import argparse


def remove_linenums_from_singleline_codefence(file_path: str):
    """Iterate over lines in a file to apply match rules.
    
    Description:
        Iterate over lines in a file, find any ```code fences that have linenums="1" in the title line.
        Count the number of rows until the closing ```, and if there is only 1 line, remove linenums="1" from the title.

    Params:
        file_path (str): Path to file to scan/work on.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    new_lines = []
    inside_fence = False
    opening_fence = None
    fence_line_index = None
    content_lines = []

    for i, line in enumerate(lines):
        # Detect opening fence
        if line.startswith("```") and 'linenums="1"' in line and not inside_fence:
            inside_fence = True
            opening_fence = line
            fence_line_index = i
            content_lines = []  # Reset the content lines buffer
            continue

        # Detect closing fence
        if inside_fence and line.startswith("```"):
            inside_fence = False
            # Check if there is exactly one line of content
            if len(content_lines) == 1:
                # Remove linenums="1" from the opening fence
                new_lines.append(opening_fence.replace(' linenums="1"', ""))
            else:
                # Keep the original opening fence
                new_lines.append(opening_fence)
            # Add the content lines and closing fence
            new_lines.extend(content_lines)
            new_lines.append(line)
            continue

        # If inside a code block, track the content lines
        if inside_fence:
            content_lines.append(line)
        else:
            # Outside of a code block, add the line as is
            new_lines.append(line)

    # Write the updated content back to the file
    with open(file_path, "w") as file:
        file.writelines(new_lines)


def process_directory(directory: str):
    """Iterate over a directory, match files, and run a processing rule."""
    ## Iterate over directory path
    for root, _, files in os.walk(directory):
        for file in files:
            ## Search for Markdown files
            if file.endswith(".md"):
                ## Remove linenums="1" line from single-line codefences
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")

                remove_linenums_from_singleline_codefence(file_path)


def main():
    parser = argparse.ArgumentParser(description="Clean Markdown files in a directory.")
    parser.add_argument("--scan-path", "-p", type=str, default="./docs", help="Path to a directory to scan for Markdown files (default: ./docs).")
    
    args = parser.parse_args()
    
    process_directory(args.scan_path)
    print(f"Finished processing files in path '{args.scan_path}'.")

if __name__ == "__main__":
    main()
