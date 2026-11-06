
import os

ROOT = "file_system_demo"
file_index = {}

os.makedirs(ROOT, exist_ok=True)


# Build an index of existing files
def build_index():
    file_index.clear()

    for folder, directories, files in os.walk(ROOT):
        for filename in files:
            full_path = os.path.join(folder, filename)
            relative_path = os.path.relpath(full_path, ROOT)

            file_index[relative_path] = full_path


# Get a safe path inside the demo directory
def get_path(name):
    full_path = os.path.abspath(os.path.join(ROOT, name))
    root_path = os.path.abspath(ROOT)

    if os.path.commonpath([root_path, full_path]) != root_path:
        return None

    return full_path


# Create a directory
def create_directory():
    name = input("Enter directory name: ")
    path = get_path(name)

    if path is None:
        print("Invalid directory path.")
    elif os.path.exists(path):
        print("Directory already exists.")
    else:
        os.makedirs(path)
        print("Directory created successfully.")


# List directories
def list_directories():
    print("\nDIRECTORIES")

    for folder, directories, files in os.walk(ROOT):
        for directory in directories:
            path = os.path.join(folder, directory)
            print(os.path.relpath(path, ROOT))


# Delete an empty directory
def delete_directory():
    name = input("Enter directory name: ")
    path = get_path(name)

    if path is None or not os.path.isdir(path):
        print("Directory does not exist.")
        return

    try:
        os.rmdir(path)
        print("Directory deleted successfully.")
    except OSError:
        print("Directory is not empty or cannot be deleted.")


# Create a file
def create_file():
    name = input("Enter file path: ")
    path = get_path(name)

    if path is None:
        print("Invalid file path.")
        return

    try:
        with open(path, "x"):
            pass

        file_index[os.path.normpath(name)] = path
        print("File created successfully.")

    except FileExistsError:
        print("File already exists.")
    except FileNotFoundError:
        print("Parent directory does not exist.")


# Write content to a file
def write_file():
    name = os.path.normpath(input("Enter file path: "))

    if name not in file_index:
        print("File not found in index.")
        return

    content = input("Enter content: ")

    with open(file_index[name], "w") as file:
        file.write(content)

    print("Content written successfully.")


# Read a file
def read_file():
    name = os.path.normpath(input("Enter file path: "))

    if name not in file_index:
        print("File not found in index.")
        return

    with open(file_index[name], "r") as file:
        print("\nFile content:")
        print(file.read())


# Update existing content
def update_file():
    name = os.path.normpath(input("Enter file path: "))

    if name not in file_index:
        print("File not found in index.")
        return

    old_text = input("Enter text to replace: ")
    new_text = input("Enter new text: ")

    with open(file_index[name], "r") as file:
        content = file.read()

    if old_text not in content:
        print("Text was not found.")
        return

    content = content.replace(old_text, new_text)

    with open(file_index[name], "w") as file:
        file.write(content)

    print("File updated successfully.")


# Delete a file
def delete_file():
    name = os.path.normpath(input("Enter file path: "))

    if name not in file_index:
        print("File not found in index.")
        return

    os.remove(file_index[name])
    del file_index[name]

    print("File deleted successfully.")


# Display indexed files
def list_files():
    print("\nINDEXED FILES")

    if not file_index:
        print("No files found.")
    else:
        for name in file_index:
            print(name)


# Main menu
def main():
    build_index()

    while True:
        print("\nFILE SYSTEM MANAGEMENT")
        print("======================")
        print("1. Create directory")
        print("2. List directories")
        print("3. Create file")
        print("4. Write to file")
        print("5. Read file")
        print("6. Update file")
        print("7. Delete file")
        print("8. List indexed files")
        print("9. Delete directory")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            create_directory()
        elif choice == "2":
            list_directories()
        elif choice == "3":
            create_file()
        elif choice == "4":
            write_file()
        elif choice == "5":
            read_file()
        elif choice == "6":
            update_file()
        elif choice == "7":
            delete_file()
        elif choice == "8":
            list_files()
        elif choice == "9":
            delete_directory()
        elif choice == "0":
            print("Program ended.")
            break
        else:
            print("Invalid option. Try again.")


main()
