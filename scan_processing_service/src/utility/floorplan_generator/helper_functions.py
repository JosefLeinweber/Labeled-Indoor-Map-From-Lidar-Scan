import math
import numpy as np
from scipy.spatial import Delaunay

import loguru


def generate_line(
    camera_pose_ar_frame, angle_x=0, angle_y=0, angle_z=0, color=[1, 0, 0], length=100
):
    rotated_points = []

    # Convert degrees to radians
    angle_x_rad = math.radians(angle_x)
    angle_y_rad = math.radians(angle_y)
    angle_z_rad = math.radians(angle_z)

    # Create individual rotation matrices
    # Rotation matrix around X-axis
    Rx = np.array(
        [
            [1, 0, 0],
            [0, math.cos(angle_x_rad), -math.sin(angle_x_rad)],
            [0, math.sin(angle_x_rad), math.cos(angle_x_rad)],
        ]
    )

    # Rotation matrix around Y-axis
    Ry = np.array(
        [
            [math.cos(angle_y_rad), 0, math.sin(angle_y_rad)],
            [0, 1, 0],
            [-math.sin(angle_y_rad), 0, math.cos(angle_y_rad)],
        ]
    )

    # Rotation matrix around Z-axis
    Rz = np.array(
        [
            [math.cos(angle_z_rad), -math.sin(angle_z_rad), 0],
            [math.sin(angle_z_rad), math.cos(angle_z_rad), 0],
            [0, 0, 1],
        ]
    )

    # Combine the individual rotation matrices to obtain the final rotation matrix
    # The order of multiplication matters depending on the desired rotation order.
    # Here, we perform ZYX rotation (rotate around Z-axis first, then Y-axis, and finally X-axis).
    R = np.dot(Rz, np.dot(Ry, Rx))

    for i in range(0, length, 1):
        point = np.dot(camera_pose_ar_frame[:3, :3], np.array([0, 0, -i / 10]))
        rotated_points.append(np.dot(R, point) + camera_pose_ar_frame[:3, 3])

    return np.asarray(rotated_points)


def alpha_shape(points, alpha, only_outer=True):
    loguru.logger.debug(f"* alpha_shape is starting")
    """
    # FROM SOME INTERNET FORUM :O
    Compute the alpha shape (concave hull) of a set of points.
    :param points: np.array of shape (n,2) points.
    :param alpha: alpha value.
    :param only_outer: boolean value to specify if we keep only the outer border
    or also inner edges.
    :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
    the indices in the points array.
    """
    assert points.shape[0] > 3, "Need at least four points"

    def add_edge(edges, i, j):
        """
        Add an edge between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # if both neighboring triangles are in shape, it's not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))

    tri = Delaunay(points)
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.simplices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < alpha:
            add_edge(edges, ia, ib)
            add_edge(edges, ib, ic)
            add_edge(edges, ic, ia)

    loguru.logger.debug(f"* alpha_shape finished")
    return edges
