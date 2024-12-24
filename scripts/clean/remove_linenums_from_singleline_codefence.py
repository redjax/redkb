import os


def process_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    new_lines = []
    inside_fence = False
    line_count = 0
    opening_fence = None
    fence_line_index = None

    for i, line in enumerate(lines):
        # Look for opening code fence (```) with a word like bash, python, etc.
        if line.startswith("```") and not inside_fence:
            inside_fence = True
            opening_fence = line
            fence_line_index = i
            line_count = 0
            new_lines.append(line)
            continue
        elif inside_fence and line.startswith("```"):
            # End of the code block
            if line_count == 1 and 'linenums="1"' in opening_fence:
                # If there was exactly 1 line inside, remove linenums="1"
                opening_fence = opening_fence.replace(' linenums="1"', "")
            # Overwrite the opening fence with modified version (if needed) and add the closing fence
            new_lines[-1] = opening_fence  # Replace the last appended opening fence
            new_lines.append(
                lines[fence_line_index + 1]
            )  # Add the content between fences
            new_lines.append(line)  # Add the closing fence
            inside_fence = False
        elif inside_fence:
            # Count the lines between the opening and closing fences
            line_count += 1
        else:
            # If not inside a fence, just append the line
            new_lines.append(line)

    # Write the processed lines back to the file
    with open(file_path, "w") as file:
        file.writelines(new_lines)


def process_directory(directory):
    # Walk through all files in the given directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                process_file(file_path)


if __name__ == "__main__":
    # docs_dir = "./docs"
    docs_dir = "./test_docs"
    process_directory(docs_dir)
    print("Processing complete.")
