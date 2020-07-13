import os
import glob
import fileinput
import random
import pybullet as p
from shutil import copyfile

# foldername = folder name in extracted

obj_colors = dict()

IDEAL_VOLUME = 0.01


def get_first_file_of_ext(directory, ext):
    return [f for f in os.listdir(
        directory) if f.endswith(ext)][0]


def get_obj_volume(obj_id):
    (ax, ay, az), (bx, by, bz) = p.getAABB(obj_id)
    return abs(ax - bx) * abs(ay - by) * abs(az - bz)


def load_obj(folder, pathname, x, y, z):
    shift = [0, -0.02, 0]

    # scale = OBJ_AND_SCALE.get(folder)
    # if scale:
    #     meshScale = [scale, scale, scale]

    color = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(
        0, 1)] if pathname not in obj_colors else obj_colors[pathname]
    obj_colors[pathname] = color

    def create(scale=0.01):
        meshScale = [scale, scale, scale]

        visualShapeId = p.createVisualShape(shapeType=p.GEOM_MESH, fileName=pathname, rgbaColor=[
                                            *color, 1], specularColor=[0.4, 0.4, 0], visualFramePosition=shift, meshScale=meshScale)

        try:
            collisionShapeId = p.createCollisionShape(
                shapeType=p.GEOM_MESH, fileName=pathname, collisionFramePosition=shift, meshScale=meshScale)
        except:
            print(pathname)
            return

        uid = p.createMultiBody(baseMass=1, baseInertialFramePosition=[-0.2, 0, 0], baseCollisionShapeIndex=collisionShapeId,
                                baseVisualShapeIndex=visualShapeId, basePosition=[x, y, z], useMaximalCoordinates=True)

        return uid

    test_uid = create()
    test_scale = IDEAL_VOLUME / get_obj_volume(test_uid) ** (1 / 3)
    p.removeBody(test_uid)

    actual_id = create(test_scale)

    for _ in range(150):
        p.stepSimulation()

    return actual_id


def load_x_objs(parent_folder, pos_range, count=-1, offset=0):
    folders = sorted(os.listdir(parent_folder))
    if count != -1:
        folders = folders[offset:offset+count]

    pos_offset = int(count / 2)

    data = []

    for folder in folders:
        target_dir = os.path.join(parent_folder, folder)
        obj_file = get_first_file_of_ext(target_dir, ".obj")
        obj_path = os.path.join(target_dir, obj_file)

        obj_id = load_obj(folder, obj_path, random.uniform(-pos_range, pos_range),
                          random.uniform(-pos_range, pos_range), 5)
        data.append({
            "id": obj_id,
            "file": folder
        })

    return data


OBJ_AND_SCALE = {
    "00000002": 0.03,
    "00000003": 0.08,
    "00000004": 0.03,
    "00000006": 0.3,
    "00000007": 0.01,
    "00000008": 0.024,
    "00000009": 0.011,
    "00000010": 0.02,
    "00000015": 0.01,
    "00000016": 0.01,
    "00000031": 0.03,
    "00000042": 0.01,
    "00000043": 0.003,
    "00000047": 0.01,
    "00000050": 0.03,
    "00000053": 0.03,
    "00000054": 0.001,
    "00000057": 0.02,
    "00000058": 0.03,
    "00000059": 0.0005,
    "00000060": 0.03,
    "00000062": 0.015,
    "00000065": 0.025,
    "00000066": 0.015,
    "00000067": 0.017,
    "00000068": 0.03,
    "00000069": 0.03,
    "00000070": 0.035,
    "00000071": 0.035,
    "00000072": 0.015,
    "00000073": 0.033,
    "00000074": 0.002,
    "00000075": 0.002,
    "00000076": 0.002,
    "00000077": 0.08,
    "00000078": 0.05,
    "00000079": 0.03,
    "00000080": 0.003,
    "00000081": 0.04,
    "00000088": 0.012,
    "00000089": 0.003,
    "00000090": 0.002,
    "00000091": 0.03,
    "00000093": 0.03,
    "00000098": 0.08,
    "00000100": 0.02,
    "00000102": 0.04,
    "00000103": 0.04,
    "00000104": 0.08,
    "00000105": 0.05,
    "00000106": 0.08,
    "00000107": 0.01,
    "00000110": 0.014,
    "00000111": 0.03,
    "00000112": 0.13,
    "00000113": 0.06,
    "00000114": 0.04,
    "00000115": 0.05,
    "00000116": 0.09,
    "00000117": 0.1,
    "00000118": 0.07,
    "00000119": 0.07,
    "00000120": 0.12,
    "00000121": 0.006,
    "00000123": 0.015,
    "00000124": 0.008,
    "00000125": 0.015,
    "00000126": 0.015,
    "00000127": 0.007,
    "00000128": 0.012,
    "00000129": 0.015,
    "00000130": 0.015,
    "00000131": 0.05,
    "00000132": 0.08,
    "00000133": 0.08,
    "00000135": 0.01,
    "00000136": 0.008,
    "00000137": 0.007,
    "00000138": 0.004,
    "00000139": 0.08,
    "00000140": 0.007,
    "00000141": 0.008,
    "00000142": 0.0095,
    "00000144": 0.07,
    "00000145": 0.08,
    "00000146": 0.006,
    "00000147": 0.01,
    "00000152": 0.008,
    "00000153": 0.01,
    "00000154": 0.08,
    "00000157": 0.06,
    "00000167": 0.04,
    "00000170": 0.009,
    "00000171": 0.07,
    "00000172": 0.006,
    "00000174": 0.07,
    "00000175": 0.07,
    "00000176": 0.07,
    "00000177": 0.008,
    "00000178": 0.007,
}
