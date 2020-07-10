import os
import glob
import fileinput
import random
import pybullet as p
from shutil import copyfile

# foldername = folder name in extracted

TEMPLATE_PLACEHOLDER = "TEMPLATE"
COLOR_PLACEHOLDER = "COLOR"


def get_first_file_of_ext(directory, ext):
    return [f for f in os.listdir(
        directory) if f.endswith(ext)][0]


def load_obj(pathname, x, y, z):
    shift = [0, -0.02, 0]
    meshScale = [0.01, 0.01, 0.01]

    visualShapeId = p.createVisualShape(shapeType=p.GEOM_MESH, fileName=pathname, rgbaColor=[
                                        1, 1, 1, 1], specularColor=[0.4, 0.4, 0], visualFramePosition=shift, meshScale=meshScale)

    try:
        collisionShapeId = p.createCollisionShape(
            shapeType=p.GEOM_MESH, fileName=pathname, collisionFramePosition=shift, meshScale=meshScale)
    except:
        print(pathname)
        return

    uid = p.createMultiBody(baseMass=1, baseInertialFramePosition=[-0.2, 0, 0], baseCollisionShapeIndex=collisionShapeId,
                            baseVisualShapeIndex=visualShapeId, basePosition=[x, y, z], useMaximalCoordinates=True)

    for _ in range(150):
        p.stepSimulation()

    return uid


def load_x_urdfs(parent_folder, pos_range, count, offset=0):
    folders = os.listdir(parent_folder)[offset:offset+count]

    pos_offset = int(count / 2)

    for folder in folders:
        target_dir = os.path.join(parent_folder, folder)
        obj_file = get_first_file_of_ext(target_dir, ".obj")
        obj_path = os.path.join(target_dir, obj_file)

        load_obj(obj_path, random.uniform(-pos_range, pos_range),
                 random.uniform(-pos_range, pos_range), 0.15)
