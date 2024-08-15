import os
import shutil
import subprocess
import sys
from tqdm import tqdm

def count_files_in_directory(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def get_directory_size(directory):
    total_size = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def get_file_size(file_path):
    if os.path.isfile(file_path):
        return os.path.getsize(file_path)
    return 0

def copy_to_new_location(paths, new_location):
    if not os.path.exists(new_location):
        os.makedirs(new_location)
    for path in paths:
        destination = os.path.join(new_location, os.path.basename(path))
        if os.path.isdir(path):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(path, destination)
        elif os.path.isfile(path):
            shutil.copy2(path, destination)

def copy_file_with_progress(src, dst):
    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst, tqdm(total=os.path.getsize(src)) as pbar:
        while True:
            buf = fsrc.read(1024)  # Adjust accordingly for larger or smaller buffer sizes
            if not buf:
                break
            fdst.write(buf)
            pbar.update(len(buf))

def copy_to_new_location(paths, new_location, ignore_dir='env'):
    if not os.path.exists(new_location):
        os.makedirs(new_location)
    for path in paths:
        # Skip the ignored directory
        if os.path.basename(path) == ignore_dir:
            continue
        # Copy operations
        destination = os.path.join(new_location, os.path.basename(path))
        if os.path.isdir(path):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(path, destination)
        elif os.path.isfile(path):
            copy_file_with_progress(path, destination)
    print("Done copying.")

def review_files(folder_paths, files_list):
    # Print the header for the grid
    print(f"{'Directory':<30}{'File Count':<10}{'Size (KB)':<15}")

    # Iterate over each directory, count files and calculate size
    for folder_path in folder_paths:
        file_count = count_files_in_directory(folder_path)
        folder_size = get_directory_size(folder_path)
        print(f"{folder_path:<30}{file_count:<10}{folder_size / 1024:<15.2f}")

    # Handle special file cases
    for file_path in files_list:
        file_size = get_file_size(file_path) / 1024  # Convert bytes to kilobytes
        print(f"{file_path:<30}{'1':<10}{file_size:<15.2f}")

def delete_files():
    print("Delete files logic not yet implemented.")

def print_menu():
    print("\nMenu Options:")
    print("1 - Review saved session files")
    print("2 - Copy files")
    print("3 - Delete files")
    print("4 - Exit")

def main():
    # Determine the project root (assuming the script is in a subdirectory of the root)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # List of directories to count files and calculate size
    folder_paths = [

        os.path.join(project_root, '/')
    
    #    os.path.join(project_root, 'files/export'),
    #    os.path.join(project_root, 'files/metrics'),
    #    os.path.join(project_root, 'files/predict'),
    #    os.path.join(project_root, 'files/read_files'),
    #    os.path.join(project_root, 'files/scan_files'),
    #    os.path.join(project_root, 'files/reports'),
    #    os.path.join(project_root, 'backend/image_graphs'),
    #    os.path.join(project_root, 'backend/images'),
    
    ]

    files_list = [os.path.join(project_root, 'sesh.json')]

    while True:
        print_menu()
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            review_files(folder_paths, files_list)

        elif choice == '2':
            all_paths = folder_paths + files_list
            new_directory = input("Enter the name for the new directory (it will be created outside the project root): ").strip()
            destination_path = os.path.join(os.path.dirname(project_root), new_directory)
            print(f"Copying files and directories to {destination_path}...")
            copy_to_new_location(all_paths, destination_path)
            print(f"Items have been copied to {destination_path}")

        elif choice == '3':
            delete_files()

        elif choice == '4':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == '__main__':
    main()
