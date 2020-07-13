import pybullet as p
import time

from scripts.create_objs import load_x_objs, load_obj
from scripts.find_obj import get_bbox
from scripts.gen_coco import BulletToCOCO

DIR_TO_TEST = "00000002"

EXTRACTED_FOLDER = "./resource/models/extracted"
SAVE_FOLDER = "./coco"


if __name__ == "__main__":
    physics_client = p.connect(p.GUI)
    p.setGravity(0.0, 0.0, -9.8)
    p.setRealTimeSimulation(1)
    p.resetDebugVisualizerCamera(15, 0, -45, [0, 0, 0])
    p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)
    plane_id = p.loadURDF("./resource/plane.urdf")

    # obj_data = load_x_objs(EXTRACTED_FOLDER, 8, 6)

    # generate_pic_with_annotation(obj_ids)

    # forcefully stabilize
    # for _ in range(10000):
    #     p.removeAllUserDebugItems()
    #     p.stepSimulation()

    #     for objdata in obj_data:
    #         obj_id = objdata['id']
    #         obj_file = objdata['file']
    #         obj_pos, obj_orn = p.getBasePositionAndOrientation(obj_id)
    #         p.addUserDebugText(str(obj_file), obj_pos, [0, 0, 0])

    BulletToCOCO(EXTRACTED_FOLDER, SAVE_FOLDER)

    while True:
        # p.removeAllUserDebugItems()
        p.stepSimulation()

        # aa, bb = get_bbox(obj_id, True)

        # for objdata in obj_data:
        #     obj_id = objdata['id']
        #     obj_file = objdata['file']
        #     obj_pos, obj_orn = p.getBasePositionAndOrientation(obj_id)
        #     p.addUserDebugText(str(obj_file), obj_pos, [0, 0, 0])
        # print(u, v)

        time.sleep(1./240.)

    p.disconnect()
