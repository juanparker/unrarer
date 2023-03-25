import os
import rarfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def find_rar_files(root_dir):
    rar_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.rar'):
                rar_path = os.path.join(dirpath, filename)
                rar_files.append(rar_path)
    return rar_files

def extract_rar(rar_path, dest_dir):
    with rarfile.RarFile(rar_path) as rf:
        rf.extractall(dest_dir)
    return f"Extracted RAR file '{rar_path}' to '{dest_dir}'"

def extract_rar_files_parallel(rar_files, dest_dir, max_workers=None):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_rar, rar_path, dest_dir) for rar_path in rar_files]
        for future in tqdm(as_completed(futures), total=len(rar_files), desc="Extracting", ncols=80, unit="files"):
            print(future.result())

if __name__ == "__main__":
    directory_to_search = input("Enter the directory path to search for RAR files: ")
    destination_directory = input("Enter the directory path to extract the RAR files to: ")
    
    rar_files = find_rar_files(directory_to_search)
    extract_rar_files_parallel(rar_files, destination_directory)
