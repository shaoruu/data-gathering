import pybullet as p
import time
import pybullet_data

from scripts.create_urdf import load_x_urdfs, load_obj
from scripts.find_obj import get_bbox

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

    # load_x_urdfs(EXTRACTED_FOLDER, 5, 10)

    obj_id = load_obj("./resource/wrench.obj", 0, 0, 1)

    for i in range(10000):
        p.stepSimulation()

        aa, bb = get_bbox(obj_id)
        # print(u, v)

        print(aa, bb)

        time.sleep(1./240.)

    p.disconnect()
