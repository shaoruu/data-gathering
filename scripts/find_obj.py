import numpy as np
import pybullet as p


pixelWidth = 320
pixelHeight = 200


def get_uv(xyz, viewMatrix, projectionMatrix):
    xyz = np.concatenate([xyz, np.array([1.])])
    viewMatrix = np.array(viewMatrix).reshape(4, 4)
    projectionMatrix = np.array(projectionMatrix).reshape(4, 4)

    # print(projectionMatrix)

    xyz = np.dot(xyz, viewMatrix)
    xyz = np.dot(xyz, projectionMatrix)

    u, v, z = xyz[:3]
    u = u / z * 128 / 2 + 128 / 2
    v = (1 - v / z) * 128 / 2

    return u, v


def get_view_image(vm=None, pm=None):
    if not vm and not pm:
        vm, pm = compute_basic_matrices()

    viewMatrix, projectionMatrix = compute_basic_matrices()

    width, height, rgbImg, depthImg, segImg = p.getCameraImage(
        width=244,
        height=244,
        viewMatrix=viewMatrix,
        projectionMatrix=projectionMatrix)

    return rgbImg


def compute_basic_matrices():
    viewMatrix = p.computeViewMatrixFromYawPitchRoll(
        cameraTargetPosition=[0, 0, 0],
        distance=8,
        yaw=180,
        pitch=-90.0,
        roll=0,
        upAxisIndex=2)
    projectionMatrix = p.computeProjectionMatrixFOV(
        fov=60.0,
        aspect=pixelWidth / pixelHeight,
        nearVal=0.01,
        farVal=100)

    return viewMatrix, projectionMatrix


def get_obj_2d_pos(obj_id, show_image=False):
    obj_pos, obj_orn = p.getBasePositionAndOrientation(obj_id)

    vm, pm = compute_basic_matrices()

    if show_image:
        get_view_image(vm, pm)

    return get_uv(obj_pos, vm, pm)


def pos3d_to_pos2d(pos3d):
    vm, pm = compute_basic_matrices()

    return get_uv(pos3d, vm, pm)


def get_bbox(obj_id, show_image=False):
    aa, bb = p.getAABB(obj_id)

    aau, aav = pos3d_to_pos2d(aa)
    bbu, bbv = pos3d_to_pos2d(bb)

    if show_image:
        vm, pm = compute_basic_matrices()
        get_view_image(vm, pm)

    return (aau, aav), (bbu, bbv)
