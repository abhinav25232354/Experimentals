import os

def get_directory_size(directory):
    """
    Calculates the total size of a directory and its subdirectories.

    :param directory: The path to the directory.
    :return: Total size in bytes.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def count_files_by_extension(directory):
    """
    Counts the number of files and categorizes them by extension.

    :param directory: The path to the directory.
    :return: A dictionary with extensions as keys and counts as values.
    """
    file_count = {}
    for root, dirs, files in os.walk(directory):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext not in file_count:
                file_count[ext] = 0
            file_count[ext] += 1
    return file_count

def main():
    directory_path = input("Enter the path of the directory to scan: ")

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # Get the total size of the directory
        directory_size = get_directory_size(directory_path)
        print(f"Total size of '{directory_path}': {directory_size / (1024 * 1024):.2f} MB")

        # Count files by extension
        file_counts_by_extension = count_files_by_extension(directory_path)
        print("\nFiles categorized by extension:")
        for ext, count in sorted(file_counts_by_extension.items()):
            print(f"{ext}: {count}")
    else:
        print(f"The specified path '{directory_path}' does not exist or is not a directory.")

if __name__ == "__main__":
    main()