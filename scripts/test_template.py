# Test and load a template

import pybullet as p
import time
import pybullet_data

from create_urdf import create_urdf


DIR_TO_TEST = "00000002"


physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0.0, 0.0, -1.0)
plane_id = p.loadURDF("plane.urdf")

obj_urdf_path = create_urdf(DIR_TO_TEST)

obj_start_pos = [0, 0, 1]
obj_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
obj_id = p.loadURDF(obj_urdf_path, obj_start_pos, obj_start_orientation)

for i in range(10000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
