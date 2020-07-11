import pybullet as p
import time
import pybullet_data

from scripts.create_objs import load_x_objs, load_obj
from scripts.find_obj import get_bbox
# from scripts.gen_coco import generate_pic_with_annotation

DIR_TO_TEST = "00000002"

EXTRACTED_FOLDER = "./resource/models/extracted"
TEMPLATE_URDF_PATH = "./templates/template.urdf"

if __name__ == "__main__":
    physics_client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0.0, 0.0, -9.8)
    p.setRealTimeSimulation(1)
    p.resetDebugVisualizerCamera(15, 0, -45, [0, 0, 0])
    plane_id = p.loadURDF("plane.urdf")

    obj_data = load_x_objs(EXTRACTED_FOLDER, 8, 6)

    # obj_id = load_obj("./resource/wrench.obj", 0, 0, 1)

    # generate_pic_with_annotation(obj_ids)

    # forcefully stabilize
    for _ in range(10000):
        p.removeAllUserDebugItems()
        p.stepSimulation()

        for objdata in obj_data:
            obj_id = objdata['id']
            obj_file = objdata['file']
            obj_pos, obj_orn = p.getBasePositionAndOrientation(obj_id)
            p.addUserDebugText(str(obj_file), obj_pos, [0, 0, 0])

    while True:
        p.removeAllUserDebugItems()
        p.stepSimulation()

        # aa, bb = get_bbox(obj_id, True)

        for objdata in obj_data:
            obj_id = objdata['id']
            obj_file = objdata['file']
            obj_pos, obj_orn = p.getBasePositionAndOrientation(obj_id)
            p.addUserDebugText(str(obj_file), obj_pos, [0, 0, 0])
        # print(u, v)

        time.sleep(1./240.)

    p.disconnect()
