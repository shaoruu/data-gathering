import os
import glob
import fileinput
from shutil import copyfile
from random import randrange

# foldername = folder name in extracted

TEMPLATE_PLACEHOLDER = "TEMPLATE"
COLOR_PLACEHOLDER = "COLOR"


def get_first_file_of_ext(directory, ext):
    return [f for f in os.listdir(
        directory) if f.endswith(ext)][0]


def create_urdf(foldername, extracted_folder, template_urdf_path):
    target_dir = os.path.join(extracted_folder, foldername)

    obj_file = get_first_file_of_ext(target_dir, ".obj")[:-4]
    copied_file = os.path.join(target_dir, f"{obj_file}.urdf")

    copyfile(template_urdf_path, copied_file)

    with open(copied_file, 'r+') as file:
        filedata = file.read()
        filedata = filedata.replace(TEMPLATE_PLACEHOLDER, obj_file)
        filedata = filedata.replace(
            COLOR_PLACEHOLDER, f"{randrange(5)/10 + .5} {randrange(5)/10 + .5} {randrange(5)/10 + .5}")
        file.seek(0)
        file.write(filedata)

    return copied_file


def load_x_urdfs(p, parent_folder, urdf_template_path, count, offset=0):
    folders = os.listdir(parent_folder)[offset:offset+count]

    pos_offset = int(count / 2)

    for folder in folders:
        pos_x = randrange(pos_offset) - pos_offset / 2
        pos_y = randrange(pos_offset) - pos_offset / 2
        pos_z = 1

        obj_urdf_path = create_urdf(folder, parent_folder, urdf_template_path)
        obj_start_pos = [pos_x, pos_y, pos_z]
        obj_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
        obj_id = p.loadURDF(obj_urdf_path, obj_start_pos,
                            obj_start_orientation)
