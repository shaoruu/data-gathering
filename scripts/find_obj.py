import numpy as np
import pybullet as p


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


def show_viewmatrix_image(viewMatrix, projectionMatrix):
    width, height, rgbImg, depthImg, segImg = p.getCameraImage(
        width=244,
        height=244,
        viewMatrix=viewMatrix,
        projectionMatrix=projectionMatrix)


def compute_basic_matrices():
    viewMatrix = p.computeViewMatrix(
        cameraEyePosition=[0, 0, 3],
        cameraTargetPosition=[0, 0, 0],
        cameraUpVector=[0, 1, 0])
    projectionMatrix = p.computeProjectionMatrixFOV(
        fov=45.0,
        aspect=1.0,
        nearVal=0.1,
        farVal=3.1)

    return viewMatrix, projectionMatrix


def get_obj_2d_pos(obj_id, show_image=False):
    cube_pos, cube_orn = p.getBasePositionAndOrientation(obj_id)

    vm, pm = compute_basic_matrices()

    if show_image:
        show_viewmatrix_image(vm, pm)

    return get_uv(cube_pos, vm, pm)


def pos3d_to_pos2d(pos3d):
    vm, pm = compute_basic_matrices()

    return get_uv(pos3d, vm, pm)


def get_bbox(obj_id, show_image=True):
    aa, bb = p.getAABB(obj_id)

    aau, aav = pos3d_to_pos2d(aa)
    bbu, bbv = pos3d_to_pos2d(bb)

    if show_image:
        vm, pm = compute_basic_matrices()
        show_viewmatrix_image(vm, pm)

    return (aau, aav), (bbu, bbv)
