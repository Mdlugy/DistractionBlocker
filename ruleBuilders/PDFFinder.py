import os
import fnmatch
import json
def find_pdfs_with(directory):
    pdfs = []
    # First, we need to get the total number of files for the progress bar
    # total_files = sum([len(files) for r, d, files in os.walk(directory)])
    
    # with tqdm(total=total_files, unit='files', desc='Searching PDFs') as pbar:
    for root, dirs, files in os.walk(directory):
        for file in files:
            # get the file's full path
            file_path = os.path.join(root, file)
            print(file_path)
            # pbar.update(1)  # Update progress bar by one for each file
            if fnmatch.fnmatch(file.lower(), '*.pdf'):
                pdfs.append(file)
    return pdfs
