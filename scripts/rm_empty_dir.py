# remove empty folders from models folder.

import os

root = '../0000'
folders = list(os.walk(root))[1:]

for folder in folders:
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:
        os.rmdir(folder[0])
