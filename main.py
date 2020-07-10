import pybullet as p
import time
import pybullet_data

from scripts.create_urdf import load_x_urdfs

DIR_TO_TEST = "00000002"

EXTRACTED_FOLDER = "./resource/models/extracted"
TEMPLATE_URDF_PATH = "./templates/template.urdf"

if __name__ == "__main__":
    physics_client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0.0, 0.0, -9.0)
    plane_id = p.loadURDF("plane.urdf")

    load_x_urdfs(EXTRACTED_FOLDER, 10, 10)

    for i in range(10000):
        p.stepSimulation()
        time.sleep(1./240.)

    p.disconnect()
