TEXT_EXTENSIONS = {
    ".txt",
    ".csv",
    ".json",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".md",
    ".xml",
    ".yaml",
    ".yml",
    ".log"
}

from pathlib import Path
import os

def read_file(file_path):

    if not os.path.isfile(file_path):
        return f"{file_path} does not exist."

    extension = Path(file_path).suffix.lower()

    if extension in TEXT_EXTENSIONS:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        return "This file type cannot be read as text."

def write_file(file_path, text):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
        if os.path.isfile(file_path):
            return f"Successfully wrote to {file_path}."
        else:
            return f"Failed to write to {file_path}."

def list_files_in_directory(directory_path):
    print(f"Directory Path: '{directory_path}'")
    if not os.path.isdir(directory_path):
        return f"{directory_path} is not a valid directory."
    files = []
    for root, dirs, filenames in os.walk(directory_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        return f"{file_path} has been deleted."
    else:
        return f"{file_path} does not exist."