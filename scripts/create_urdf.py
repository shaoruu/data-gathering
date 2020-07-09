import os
import glob
import fileinput
from shutil import copyfile

# foldername = folder name in extracted

TEMPLATE_PLACEHOLDER = "TEMPLATE"
EXTRACTED_FOLDER = "../resource/models/extracted"
TEMPLATE_URDF_PATH = "../templates/template.urdf"


def create_urdf(foldername):
    target_dir = os.path.join(EXTRACTED_FOLDER, foldername)

    obj_file = [f for f in os.listdir(
        target_dir) if f.endswith(".obj")][0][:-4]
    copied_file = os.path.join(target_dir, f"{obj_file}.urdf")

    copyfile(TEMPLATE_URDF_PATH, copied_file)

    with open(copied_file, 'r+') as file:
        filedata = file.read()
        filedata = filedata.replace(TEMPLATE_PLACEHOLDER, obj_file)
        file.seek(0)
        file.write(filedata)

    return copied_file
