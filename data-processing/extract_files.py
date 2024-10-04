import os

def main():
    import argparse
    from pathlib import Path

    # Define the file extensions to include
    INCLUDED_EXTENSIONS = {'.py', '.css', '.txt', '.json', '.csv', '.md'}

    # Define additional files to exclude
    EXCLUDED_FILES = {'extracted_contents.txt', 'extract_files.py'}

    # Define directories to exclude (e.g., virtual environments)
    EXCLUDED_DIRS = {'venv', 'myenv', 'env', '__pycache__'}

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract specific file types into a single text file.")
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='The root directory to start extraction (default: current directory).'
    )
    parser.add_argument(
        '-o', '--output',
        default='extracted_contents.txt',
        help='The output text file (default: extracted_contents.txt).'
    )
    args = parser.parse_args()

    root_dir = Path(args.directory).resolve()
    output_file = Path(args.output).resolve()

    # Add the output file to the exclusion list to prevent it from being read if located within the root_dir
    EXCLUDED_FILES.add(output_file.name)

    if not root_dir.is_dir():
        print(f"Error: The specified directory '{root_dir}' does not exist or is not a directory.")
        return

    with output_file.open('w', encoding='utf-8') as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            current_dir = Path(dirpath)

            # Modify dirnames in-place to exclude hidden directories and those in EXCLUDED_DIRS
            dirnames[:] = [
                d for d in dirnames 
                if not d.startswith('.') and d.lower() not in EXCLUDED_DIRS
            ]

            for filename in filenames:
                if filename.startswith('.'):
                    continue  # Skip hidden files

                if filename in EXCLUDED_FILES:
                    continue  # Skip explicitly excluded files

                file_path = current_dir / filename
                file_extension = file_path.suffix.lower()

                if file_extension not in INCLUDED_EXTENSIONS:
                    continue  # Skip files with unwanted extensions

                try:
                    relative_path = file_path.relative_to(root_dir)
                    outfile.write(f"{relative_path}:\n```\n")

                    if file_extension == '.csv':
                        # Extract only the first 5 lines for CSV files
                        with file_path.open('r', encoding='utf-8') as f:
                            for i in range(5):
                                line = f.readline()
                                if not line:
                                    break  # End of file
                                outfile.write(line)
                            outfile.write("... (abbreviated)\n")
                    else:
                        # Read the entire content for other file types
                        with file_path.open('r', encoding='utf-8') as f:
                            content = f.read()
                            outfile.write(content)
                    
                    outfile.write("```\n\n")
                except UnicodeDecodeError as ude:
                    print(f"Warning: Could not decode file '{file_path}': {ude}")
                    continue
                except Exception as e:
                    print(f"Warning: Could not read file '{file_path}': {e}")
                    continue

    print(f"Extraction complete. Contents have been written to '{output_file}'.")

if __name__ == "__main__":
    main()
