# PyBullet test to get familiar with pybullet

import pybullet as p
import time
import pybullet_data

physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0.0, 0.0, -1.0)
plane_id = p.loadURDF("plane.urdf")

cubeStartPos = [0, 0, 1]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
wrench_id = p.loadURDF("../resource/wrench.urdf",
                       cubeStartPos, cubeStartOrientation)

for i in range(10000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
