import argparse
from pathlib import Path
import re

'''
prepara as pastas para o moodle, renomeando-as para o formato nome_aluno/eN/+page.svelte
'''

def rename_folders_recursive(base_path, pattern, replacement):
    """
    Rename folders recursively by replacing parts of their names that match a regex pattern.

    Args:
        base_path (str): The root directory to start renaming from.
        pattern (str): The regex pattern to search for.
        replacement (str): The string to replace the pattern with.
    """
    try:
        for folder in sorted(base_path.rglob("*"))[::-1]:  # Process folders from the deepest to the shallowest
            if folder.is_dir():
                new_name = re.sub(pattern, replacement, folder.name)
                if new_name != folder.name:
                    new_path = folder.parent / new_name
                    folder.rename(new_path)
                    print(f"Renamed: {folder} -> {new_path}")
    except Exception as e:
        print(f"Error occurred: {e}")


def parse_arguments():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.ArgumentParser: Argument parser.
    """
    parser = argparse.ArgumentParser(description="Recursively rename folders using a regex pattern.")
    parser.add_argument("-a", "--auto", help="Perform automatic renaming with default patterns.", action="store_true")
    parser.add_argument("-p", "--path", help="Path where folders will be recursively renamed.")
    parser.add_argument("-r", "--replace", help="Regex pattern to search for in folder names.")
    parser.add_argument("-s", "--string", help="String to replace the pattern with.")
    return parser


import os
from pathlib import Path


def rename_files_in_folder(folder_path):
    """
    Recursively rename each file in the folder to the format 'eN/+page.svelte',
    where N is an ascending number starting from 1 for each folder.

    Args:
        folder_path (Path): The root directory to start renaming from.
    """
    try:
        # Walk through each folder and its files
        for root, _, files in os.walk(folder_path):
            # Sort files alphabetically (you can modify the sorting if needed)
            files.sort()

            # Initialize a counter for the files in each folder
            for index, file_name in enumerate(files, start=1):
                if not file_name.endswith(".svelte"):
                    continue
                file_path = Path(root) / file_name
                new_name = f"e{index}/+page.svelte"
                new_path = Path(root) / new_name

                # Create the target directory if it doesn't exist
                target_directory = new_path.parent
                target_directory.mkdir(parents=True, exist_ok=True)

                # Rename the file
                file_path.rename(new_path)
                print(f"Renamed: {file_path} -> {new_path}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":

    parser = parse_arguments()
    args = parser.parse_args()

    if args.auto:
        # Automatic renaming using predefined patterns
        base_path = Path(".").resolve()
        print("Starting automatic renaming...")
        rename_folders_recursive(base_path, r"_.*", "")  # Remove everything after an underscore
        rename_folders_recursive(base_path, r"(.{1,15}).*", r"\1")  # Trim folder names to 15 chars
        rename_folders_recursive(base_path, r"_", "")  # Trim folder names to 15 chars
        rename_folders_recursive(base_path, r" ", "_")  # replace spaces by underscores
        rename_folders_recursive(base_path, r"([A-ZÀ-Ý])", lambda match: match.group(0).lower())  # replace uppercase to lowercase, including accented chars
        print("Automatic renaming completed.")

        # Set the path to the folder you want to process
        path = Path(".")  # Replace with your folder path
        if path.is_dir():
            rename_files_in_folder(path)
        else:
            print(f"Error: The path '{path}' is not a valid directory.")

    elif args.path and args.replace and args.string:
        # Validate and resolve the base path
        base_path = Path(args.path).resolve()
        if not base_path.is_dir():
            print(f"Error: The path '{base_path}' does not exist or is not a directory.")
        else:
            print(f"Starting renaming in '{base_path}'...")
            rename_folders_recursive(base_path, rf"{args.replace}", args.string)
            print("Renaming completed.")
    else:
        parser.print_usage()
        print("\nError: Either use '--auto' or provide '-p', '-r', and '-s'.")
